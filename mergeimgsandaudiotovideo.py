import os

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
        #print(start)
        end = timestamps[i + 1]
        #print(end)
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

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    timestamps_file = os.path.join(folder_path, 'timestamps.txt')

    if not os.path.exists(timestamps_file):
        print("Error: timestamps.txt file not found in the specified folder.")
    else:
        timestamps = parse_timestamps(timestamps_file)
        durations = calculate_durations(timestamps)
        generate_output_file(folder_path, timestamps, durations)
        print("Image durations file generated successfully.")
