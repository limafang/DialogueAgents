from cssa.agent.tts import ChatTTS_agent
from cssa.utils import get_script


if __name__ == "__main__":
    model_path = "/data/xli/speech-agent/ChatTTS/asset/speaker_emb"
    output_dir = "baseline_outputs"
    script_path = "example_data.json"
    text_batches, speakers = get_script(script_path)
    processor = ChatTTS_agent(model_path, output_dir)

    for i, data in enumerate(text_batches):
        print(data)
        prompts_len = len(data)
        prompts = ["[oral_2][laugh_0][break_6]" for _ in range(prompts_len)]
        print(prompts)
        processor.run_batch(data, speakers[i], prompts, f"conversation{i}.wav")
