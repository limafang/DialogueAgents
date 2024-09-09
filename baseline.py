from DA.tts.cosyTTS import cosyvoice_agent
from DA.utils import get_script,get_speaker
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