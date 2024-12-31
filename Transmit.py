# This is the main python file

import numpy as np
import sounddevice as sd

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_sound(binary_data, duration_per_bit=0.3):
    sample_rate = 44100
    sound = []

    # Frequencies for 1 and 0
    freq_1 = 1000  # Frequency for '1' (1 kHz)
    freq_0 = 500   # Frequency for '0' (500 Hz)
    
    # Start and Stop tones
    start_freq = 2000  # Start tone (2 kHz)
    stop_freq = 2500   # Stop tone (2.5 kHz)
    
    # Add start tone
    t_start = np.linspace(0, duration_per_bit, int(sample_rate * duration_per_bit), False)
    start_tone = 0.5 * np.sin(2 * np.pi * start_freq * t_start)
    sound.extend(start_tone)

    for bit in binary_data:
        frequency = freq_1 if bit == '1' else freq_0
        t = np.linspace(0, duration_per_bit, int(sample_rate * duration_per_bit), False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        sound.extend(wave)

    # Add stop tone
    t_stop = np.linspace(0, duration_per_bit, int(sample_rate * duration_per_bit), False)
    stop_tone = 0.5 * np.sin(2 * np.pi * stop_freq * t_stop)
    sound.extend(stop_tone)

    return np.array(sound)

text = "Hello"
binary_data = text_to_binary(text)
sound_wave = binary_to_sound(binary_data)

# Play the sound
sd.play(sound_wave, samplerate=44100)
sd.wait()
