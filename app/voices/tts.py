import torch
import re

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tts_model, _ = torch.hub.load(
    repo_or_dir="snakers4/silero-models",
    model="silero_tts",
    language="ru",
    speaker="v5_6_ru",
)

tts_model.to(device)

def synthesize(model, text, speaker="eugene", sample_rate=24000):
    audio = model.apply_tts(
        text=text,
        speaker=speaker,
        sample_rate=sample_rate,
    )
    return audio
