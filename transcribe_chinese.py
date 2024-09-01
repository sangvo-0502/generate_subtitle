import os
import subprocess
import time
import json
import shutil

import argparse
# from tqdm import tqdm
import threading
import sys

def get_video_duration(file_path):
    try:
        probe = ffmpeg.probe(file_path, v='error', s='hd480', select_streams='v:0', show_entries='stream=duration', format='json')
        duration = float(probe['streams'][0]['duration'])
        return duration
    except Exception as e:
        print(f"Error retrieving duration for {file_path}: {e}")
        return None

def convert_video_to_mp3(video_path, output_folder):
    """
    Converts a video file to mp3 format.

    Args:
        video_path (str): Path to the video file.
        output_folder (str): Path to the folder where the mp3 file will be saved.

    Returns:
        str: Path to the converted mp3 file.
    """
    video_filename = os.path.basename(video_path)
    mp3_filename = os.path.splitext(video_filename)[0] + '.mp3'
    mp3_path = os.path.join(output_folder, mp3_filename)

    #### remove file if exist
    if os.path.exists(mp3_path):
        os.remove(mp3_path)

    command = f'ffmpeg -i "{video_path}" -q:a 0 -map a "{mp3_path}"'
    subprocess.run(command, shell=True, check=True)

    return mp3_path


def stopwatch(start_time, stop_event):
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        sys.stdout.write(f"\rElapsed time: {int(minutes):02}:{int(seconds):02} minutes")
        sys.stdout.flush()
        time.sleep(1)


def transcribe_audio(audio_path, json_output_folder, language, batch_size):
    # batch_size = initial_batch_size
    success = False

    audio_filename = os.path.basename(audio_path)
    json_filename = os.path.splitext(audio_filename)[0] + '.json'
    json_path = os.path.join(json_output_folder, json_filename)

    while not success and batch_size > 0:
        try:
            # Define the command
            command = f'insanely-fast-whisper --device-id mps --model-name openai/whisper-large-v2 --language "{language}" --batch-size "{batch_size}" --transcript-path "{json_path}" --file-name "{audio_path}"'

            print(f">>>>>>Transcription of {audio_path}")
            print('\n')

            start_time = time.time()
            stop_event = threading.Event()
            stopwatch_thread = threading.Thread(target=stopwatch, args=(start_time, stop_event))
            stopwatch_thread.start()

            # Run the command and capture the output
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            for line in process.stdout:
                if "CUDA out of memory" in line or "out of memory" in line:
                    raise MemoryError("Out of memory")

            process.stdout.close()
            process.wait()

            stop_event.set()  # Signal the stopwatch thread to stop
            stopwatch_thread.join()  # Wait for the stopwatch thread to finish

            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command)

            success = True

        except (subprocess.CalledProcessError, MemoryError) as e:
            print('\n')
            print(f"Error encountered: {e}. Reducing batch size to {batch_size - 4 }")
            batch_size = batch_size - 4
            if batch_size == 0:
                raise RuntimeError("Unable to transcribe file due to repeated memory errors.")

    return json_path


#####################################
# Function to read the JSON file
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Function to convert JSON data to SRT format
def convert_to_srt(data):
    srt_lines = []
    index = 1

    for chunk in data.get('chunks', []):
        timestamps = chunk.get('timestamp', [None, None])
        text = chunk.get('text', '')

        start_time = timestamps[0]
        end_time = timestamps[1]

        # Check if start_time and end_time are valid
        if start_time is None or end_time is None:
            print(f"Skipping chunk with invalid timestamps: {chunk}")
            continue

        # Convert seconds to SRT timestamp format (HH:MM:SS,MS)
        start_time_srt = format_time(start_time)
        end_time_srt = format_time(end_time)

        # Append index, timestamps, and text to SRT lines
        srt_lines.append(f"{index}")
        srt_lines.append(f"{start_time_srt} --> {end_time_srt}")
        srt_lines.append(text)
        srt_lines.append("")  # Blank line to separate entries

        index += 1

    return "\n".join(srt_lines)

