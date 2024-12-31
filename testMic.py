import sounddevice as sd
import numpy as np
import wave

def test_microphone():
    duration = 5  # seconds
    sample_rate = 44100

    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")

    # Save the recording
    with wave.open('test_recording.wav', 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 2 bytes for float64
        wf.setframerate(sample_rate)
        wf.writeframes((recording * 32767).astype(np.int16).tobytes())

    print("Audio saved as 'test_recording.wav'.")

test_microphone()
