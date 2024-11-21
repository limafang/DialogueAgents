import os
import argparse
from DA.tts.cosyTTS import cosyvoice_agent
from DA.llm.openai import OpenAILLM
from DA.prompt import *
from DA.utils import (
    get_script,
    get_speaker,
    get_text_inside_tag,
    read_json_file,
    save_json,
)
from DA.audio.qwen import QwenAudio


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        type=str,
        required=True,
        help="Execution mode: baseline, refine, or reflection",
    )
    parser.add_argument(
        "--model_path", type=str, required=True, help="Path to the TTS model"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Output directory for generated files",
    )
    parser.add_argument(
        "--script_path", type=str, required=True, help="Path to the script file"
    )
    parser.add_argument(
        "audio_model_path", type=str, help="Path to the audio evaluation model"
    )
    parser.add_argument(
        "--max_loop",
        type=int,
        default=5,
        help="Maximum number of loops in reflection mode",
    )
    return parser.parse_args()


def initialize_tts(model_path, output_dir):
    return cosyvoice_agent(model_path, output_dir)


def initialize_llm():
    return OpenAILLM(
        "gpt-4o",
        os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE_URL"),
    )


def initialize_qwen_audio(model_path):
    return QwenAudio(model_path)


def process_baseline_mode(tts, script_path):
    text_batches, speakers = get_script(script_path)
    speaker_labels, prompts, wavs = [], [], []

    for speaker_group in speakers:
        current_labels, current_prompts, current_wavs = [], [], []
        for speaker in speaker_group:
            label, _, wav = get_speaker(speaker)
            current_labels.append(label)
            current_prompts.append("")
            current_wavs.append(wav)
        speaker_labels.append(current_labels)
        prompts.append(current_prompts)
        wavs.append(current_wavs)

    for i, data in enumerate(text_batches):
        tts.run_batch(
            data, speaker_labels[i], prompts[i], wavs[i], f"conversation{i}.wav"
        )


def process_refine_mode(tts, llm_bot, script_path, output_dir):
    data = read_json_file(script_path)
    text_batches, speakers = get_script(script_path)
    speaker_labels, wavs = [], []

    for speaker_group in speakers:
        current_labels, current_wavs = [], []
        for speaker in speaker_group:
            label, _, wav = get_speaker(speaker)
            current_labels.append(label)
            current_wavs.append(wav)
        speaker_labels.append(current_labels)
        wavs.append(current_wavs)

    for i, script in enumerate(data["scripts"]):
        conversation = script["conversation"]
        res = llm_bot.predict(EN_REFINE_PROMPT_v2.format(text=conversation))
        texts = get_text_inside_tag(res, "speaker")
        prompts = get_text_inside_tag(res, "prompt")

        for j, conv in enumerate(conversation):
            conv["text"] = texts[j]
            conv["prompt"] = prompts[j]

        tts.run_batch(
            texts, speaker_labels[i], prompts, wavs[i], f"conversation{i}.wav"
        )

    save_json(data, f"{output_dir}/data.json")


def process_reflection_mode(
    tts, llm_bot, qwen_audio, script_path, output_dir, max_loop=5
):
    data = read_json_file(script_path)
    text_batches, speakers = get_script(script_path)
    speaker_labels, wavs = [], []

    for speaker_group in speakers:
        current_labels, current_wavs = [], []
        for speaker in speaker_group:
            label, _, wav = get_speaker(speaker)
            current_labels.append(label)
            current_wavs.append(wav)
        speaker_labels.append(current_labels)
        wavs.append(current_wavs)

    for i, script in enumerate(data["scripts"]):
        llm_bot.clear_history()
        conversation = script["conversation"]
        res = llm_bot.chat(EN_REFINE_PROMPT_v2.format(text=conversation))
        texts = get_text_inside_tag(res, "speaker")
        prompts = get_text_inside_tag(res, "prompt")

        tts.run_batch(
            texts, speaker_labels[i], prompts, wavs[i], f"conversation{i}.wav"
        )
        audio_file_path = os.path.join(
            output_dir, f"conversation{i}", f"conversation{i}.wav"
        )

        for _ in range(max_loop):
            eval_res = qwen_audio.evaluate_audio(audio_file_path, EVAL_AUDIO)
            res = llm_bot.chat(UPDATE_REFINE_PROMPT.format(advice=eval_res))
            texts = get_text_inside_tag(res, "speaker")
            prompts = get_text_inside_tag(res, "prompt")

            for j, conv in enumerate(conversation):
                conv["text"] = texts[j]
                conv["prompt"] = prompts[j]

            tts.run_batch(
                texts, speaker_labels[i], prompts, wavs[i], f"conversation{i}.wav"
            )

    save_json(data, f"{output_dir}/data.json")


if __name__ == "__main__":
    args = parse_arguments()
    mode = args.mode
    model_path = args.tts_model_path
    output_dir = args.output_dir
    script_path = args.script_path
    audio_model_path = args.audio_model_path
    max_loop = args.max_loop

    tts = initialize_tts(model_path, output_dir)

    if mode == "baseline":
        process_baseline_mode(tts, script_path)
    elif mode == "refine":
        llm_bot = initialize_llm()
        process_refine_mode(tts, llm_bot, script_path, output_dir)
    elif mode == "reflection":
        llm_bot = initialize_llm()
        qwen_audio = initialize_qwen_audio(audio_model_path)
        process_reflection_mode(
            tts, llm_bot, qwen_audio, script_path, output_dir, max_loop
        )
    else:
        raise ValueError(f"Unknown mode: {mode}")
