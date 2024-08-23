class BaseLLM:
    def __init__(self, model_name="", system_message=None, api_key=None, base_url=None):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        if system_message is not None:
            self.conversation_history = [{"role": "system", "content": system_message}]
        else:
            self.conversation_history = []

    def chat(self, prompt):
        raise NotImplementedError("Subclasses should implement this method.")

    def predict(self, prompt, context=None):
        raise NotImplementedError("Subclasses should implement this method.")
