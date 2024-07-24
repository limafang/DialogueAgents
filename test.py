from cssa.llm.qwen_audio import AudioRefinementBot
from cssa.prompt import *

audio_bot = AudioRefinementBot("qwen-audio-turbo")
audio_path = "baseline_outputs/conversation0.wav"
res = audio_bot.evaluate_audio(audio_path, EVAL_AUDIO)
print(res)
