import dashscope
from dashscope import MultiModalConversation
from base import BaseAudio

dashscope.api_key = "sk-2250e5f690cd47afb415002c9164f0f9"


class QwenAudio(BaseAudio):
    def __init__(self, model_name, system_message=None):
        self.model_name = model_name
        if system_message is not None:
            self.conversation_history = [{"role": "system", "content": system_message}]
        else:
            self.conversation_history = []

    def evaluate_audio(self, audio_file_path, prompt):
        self.conversation_history.append(
            {"role": "user", "content": [{"audio": audio_file_path}, {"text": prompt}]}
        )
        response = MultiModalConversation.call(
            model=self.model_name,
            messages=self.conversation_history,
            temperature=0,
            stream=False,
        )
        bot_response = response
        return bot_response
