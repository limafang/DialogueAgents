from zhipuai import ZhipuAI
from base import BaseLLM

# 填写您自己的APIKey
client = ZhipuAI(api_key="7c172280522ff372cba10aeb1c67cbd2.6YOBziXCNFnAx1hL")


class ZhipuLLM(BaseLLM):
    def chat(self, prompt):
        self.conversation_history.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
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
        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0,
            stream=False,
        )
        bot_response = response.choices[0].message.content
        return bot_response
