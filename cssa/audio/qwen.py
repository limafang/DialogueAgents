from io import BytesIO
from urllib.request import urlopen
import librosa
from transformers import Qwen2AudioForConditionalGeneration, AutoProcessor
from .base import BaseAudio


class QwenAudio(BaseAudio):
    def __init__(self, model_path, system_message=None):
        self.processor = AutoProcessor.from_pretrained(model_path, device_map="auto")
        self.model = Qwen2AudioForConditionalGeneration.from_pretrained(
            model_path, device_map="auto"
        )
        if system_message is not None:
            self.conversation_history = [{"role": "system", "content": system_message}]
        else:
            self.conversation_history = []

    def evaluate_audio(self, audio_file_path, prompt):
        messages = []
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "audio", "audio_url": audio_file_path},
                    {"type": "text", "text": prompt},
                ],
            }
        )
        text = self.processor.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=False
        )
        audios = []
        for message in messages:
            if isinstance(message["content"], list):
                for ele in message["content"]:
                    if ele["type"] == "audio":
                        audios.append(
                            librosa.load(
                                ele["audio_url"],
                                sr=self.processor.feature_extractor.sampling_rate,
                            )[0]
                        )
        inputs = self.processor(
            text=text, audios=audios, return_tensors="pt", padding=True
        )
        inputs["input_ids"] = inputs["input_ids"].to("cuda")
        inputs.input_ids = inputs.input_ids.to("cuda")
        generate_ids = self.model.generate(**inputs, max_length=4096)
        generate_ids = generate_ids[:, inputs.input_ids.size(1) :]
        response = self.processor.batch_decode(
            generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]
        bot_response = response
        return bot_response
