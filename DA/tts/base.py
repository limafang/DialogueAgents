import os
import torch
import torchaudio
import lzma
import numpy as np
import pybase16384 as b14
import ChatTTS
import subprocess


class BaseTTS:
    def __init__(self, model_path, output_dir, device="gpu"):
        self.chat = ChatTTS.Chat()
        self.chat.load(compile=True)
        self.model_path = model_path
        self.output_dir = output_dir
        self.temp_dir = os.path.join(output_dir, "temp")
        self.concat_file = os.path.join(output_dir, "concat.txt")
        self.device = device
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

    def generate_wavs(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def save_wav(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def save_wavs(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def concatenate_wavs(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def run_batch(
        self,
        text_batches: list,
        speaker_names: list,
        prompts: list,
        output_filename: str,
        refine_skip: bool,
    ):
        """
        Placeholder method to run batch processing.
        Subclasses should implement this method.
        """
        raise NotImplementedError("Subclasses should implement this method.")
