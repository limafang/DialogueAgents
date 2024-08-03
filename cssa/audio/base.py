class BaseAudio:
    def __init__(self, model_name, system_message=None):
        self.model_name = model_name
        if system_message is not None:
            self.conversation_history = [{"role": "system", "content": system_message}]
        else:
            self.conversation_history = []

    def evaluate_audio(self, audio_file_path, prompt):
        raise NotImplementedError("Subclasses should implement this method.")
