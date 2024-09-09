from cssa.llm.openai import OpenAILLM
from cssa.prompt import *
from cssa.tts.cosyTTS import cosyvoice_agent
from cssa.utils import get_script, replace_,get_speaker,get_text_inside_tag,read_json_file,save_json
import os
from cssa.audio.qwen import QwenAudio
import argparse
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, required=True, help='model path')
    parser.add_argument('--output_dir', type=str, required=True, help='output file')
    parser.add_argument('--script_path', type=str, required=True, help='script path')
    parser.add_argument('--max_loop', type=int, required=True, default=1,help='max loop')
    args = parser.parse_args()
    
    model_path = args.model_path
    output_dir = args.output_dir
    script_path = args.script_path
    max_loop = args.max_loop
    
    tts = cosyvoice_agent(model_path,output_dir)
    llm_bot = OpenAILLM(
        "gpt-4o",
        os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE_URL")
    )
    data = read_json_file(script_path)
    text_batches, speakers = get_script(script_path)
    audio_bot = QwenAudio("your qwen model path")
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
        llm_bot.clear_history()
        conversation = script["conversation"]
        res = llm_bot.chat(EN_REFINE_PROMPT_v2.format(text=conversation))
        texts = get_text_inside_tag(res, "speaker")
        prompts = get_text_inside_tag(res, "prompt")
        tts.run_batch(texts,speaker_labels[i],prompts,wavs[i],f'conversation{i}.wav')
        audio_file_path = output_dir + f"/conversation{i}/" + f"conversation{i}.wav"
        for j in range(max_loop):
            print(audio_file_path)
            eval_res = audio_bot.evaluate_audio(audio_file_path, EVAL_AUDIO)
            print(eval_res)
            res = llm_bot.chat(UPDATE_REFINE_PROMPT.format(advice=eval_res))
            print(res)
            texts = get_text_inside_tag(res, "speaker")
            prompts = get_text_inside_tag(res, "prompt")
            for j, conv in enumerate(conversation):
                conv['text'] = texts[j]
                conv['prompt'] = prompts[j]
            tts.run_batch(texts,speaker_labels[i],prompts,wavs[i],f'conversation{i}.wav')
    save_json(data,f"{output_dir}/data.json")