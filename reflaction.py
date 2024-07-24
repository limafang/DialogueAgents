from cssa.prompt import *
from cssa.llm.zhipu import zhipullm
from cssa.prompt import *
from cssa.utils import get_text_inside_tag
from cssa.agent.tts import ChatTTS_agent
from cssa.utils import get_script, read_json_file, replace_
from cssa.llm.qwen_audio import AudioRefinementBot

if __name__ == "__main__":
    model_path = "/data/xli/speech-agent/ChatTTS/asset/speaker_emb"
    output_dir = "llm_refine_outputs/"
    max_loop = 3
    script_path = "example_data.json"
    processor = ChatTTS_agent(model_path, output_dir)
    llm_bot = zhipullm("glm-4")
    audio_bot = AudioRefinementBot("qwen-audio-turbo")
    text_batches, speakers = get_script(script_path)
    data = read_json_file(script_path)
    for i, data in enumerate(data["scripts"]):
        res = llm_bot.predict(CHINESE_REFINE_PROMPT.format(text=data["conversation"]))
        texts = get_text_inside_tag(res, "speaker")
        prompts = get_text_inside_tag(res, "prompt")
        processor.run_batch(
            texts, speakers[i], prompts, f"conversation{i}.wav", refine_skip=True
        )
        res = audio_bot.evaluate_audio(output_dir + f"conversation{i}.wav", EVAL_AUDIO)
