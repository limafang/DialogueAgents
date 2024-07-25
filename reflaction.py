from cssa.prompt import *
from cssa.llm.zhipu import zhipullm
from cssa.prompt import *
from cssa.utils import get_text_inside_tag
from cssa.agent.tts import ChatTTS_agent
from cssa.utils import get_script, read_json_file, replace_
from cssa.llm.qwen_audio import AudioRefinementBot

if __name__ == "__main__":
    model_path = "/data/xli/speech-agent/ChatTTS/asset/speaker_emb"
    output_dir = "reflaction_output/"
    max_loop = 3
    script_path = "example_data.json"
    processor = ChatTTS_agent(model_path, output_dir)
    llm_bot = zhipullm("glm-4")
    audio_bot = AudioRefinementBot("qwen-audio-turbo")
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
