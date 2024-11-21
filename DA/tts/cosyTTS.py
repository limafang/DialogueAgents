from .base import BaseTTS
from contextlib import contextmanager
import os
import torchaudio
import sys
import subprocess


@contextmanager
def custom_path(path):
    original_sys_path = list(sys.path)
    sys.path.append(path)
    yield
    sys.path = original_sys_path


with custom_path("DA/CosyVoice"):
    from cosyvoice.cli.cosyvoice import CosyVoice
    from cosyvoice.utils.file_utils import load_wav

os.environ["PYTHONPATH"] = "DA/CosyVoice/third_party/Matcha-TTS"


class cosyvoice_agent(BaseTTS):
    def __init__(self, model_path=None, output_dir="outputs", device="gpu"):
        self.chat = CosyVoice(model_path)
        self.output_dir = output_dir
        self.help_dir = output_dir

    def save_wav(self, wav, prefix):
        filename = f"{prefix}_output.wav"
        filepath = os.path.join(self.temp_dir, filename)
        torchaudio.save(filepath, wav["tts_speech"], 22050)
        print(f"Saved {filepath}")
        return filepath

    def concatenate_wavs(self, wav_files, output_filename):
        with open(self.concat_file, "w") as f:
            for i in wav_files:
                f.write(f"file '{os.path.abspath(i)}'\n")
        output_path = os.path.join(self.help_dir, output_filename)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
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

    def add_speaker(self, filename, speaker_name):
        # load speaker
        prompt_speech_16k = load_wav(speaker_name, 16000)
        rhythm_speech_16k = load_wav(filename, 16000)
        output = self.chat.inference_voice_convert(prompt_speech_16k, rhythm_speech_16k)
        torchaudio.save(filename, output["tts_speech"], 22050)

    def run_batch(
        self,
        text_batches: list,
        speakers: list,
        prompts: list,
        wavs: list,
        output_filename: str,
    ):
        self.help_dir = os.path.join(self.output_dir, output_filename.split(".")[0])
        self.temp_dir = os.path.join(self.help_dir, "segments")
        self.concat_file = os.path.join(self.help_dir, "concat.txt")
        os.makedirs(self.help_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        all_filenames = []
        args = zip(text_batches, speakers, prompts, wavs)
        for i, arg in enumerate(args):
            wav = self.chat.inference_instruct(*(arg[:3]))
            filename = self.save_wav(wav, f"{arg[1]}_text{i}")
            self.add_speaker(filename, arg[3])
            all_filenames.append(filename)
        self.concatenate_wavs(all_filenames, output_filename)
