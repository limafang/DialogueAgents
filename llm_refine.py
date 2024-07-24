from cssa.prompt import *
from cssa.llm.zhipu import zhipullm
from cssa.prompt import *
from cssa.utils import get_text_inside_tag
from cssa.agent.tts import ChatTTS_agent
from cssa.utils import get_script, read_json_file


if __name__ == "__main__":
    model_path = "/data/xli/speech-agent/ChatTTS/asset/speaker_emb"
    output_dir = "baseline_outputs"
    script_path = "example_data.json"
    llm_bot = zhipullm("glm-4")
    data = read_json_file(script_path)
    for i in data["scripts"]:
        res = llm_bot.predict(CHINESE_REFINE_PROMPT.format(text=i["conversation"]))
        print(res)
        text = get_text_inside_tag(res, "speaker")
        print(text)
        prompt = get_text_inside_tag(res, "prompt")
        print(prompt)
    # text_batches, speakers = get_script(script_path)

    # processor = ChatTTS_agent(model_path, output_dir)
    # for i, data in enumerate(text_batches):
    #     print(data)
    #     prompts_len = len(data)
    #     prompts = ["[oral_2][laugh_0][break_6]" for _ in range(prompts_len)]
    #     print(prompts)
    #     processor.run_batch(data, speakers[i], prompts, f"conversation{i}.wav")
