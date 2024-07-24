import os
import torch
import torchaudio
import lzma
import numpy as np
import pybase16384 as b14
import ChatTTS
import subprocess
from cssa.prompt import *
from cssa.llm.zhipu import zhipubot
from cssa.utils import get_text_inside_tag


def llm_refine(text, json_file):
    response = zhipubot.predict(EN_REFINE_PROMPT.format(text))
    print(response)
    speaker_1 = get_text_inside_tag(response, "speaker1")
    speaker_2 = get_text_inside_tag(response, "speaker2")
    prompts_1 = get_text_inside_tag(response, "prompts1")
    prompts_2 = get_text_inside_tag(response, "prompts2")

    return text_batches


class ChatTTSProcessor:
    def __init__(self, model_path, output_dir, device="cpu"):
        self.chat = ChatTTS.Chat()
        self.chat.load(compile=True)
        self.model_path = model_path
        self.output_dir = output_dir
        self.temp_dir = os.path.join(output_dir, "temp")
        self.concat_file = os.path.join(output_dir, "concat.txt")
        self.device = device
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

    @staticmethod
    def compress_and_encode(tensor):
        np_array = tensor.numpy().astype(np.float16)
        compressed = lzma.compress(
            np_array.tobytes(),
            format=lzma.FORMAT_RAW,
            filters=[{"id": lzma.FILTER_LZMA2, "preset": 9 | lzma.PRESET_EXTREME}],
        )
        encoded = b14.encode_to_string(compressed)
        return encoded

    def load_speaker_embedding(self, speaker_name):
        if speaker_name == "A":
            filename = "seed_speaker_man.pt"
        else:
            filename = "seed_speaker_woman.pt"
        path = os.path.join(self.model_path, filename)
        spk_emb = torch.load(path, map_location=torch.device(self.device)).detach()
        return self.compress_and_encode(spk_emb)

    def create_infer_code_params(self, spk_emb_str):
        return ChatTTS.Chat.InferCodeParams(
            spk_emb=spk_emb_str,
            temperature=0.3,
            top_P=0.7,
            top_K=20,
        )

    def create_refine_text_params(self, prompt):
        return ChatTTS.Chat.RefineTextParams(prompt=prompt)

    def process_texts(
        self, texts, params_refine_text, params_infer_code, is_refine=True
    ):
        if is_refine:
            refined_texts = self.chat.infer(
                texts,
                params_refine_text=params_refine_text,
                params_infer_code=params_infer_code,
                refine_text_only=True,
            )
        else:
            refined_texts = texts
        return refined_texts

    def generate_wavs(self, refined_texts, params_refine_text, params_infer_code):
        wavs = self.chat.infer(
            refined_texts,
            params_refine_text=params_refine_text,
            params_infer_code=params_infer_code,
            skip_refine_text=True,
        )
        return wavs

    def save_wav(self, wav, prefix):
        filename = f"{prefix}_output.wav"
        filepath = os.path.join(self.temp_dir, filename)
        torchaudio.save(filepath, torch.from_numpy(wav).unsqueeze(0), 24000)
        print(f"Saved {filepath}")
        return filepath

    def save_wavs(self, wavs, prefix):
        filenames = []
        for i, wav in enumerate(wavs):
            filename = f"{prefix}_output{i}.wav"
            filepath = os.path.join(self.temp_dir, filename)
            torchaudio.save(filepath, torch.from_numpy(wav).unsqueeze(0), 24000)
            filenames.append(filepath)
            print(f"Saved {filepath}")
        return filenames

    def concatenate_wavs(self, wav_files, output_filename):

        with open(self.concat_file, "w") as f:
            for i in wav_files:
                f.write(f"file '{os.path.abspath(i)}'\n")
        output_path = os.path.join(self.output_dir, output_filename)
        subprocess.run(
            [
                "ffmpeg",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                self.concat_file,
                "-c",
                "copy",
                output_path,
            ],
            check=True,
        )
        print(f"Concatenated audio saved at {output_path}")

    def run_batch(
        self, text_batches, speaker_names, prompts, output_filename, is_refine
    ):
        all_filenames = []
        refined_texts_batches = []
        for texts, speaker_name, prompt in zip(text_batches, speaker_names, prompts):
            spk_emb_str = self.load_speaker_embedding(speaker_name)
            params_infer_code = self.create_infer_code_params(spk_emb_str)
            params_refine_text = self.create_refine_text_params(prompt)
            refined_texts = self.process_texts(
                texts, params_refine_text, params_infer_code, is_refine
            )
            refined_texts_batches.append(
                (refined_texts, params_refine_text, params_infer_code)
            )
        for i, data in enumerate(refined_texts_batches):
            wavs = self.generate_wavs(
                data[0],
                data[1],
                data[2],
            )
            if speaker_filenames[i] == "A":
                filename = self.save_wav(wavs[0], f"batch0_text{i}")
                all_filenames.append(filename)
            elif speaker_filenames[i] == "B":
                filename = self.save_wav(wavs[0], f"batch1_text{i}")
                all_filenames.append(filename)
        self.concatenate_wavs(all_filenames, output_filename)


if __name__ == "__main__":
    model_path = "/data/xli/speech-agent/ChatTTS/asset/speaker_emb"
    output_dir = "baseline_outputs"

    processor = ChatTTSProcessor(model_path, output_dir)

    text_batches = [
        "he was in jail for fourteen times and they finally deported him",
        "fourteen times",
        "yes his family spent over two hundred thousand dollars keeping him here",
        "and then finally they said no that is it he is out can not even come back to visit",
        "wow",
    ]
    speaker_filenames = [
        "A",
        "B",
        "A",
        "A",
        "B",
    ]
    prompts = [
        "[oral_2][laugh_0][break_6]",
        "[oral_2][laugh_0][break_6]",
        "[oral_2][laugh_0][break_6]",
        "[oral_2][laugh_0][break_6]",
        "[oral_2][laugh_0][break_6]",
    ]
    processor.run_batch(text_batches, speaker_filenames, prompts, "conversation.wav")
