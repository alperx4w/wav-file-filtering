import argparse
import sys
from scipy.io import wavfile
import numpy as np

def crop_audio(input_file, start_sec, stop_sec):
    try:
        # 1. Read the file
        print(f"Reading {input_file}...")
        sample_rate, data = wavfile.read(input_file)
        
        # 2. Calculate details
        total_samples = data.shape[0]
        total_duration = total_samples / sample_rate
        print(f"  Sample Rate: {sample_rate} Hz")
        print(f"  Duration:    {total_duration:.2f} seconds")

        # 3. Validate inputs
        if start_sec < 0:
            print("Error: Start time cannot be negative.")
            return
        if stop_sec > total_duration:
            print(f"Warning: Stop time ({stop_sec}s) is longer than file. Cropping to end.")
            stop_sec = total_duration
        if start_sec >= stop_sec:
            print("Error: Start time must be smaller than stop time.")
            return

        # 4. Convert Seconds to Indices (The Math)
        #    Index = Time * SamplesPerSecond
        start_index = int(start_sec * sample_rate)
        end_index   = int(stop_sec * sample_rate)

        # 5. Slice the Numpy Array
        #    This works for both Mono (1D) and Stereo (2D)
        cropped_data = data[start_index:end_index]

        # 6. Save the new file
        output_file = f"Cropped_{input_file}_{start_sec}_{stop_sec}.wav"
        wavfile.write(output_file, sample_rate, cropped_data)
        print(f"Success! Saved {output_file} ({stop_sec - start_sec:.2f} seconds)")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Crop a WAV file by time.")
    
    # Positional arguments
    parser.add_argument("input", help="Path to input WAV file")
    
    # Flags for start and stop
    parser.add_argument("--start", type=float, default=0.0, help="Start time in seconds")
    parser.add_argument("--stop", type=float, required=True, help="Stop time in seconds")

    args = parser.parse_args()

    crop_audio(args.input,args.start, args.stop)