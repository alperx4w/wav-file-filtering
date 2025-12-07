# Audio Filtering & Processing Tool

A lightweight Python command-line tool for analyzing, filtering, and cropping WAV audio files. This project was built to assist with underwater vehicle (AUV) acoustic analysis but works for any standard WAV file.

## Features

Filter Audio: Apply Lowpass, Highpass, Bandpass, and Bandstop filters.

Visual Analysis: Automatically plots Time Domain waveforms and Frequency Domain (FFT) spectrums.

Audio Cropping: Precise cutting of WAV files by start/stop seconds.
l
Format Support: Handles Mono and Stereo WAV files.

## Installation

*Clone the repository:*

git clone [https://github.com/alperx4w/audio-filtering-tool.git](https://github.com/alperx4w/audio-filtering-tool.git)

cd audio-filtering-tool

*Install dependencies:*

pip install numpy scipy matplotlib


## Usage

**1. Filtering Audio**

Use audio_filtering.py to apply filters.

**Syntax:**

python audio_filtering.py <input_file> <order> <cutoff_freq> <filter_type> [options]


## Examples:

**Lowpass filter at 1000Hz (Order 4)**

python audio_filtering.py recording.wav 4 1000 lowpass

**Highpass filter at 500Hz**

python audio_filtering.py recording.wav 4 500 highpass

**Bandpass filter between 400Hz and 800Hz**

python audio_filtering.py recording.wav 4 400 800 bandpass

**Bandstop (Notch) filter between 45Hz and 55Hz**

python audio_filtering.py recording.wav 4 45 55 bandstop


## Options:

--no-plot: Disable the popup graphs (faster).

--no-save: Disable saving the output WAV file.

-output_file "name.wav": Specify a custom output filename.

# 2. Cropping Audio

Use wav_cropper.py to trim files.

**Syntax:**

python wav_cropper.py <input> <output> --start <seconds> --stop <seconds>


## Example:

**Crop from 5.5 seconds to 10 seconds**

python wav_cropper.py long_recording.wav snippet.wav --start 5.5 --stop 10

## Dependencies

Python 3.x

NumPy

SciPy

Matplotlib
