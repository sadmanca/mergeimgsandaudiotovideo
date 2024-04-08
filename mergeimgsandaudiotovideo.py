import os
import subprocess
import datetime
import glob
from PIL import Image
import argparse

def parse_timestamps(timestamps_file):
    timestamps = []
    with open(timestamps_file, 'r') as file:
        for line in file:
            timestamp = line.strip()
            if timestamp:
                timestamps.append(timestamp)
    return timestamps

def calculate_durations(timestamps):
    durations = []
    for i in range(len(timestamps) - 1):
        start = timestamps[i]
        end = timestamps[i + 1]
        duration = calculate_duration(start, end)
        durations.append(duration)
    return durations

def calculate_duration(start, end):
    start_time = convert_to_seconds(start)
    end_time = convert_to_seconds(end)
    return end_time - start_time

def convert_to_seconds(timestamp):
    parts = timestamp.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    return hours * 3600 + minutes * 60 + seconds

def generate_output_file(folder_path, durations):
    output_file_path = os.path.join(folder_path, 'image_durations.txt')
    with open(output_file_path, 'w') as file:
        files = os.listdir(folder_path)
        files.sort()  # Sort the list of files alphabetically
        i = 0  # Start index at 0
        for filename in files:
            if filename.endswith('.jpg'):
                file_path = os.path.join(folder_path, filename).replace('\\', '/')
                file.write(f'file \'{file_path}\'\n')
                file.write(f'duration {durations[i]}\n')
                i += 1  # Only increment index if processing a .jpg file

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height
    
def round_even(number):
    return number + 1 if number % 2 == 1 else number

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--i", help="folder path for imgs", type=str, required=True)
    parser.add_argument("--a", help="file path for audio", type=str, required=True)
    args = parser.parse_args()
    
    folder_path = args.i
    audio_path = args.a
    
    if folder_path == None:
        folder_path = input("Enter the folder path: ")
    if audio_path == None:
        audio_path = input("Enter the audio file path: ")
    timestamps_file = os.path.join(folder_path, 'timestamps.txt')

    if not os.path.exists(timestamps_file):
        print("Error: timestamps.txt file not found in the specified folder.")
    else:
        timestamps = parse_timestamps(timestamps_file)
        durations = calculate_durations(timestamps)
        generate_output_file(folder_path, durations)

        print("Image durations file generated successfully.")

        folder_name = os.path.basename(folder_path)
        folder_name = ''.join(c for c in folder_name if c.isalnum())  # Strip away non-alphanumeric characters
        # Extract the last two characters of the folder name
        suffix = folder_name[-2:]
        # Construct the output file name
        output_file = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{suffix}_output.mp4"
        
        # Get the path of the first image in the folder
        image_path = glob.glob(os.path.join(folder_path, '*.jpg'))[0]

        # Get the dimensions of the first image
        image_dimensions = get_image_dimensions(image_path)

        # If the image dimensions are larger than 720p, scale them down while preserving aspect ratio
        if image_dimensions[0] > 1280 or image_dimensions[1] > 720:
            # Calculate the new dimensions while maintaining the aspect ratio
            aspect_ratio = image_dimensions[0] / image_dimensions[1]
            new_width = min(image_dimensions[0], 1280)  # Set maximum width to 1280 (720p)
            new_height = round(new_width / aspect_ratio)
        
            # Round dimensions to even numbers
            rounded_width = round_even(new_width)
            rounded_height = round_even(new_height)
        else:
            # If dimensions are smaller or equal to 720p, keep them as they are
            rounded_width = round_even(image_dimensions[0])
            rounded_height = round_even(image_dimensions[1])
            
        # Scale the video to match the rounded dimensions
        scale = f'scale={rounded_width}:{rounded_height}'
        
        # Run ffmpeg command
        ffmpeg_command = [
            "ffmpeg", "-f", "concat", "-safe", "0", "-i",
            os.path.join(folder_path, "image_durations.txt"), "-i", audio_path,
            "-vf", f"{scale},format=yuv420p",
            "-r", "10",  # Set frame rate to 10 fps
            "-c:v", "libx264", "-preset", "fast", "-crf", "28",  # Faster preset and higher CRF
            "-c:a", "aac", "-b:a", "192k",  # Retain original audio bitrate
            "-shortest", output_file
        ]
        
        subprocess.run(ffmpeg_command)
