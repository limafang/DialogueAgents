from DA.llm.openai import OpenAILLM
from DA.prompt import *
from DA.tts.cosyTTS import cosyvoice_agent
from DA.utils import get_script,get_speaker,get_text_inside_tag,read_json_file,save_json
import os
import argparse
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, required=True, help='model path')
    parser.add_argument('--output_dir', type=str, required=True, help='output file')
    parser.add_argument('--script_path', type=str, required=True, help='script path')
    args = parser.parse_args()
    
    model_path = args.model_path
    output_dir = args.output_dir
    script_path = args.script_path
    tts = cosyvoice_agent(model_path,output_dir)
    llm_bot = OpenAILLM(
        "gpt-4o",
        os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE_URL")
    )
    data = read_json_file(script_path)
    text_batches, speakers = get_script(script_path)
    speaker_labels = [] 
    wavs = []
    for i in speakers:
        current_labels = []
        current_wavs = []
        for j in i:  
            label,_,wav = get_speaker(j)
            current_labels.append(label)
            current_wavs.append(wav)
        speaker_labels.append(current_labels)
        wavs.append(current_wavs)   
    for i, script in enumerate(data["scripts"]):
        conversation = script["conversation"]
        res = llm_bot.predict(EN_REFINE_PROMPT_v2.format(text=conversation))
        print(res)
        texts = get_text_inside_tag(res, "speaker")
        prompts = get_text_inside_tag(res, "prompt")
        for j, conv in enumerate(conversation):
            conv['text'] = texts[j]
            conv['prompt'] = prompts[j]
        tts.run_batch(texts,speaker_labels[i],prompts,wavs[i],f'conversation{i}.wav')
    save_json(data,f"{output_dir}/data.json")