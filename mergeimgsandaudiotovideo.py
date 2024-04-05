import os
import subprocess
import datetime
import glob
from PIL import Image

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

def generate_output_file(folder_path, timestamps, durations):
    output_file_path = os.path.join(folder_path, 'image_durations.txt')
    with open(output_file_path, 'w') as file:
        for i in range(len(timestamps) - 1):
            file_path = os.path.join(folder_path, str(i+1) + ".jpg").replace('\\', '/')
            file.write(f'file {file_path}\n')
            file.write(f'duration {durations[i]}\n')

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height

if __name__ == "__main__":
    #folder_path = input("Enter the folder path: ")
    folder_path = "C:/Users/MSadm/Documents/Sadman/code/SIDEPROJECTS/mergeimgsandaudiotovideo/tests/imgs"
    audio_path = "C:/Users/MSadm/Documents/Sadman/code/SIDEPROJECTS/mergeimgsandaudiotovideo/tests/imgs/a.m4a"
    timestamps_file = os.path.join(folder_path, 'timestamps.txt')

    if not os.path.exists(timestamps_file):
        print("Error: timestamps.txt file not found in the specified folder.")
    else:
        timestamps = parse_timestamps(timestamps_file)
        durations = calculate_durations(timestamps)
        generate_output_file(folder_path, timestamps, durations)

        print("Image durations file generated successfully.")

        # Run ffmpeg --help
        output_file = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_output.mp4"
        # Get the path of the first image in the folder
        image_path = glob.glob(os.path.join(folder_path, '*.jpg'))[0]

        # Get the dimensions of the first image
        image_dimensions = get_image_dimensions(image_path)

        # Scale the video to match the dimensions of the first image
        scale = f'scale={image_dimensions[0]}:{image_dimensions[1]}'

        # Run ffmpeg command
        subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", os.path.join(folder_path, "image_durations.txt"), "-i", audio_path, "-vf", f"{scale},format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-c:a", "aac", "-b:a", "192k", "-shortest", output_file])