# Function to format time in seconds to SRT format
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Main function for json to srt
def convert_json_to_srt(json_path, output_srt):

    # Read JSON data
    data = read_json_file(json_path)

    json_filename = os.path.basename(json_path)
    srt_filename = os.path.splitext(json_filename)[0] + '.srt'
    srt_path = os.path.join(output_srt, srt_filename)

    # Convert JSON to SRT format
    srt_content = convert_to_srt(data)

    # Write to SRT file
    with open(srt_path, 'w', encoding='utf-8') as file:
        file.write(srt_content)

    print(f">>>>Conversion complete. SRT file saved as {srt_path}")

#####################################


def process_videos_folder(videos_folder, output_folder, json_output_folder, srt_output_folder, language, batch_size):
    """
    Converts all video files in a folder to mp3, transcribes them, and saves the transcription to JSON files.

    Args:
        videos_folder (str): Path to the folder containing video files.
        output_folder (str): Path to the folder where mp3 files will be saved.
        json_output_folder (str): Path to the folder where JSON files will be saved.
    """
    video_files = [f for f in os.listdir(videos_folder) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    total_files = len(video_files)

    # command_spec = f'export PYTORCH_ENABLE_MPS_FALLBACK=1'
    # subprocess.Popen(command_spec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    start_time_total = time.time()

    for index, filename in enumerate(video_files):
        video_path = os.path.join(videos_folder, filename)
        print("\n" * 2)
        print("=" * 100)
        print(f"Processing file {index + 1}/{total_files}: {filename}")
        print("=" * 100)

        print("\n" * 2)
        print(">>>>>Converting video to audio file.....................")
        mp3_path = convert_video_to_mp3(video_path, output_folder)

        print(">>>>>Convert video to audio file successfully!")
        print("\n" * 2)

        # duration = get_video_duration(video_path)
        # if duration:
        # print(f"Video Duration: {(duration / 60):.2f} minutes")
        # else:
            # print(f"Skipping due to duration retrieval failure.")
            # continue

        # print("\n" * 2)
        print(f'>>>>>>Transcribing video using "{language}" .....................')

        print("\n" * 2)
        json_file = transcribe_audio(mp3_path, json_output_folder, language, batch_size)

        print("\n" * 2)
        print(">>>>>Transcribe video successfully!")

        print("\n" * 2)
        convert_json_to_srt(json_file, srt_output_folder)

        print("\n" * 2)
        print(">>>>>Json to SRT successfully!")

        elapsed_time = time.time() - start_time_total
        percentage = ((index + 1) / total_files) * 100

        print("\n" * 2)
        print("=" * 100)
        print(f">>>>Completed {filename}: Total elapsed Time: {(elapsed_time/60):.2f} minutes, Progress: {percentage:.2f}%")
        print("=" * 100)

        print("\n" * 5)

        # move the MP4 file after transcription
        # os.remove(video_path)

        # Move the MP4 file to the archive folder after transcription
        # if not os.path.exists(video_path):
        #     os.makedirs(video_path)
        # shutil.move(mp4_file, os.path.join(archive_folder, file_name))

        # print(">>>>Removed video!")
        # print("\n" * 2)
# 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


if __name__ == "__main__":
    videos_folder = "/Users/administrator/Documents/test/video/"
    output_folder = "/Users/administrator/Documents/test/audio/"
    json_output_folder = "/Users/administrator/Documents/test/json/"
    srt_output_folder =  "/Users/administrator/Documents/test/srt/"
    batch_size = 12
    language = "Chinese"
    # language = "Vietnamese"
    # language = "Japanese"



    # Ensure the output folders exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(json_output_folder, exist_ok=True)

    process_videos_folder(videos_folder, output_folder, json_output_folder, srt_output_folder, language, batch_size)
