from cssa.tts.cosyTTS import cosyvoice_agent
from cssa.utils import get_script, replace_,get_speaker
import os
import argparse

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="输入必要的参数")

    parser.add_argument('--model_path', type=str, required=True, help='模型路径')
    parser.add_argument('--output_dir', type=str, required=True, help='输出目录')
    parser.add_argument('--script_path', type=str, required=True, help='脚本文件路径')

    args = parser.parse_args()
    model_path = args.model_path
    output_dir = args.output_dir
    script_path = args.script_path
    
    tts = cosyvoice_agent(model_path,output_dir)
    text_batches, speakers = get_script(script_path)
    
    speaker_labels = [] 
    prompts = [] 
    wavs = []   
    
    for i in speakers:
        current_labels = []
        current_prompts = []
        current_wavs = []
        for j in i:  
            label,_,wav = get_speaker(j)
            current_labels.append(label)
            current_prompts.append("")
            current_wavs.append(wav)
        speaker_labels.append(current_labels)
        prompts.append(current_prompts)
        wavs.append(current_wavs)   
    for i, data in enumerate(text_batches):
        tts.run_batch(data,speaker_labels[i],prompts[i],wavs[i],f'conversation{i}.wav')