from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from audio_filtering import *

# samplerate, data = wavfile.read('Empire_Of_The_Sun_-_We_Are_The_People_Radio_Edit_Empire_Of_The_Sun_(mp3.pm).wav')
# samplerate, data = wavfile.read('filtered_result.wav')
# length = data.shape[0]/samplerate
# time = np.linspace(0., length, data.shape[0])

order = 10  
cutt_freq = 100

time_limit= 1
rate = 1000

t = np.linspace(0, time_limit, rate*time_limit,False)
wave = np.sin(90*2*np.pi*t) + np.sin(120*2*np.pi*t)
xf,yf = fft(wave,rate)

sos = scipy.signal.butter(order, cutt_freq, 'lowpass', fs=rate, output='sos')
filtered = scipy.signal.sosfilt(sos, wave)
filtered_xf,filtered_yf = fft(filtered,rate)

plt.figure("Audio Lowpass Filter",figsize=(15, 10))
#raw
plt.subplot(2,2,1)
plt.grid(True)
plt.plot(t,wave,label = "Raw data")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
#fft raw
plt.subplot(2,2,2)
plt.grid(True)
plt.plot(xf,yf,label = "FFT Raw data")
plt.legend()
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude")
plt.axvline(cutt_freq, color='red', linestyle='--', label=f"Cutoff {cutt_freq}Hz")
# plt.axvline(cutt_freq[0], color='red', linestyle='--', label=f"Cutoff {cutt_freq[1]}Hz")
# plt.axvline(cutt_freq[1], color='red', linestyle='--', label=f"Cutoff {cutt_freq[1]}Hz")

#filtered audio
plt.subplot(2,2,3)
plt.grid(True)
plt.plot(t,filtered,label = "Saved Audio")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
#fft filtered audio
plt.subplot(2,2,4)
plt.grid(True)
plt.plot(filtered_xf,filtered_yf,label = "FFT Filtered data")
plt.legend()
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude")
plt.axvline(cutt_freq, color='red', linestyle='--', label=f"Cutoff {cutt_freq}Hz")
# plt.axvline(cutt_freq[0], color='red', linestyle='--', label=f"Cutoff {cutt_freq[1]}Hz")
# plt.axvline(cutt_freq[1], color='red', linestyle='--', label=f"Cutoff {cutt_freq[1]}Hz")

plt.show()


saved_wave = (wave/max(np.abs(wave))).astype(np.float32)
saved_filtered_wave = (filtered/max(np.abs(filtered))).astype(np.float32)
wavfile.write("test_pure_wave.wav", rate, saved_wave)
wavfile.write("test_filtered_pure_wave.wav", rate, saved_filtered_wave)

