from .base import BaseLLM
from openai import OpenAI


class OpenAILLM(BaseLLM):
    def __init__(self, model_name="", system_message=None, api_key=None, base_url=None):
        super(OpenAILLM, self).__init__(model_name, system_message, api_key, base_url)
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(self, prompt):
        self.conversation_history.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.conversation_history,
            temperature=0,
            stream=False,
        )
        bot_response = response.choices[0].message.content
        return bot_response

    def predict(self, prompt, context=None):
        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0,
            stream=False,
        )
        bot_response = response.choices[0].message.content
        return bot_response

    def clear_history(self):
        self.conversation_history = []
