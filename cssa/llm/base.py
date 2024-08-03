class BaseLLM:
    def __init__(self, model_name="glm-4", system_message=None):
        self.model_name = model_name
        if system_message is not None:
            self.conversation_history = [{"role": "system", "content": system_message}]
        else:
            self.conversation_history = []

    def chat(self, prompt):
        raise NotImplementedError("Subclasses should implement this method.")

    def predict(self, prompt, context=None):
        raise NotImplementedError("Subclasses should implement this method.")
