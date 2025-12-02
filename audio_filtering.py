import scipy
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse


def fft(signal,rate):
    n = len(signal)
    yf = 2.0/n*np.abs(scipy.fft.rfft(signal))
    xf = scipy.fft.rfftfreq(n,1/rate)
    return xf, yf


def audio_filter(input_file,order,cutt_freq,filter_type = "lowpass",save_audio = True,plot_result=True,channel=0,output_file = ""):
    try:

        if filter_type not in ["lowpass","highpass","bandpass","bandstop"]:
            print(f"filter type {filter_type} is not supported")
            return
        if (filter_type == "bandpass" or filter_type == "bandstop") and (len(cutt_freq) != 2):
            print(f"{filter_type} filter must contain two frequencies")
            return
        if (order < 0):
            print("Order must be a positive integer")
            return
        if not isinstance(order, int):
            print("Order must be a positive integer")
            return

        samplerate, wav_data = wavfile.read(input_file)
        number_of_channels = wav_data.shape[1]

        if channel > number_of_channels-1 or channel < 0:
            print("Channel out of range")
            return
        for f in cutt_freq:
            if f >= samplerate/2:
                print(f"Error: Frequency {f} Hz is too high. Max allowed is {samplerate/2-1} Hz.")
                return
            if f <= 0:
                print(f"Error: Frequency {f} Hz must be positive.")
                return

        if len(cutt_freq) == 1:
            final_cutt = cutt_freq[0]
        else:
            final_cutt = cutt_freq

        length = wav_data.shape[0]/samplerate
        time = np.linspace(0., length, wav_data.shape[0])


        print(f"Number of channels: {number_of_channels}")
        print(f"Sample Rate: {samplerate} Hz")
        print(f"wav_data.shape[0]: {wav_data.shape[0]} Hz")
        print(f"Max Cutoff freq: {samplerate/2}")
        print(f"Audio length: {length} seconds")

        ndata = wav_data[:,0] / np.max(np.abs(wav_data[:,channel]))
        data = (ndata * 32767).astype(np.int16)

        sos = scipy.signal.butter(order, final_cutt, filter_type, fs=samplerate, output='sos')
        filtered = scipy.signal.sosfilt(sos, data)

        normalized = filtered / np.max(np.abs(filtered))
        filtered_audio = (normalized * 32767).astype(np.int16)

        data_xfft, data_yfft = fft(data,samplerate)
        filtered_xfft, filtered_yfft = fft(filtered_audio,samplerate)

        if (plot_result == True):
            plt.figure("Audio Lowpass Filter",figsize=(15, 10))
            #raw audio
            # plt.subplot(2,1,1)
            plt.subplot(2,2,1)
            plt.grid(True)
            plt.plot(time,data,label = "Raw data")
            plt.legend()
            plt.xlabel("Time [s]")
            plt.ylabel("Amplitude")
            #filtered audio
            plt.subplot(2,2,3)
            plt.grid(True)
            plt.plot(time,filtered_audio,label = "Saved Audio")
            plt.xlabel("Time [s]")
            plt.ylabel("Amplitude")
            plt.legend()


            #fft raw
            # plt.subplot(2,1,2)
            plt.subplot(2,2,2)
            plt.grid(True)
            plt.plot(data_xfft,data_yfft,label = "FFT Raw data",color = 'green')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("Amplitude")
            for f in cutt_freq:
                plt.axvline(f, color='red', linestyle='--', label=f"Cutoff {f}Hz")
            plt.legend()

            #fft filtered audio
            plt.subplot(2,2,4)
            plt.grid(True)
            plt.plot(filtered_xfft,filtered_yfft,label = "FFT Filtered data",color ='green')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("Amplitude")
            for f in cutt_freq:
                plt.axvline(f, color='red', linestyle='--', label=f"Cutoff {f}Hz")
            plt.legend()


            plt.show()


        if (save_audio == True):
            if output_file == "":
                output_file = f"filtered_{input_file}_{filter_type}_{order}_{cutt_freq}Hz"

            wavfile.write(output_file, samplerate, filtered_audio)
            print(f"Saved '{output_file}'")


    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Filter .wav file")
    
    parser.add_argument("input",type=str, help="Path to input WAV file")
    parser.add_argument("order",type=int,help="Order of the filter")
    parser.add_argument("cutt_freq", type=float, nargs='+', help="Cutoff frequency. Provide 1 value for lowpass/highpass, or 2 values (min max) for bandpass/bandstop.")
    parser.add_argument("filter_type",type=str,default="lowpass",help="Filter type. ""lowpass"", ""highpass"", ""bandpass"", ""bandstop"" filters are supported.")
    parser.add_argument("--no-plot", action="store_false", dest="plot", help="Disable plotting (Enabled by default)")
    parser.add_argument("--no-save", action="store_false", dest="save", help="Disable saving file (Enabled by default)")
    parser.add_argument("-output_file",type=str,default="",help="The name of the output_file (if -save is True), Automatically genarated if is not specified")
    

    args = parser.parse_args()

    audio_filter(args.input,args.order, args.cutt_freq,args.filter_type,plot_result=args.plot,save_audio=args.save,output_file=args.output_file)