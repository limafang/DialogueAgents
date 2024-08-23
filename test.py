from cssa.tts.chatTTS import ChatTTS_agent
from cssa.utils import get_script, replace_
import os

# os.environ["CUDA_VISIBLE_DEVICES"] = "1"

if __name__ == "__main__":
    speaker_path = "speaker_emb"  # speaker embedding path
    output_dir = "baseline_outputs"
    script_path = "example_data.json"
    text_batches, speakers = get_script(script_path)
    processor = ChatTTS_agent(speaker_path, output_dir)

    for i, data in enumerate(text_batches):
        print(data)
        texts = [replace_(j) for j in data]
        prompts_len = len(data)
        prompts = ["[oral_2][laugh_0][break_6]" for _ in range(prompts_len)]
        print(prompts)
        processor.run_batch(
            data, speakers[i], prompts, f"conversation{i}.wav", refine_skip=False
        )
from cssa.prompt import *
from cssa.llm.zhipu import ZhipuLLM
from cssa.prompt import *
from cssa.utils import get_text_inside_tag
from cssa.tts.chatTTS import ChatTTS_agent
from cssa.utils import get_script, read_json_file, replace_


if __name__ == "__main__":
    model_path = "speaker_emb/"
    output_dir = "llm_refine_outputs/"
    script_path = "example_data.json"
    processor = ChatTTS_agent(model_path, output_dir)
    llm_bot = ZhipuLLM("glm-4")
    text_batches, speakers = get_script(script_path)
    data = read_json_file(script_path)
    for i, data in enumerate(data["scripts"]):
        res = llm_bot.predict(CHINESE_REFINE_PROMPT.format(text=data["conversation"]))
        texts = get_text_inside_tag(res, "speaker")
        texts = [replace_(j) for j in texts]
        print(texts)
        prompts = get_text_inside_tag(res, "prompt")
        processor.run_batch(
            texts, speakers[i], prompts, f"conversation{i}.wav", refine_skip=True
        )
from cssa.prompt import *
from cssa.llm.openai import OpenAILLM
from cssa.prompt import *
from cssa.utils import get_text_inside_tag
from cssa.tts.chatTTS import ChatTTS_agent
from cssa.utils import get_script, read_json_file, replace_
from cssa.audio.qwen import QwenAudio

if __name__ == "__main__":
    model_path = "speaker_emb/"
    output_dir = "reflaction_output/"
    max_loop = 3
    script_path = "example_data.json"
    processor = ChatTTS_agent(model_path, output_dir=output_dir)
    llm_bot = OpenAILLM("gpt-4o")
    audio_bot = QwenAudio()
    text_batches, speakers = get_script(script_path)
    data = read_json_file(script_path)
    for i, data in enumerate(data["scripts"]):
        res = llm_bot.chat(CHINESE_REFINE_PROMPT.format(text=data["conversation"]))
        texts = get_text_inside_tag(res, "speaker")
        texts = [replace_(m) for m in texts]
        prompts = get_text_inside_tag(res, "prompt")
        processor.run_batch(
            texts, speakers[i], prompts, f"conversation{i}.wav", refine_skip=True
        )
        audio_file_path = output_dir + f"conversation{i}.wav"
        for j in range(max_loop):
            eval_res = audio_bot.evaluate_audio(audio_file_path, EVAL_AUDIO)
            print(eval_res)
            res = llm_bot.chat(UPDATE_REFINE_PROMPT.format(advice=eval_res))
            texts = get_text_inside_tag(res, "speaker")
            texts = [replace_(m) for m in texts]
            prompts = get_text_inside_tag(res, "prompt")
            processor.run_batch(
                texts, speakers[i], prompts, f"conversation{i}.wav", refine_skip=True
            )
