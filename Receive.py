import numpy as np
import sounddevice as sd
import scipy.signal as signal
import wave

# Frequency definitions
freq_1 = 1000  # Frequency for '1' (1 kHz)
freq_0 = 500   # Frequency for '0' (500 Hz)
start_freq = 2000  # Start tone (2 kHz)
stop_freq = 2500   # Stop tone (2.5 kHz)

# Parameters
sample_rate = 44100  # Sample rate
duration_per_bit = 0.3  # Duration of each bit in seconds
threshold = 0.1  # Threshold for detecting tones

def record_audio(duration):
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
    sd.wait()  # Wait until recording is finished
    return recording.flatten()

def detect_tone(signal_data):
    # Perform FFT
    freqs, times, Sxx = signal.spectrogram(signal_data, fs=sample_rate)
    avg_power = np.mean(Sxx, axis=1)
    
    detected_bits = []
    
    for index, power in enumerate(avg_power):
        if power > threshold:
            freq_detected = freqs[index]
            if start_freq - 50 < freq_detected < start_freq + 50:
                detected_bits.append('S')  # Start signal
            elif stop_freq - 50 < freq_detected < stop_freq + 50:
                detected_bits.append('E')  # End signal
            elif freq_1 - 50 < freq_detected < freq_1 + 50:
                detected_bits.append('1')
            elif freq_0 - 50 < freq_detected < freq_0 + 50:
                detected_bits.append('0')

    return detected_bits

def decode_message(detected_bits):
    binary_data = ''
    for bit in detected_bits:
        if bit == '1' or bit == '0':
            binary_data += bit
        elif bit == 'E':  # Stop signal detected
            break
    
    # Convert binary data to text
    decoded_text = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i + 8]
        if len(byte) == 8:
            decoded_text += chr(int(byte, 2))
    
    return decoded_text

def main():
    duration = 10  # Adjust duration based on expected transmission time
    audio_data = record_audio(duration)
    
    detected_bits = detect_tone(audio_data)
    
    if 'S' in detected_bits:
        # Only decode if start signal was detected
        decoded_text = decode_message(detected_bits)
        print("Decoded Message:", decoded_text)
        
        # Save to file
        with open("decoded_message.txt", "w") as f:
            f.write(decoded_text)
    else:
        print("No valid start signal detected.")

if __name__ == "__main__":
    main()
