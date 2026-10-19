from app.voices.rvc import rvc
from app.voices.tts import tts_model, synthesize
import soundfile as sf
import sounddevice as sd
from rvc_python.modules.vc.pipeline import cache_harvest_f0
from app.voices.sounds import sound_start, sound_dialog_answer

def make_tts(text: str):
    audio = synthesize(tts_model, text, "eugene", 48000)

    sf.write(
        "input.wav",
        audio.cpu().numpy(),
        36000,
    )
    
def make_rvc():
    cache_harvest_f0.cache_clear()
    rvc.infer_file("input.wav", "output.wav")


def narrate(text: str):
    make_tts(text)
    make_rvc()
    sound_dialog_answer()
    audio, sample_rate = sf.read("output.wav")
    sd.play(audio, sample_rate)
    sd.wait()
    
# narrate(" Закон — это бумага. Ты же — мясо, кости и мышцы. Если кто-то решит с тобой не согласиться, никакие параграфы не помогут, если ты не сможешь прижать его к стене и удержать там. Перестань орать, просто покажи им, что ты способен сломать их сопротивление.  Закон — это бумага. Ты же — мясо, кости и мышцы. Если кто-то решит с тобой не согласиться, никакие параграфы не помогут, если ты не сможешь прижать его к стене и удержать там. Перестань орать, просто покажи им, что ты способен сломать их сопротивление.")