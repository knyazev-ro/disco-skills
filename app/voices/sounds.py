import soundfile as sf
import sounddevice as sd

def sound_rec(path: str):
    audio, sample_rate = sf.read(path)
    sd.play(audio, sample_rate)
    sd.wait()

def sound_start():
    sound_rec("resources/thought-complete-01.wav")

def sound_dialog_answer():
    sound_rec("resources/short-skillsounds-PSY-tr.wav")


