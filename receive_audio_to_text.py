import subprocess
import datetime
import os
import io
import whisper

# Configuration
REMOTE_HOST = "10.1.15.10"
PORT = "5000"
OUTPUT_DIR = "/home/robbie/Code/speech_to_text/audio"
OUTPUT_DIR_TEXT = "/home/robbie/Code/speech_to_text/text"
CHUNK_DURATION = 30  # Duration of each chunk in seconds

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_timestamp():
    """Generate a timestamp for naming the output files."""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def process_audio_stream():
    """Receive the audio stream and process it into chunks."""
    # Start the netcat process to receive audio stream
    nc_process = subprocess.Popen(
        ['nc', REMOTE_HOST, PORT],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Calculate the number of bytes needed for each chunk
    # ffmpeg reads raw PCM data at 48000 Hz, 16-bit, mono
    bytes_per_second = 48000 * 2  # 2 bytes per sample (16-bit)
    chunk_size = CHUNK_DURATION * bytes_per_second

    buffer = io.BytesIO()
    file_count = 0

    try:
        while True:
            # Read the raw audio data from netcat
            chunk_data = nc_process.stdout.read(chunk_size)

            if not chunk_data:
                break

            # Write the chunk data to a buffer
            buffer.write(chunk_data)

            # Process the buffer in chunks and save to file
            while buffer.tell() >= chunk_size:
                timestamp = generate_timestamp()
                file_name = os.path.join(OUTPUT_DIR, f"audio_{timestamp}.wav")
                buffer.seek(0)
                with subprocess.Popen(
                    [
                        'ffmpeg', '-f', 's16le', '-ar', '48000', '-ac', '1', '-i', '-',
                        '-t', str(CHUNK_DURATION), file_name
                    ],
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE
                ) as ffmpeg_process:
                    ffmpeg_process.communicate(input=buffer.read(chunk_size))

                buffer.seek(0)
                buffer.truncate(0)  # Clear buffer

                print(f"Chunk saved as {file_name}")
                #file_count += 1

                # Transcribe the audio file using Whisper
                transcribe_audio(file_name)

    finally:
        nc_process.terminate()

def transcribe_audio(file_path):
    """Transcribe the audio file using Whisper."""
    print(f"Transcribing {file_path}...")
    
    # Load the Whisper model
    model = whisper.load_model("tiny")  # You can choose 'small', 'medium', 'large' based on your requirements

    # Transcribe the audio
    result = model.transcribe(file_path)

    # Print or save the transcription result
    transcription = result['text']
    timestamp = generate_timestamp()
    transcription_file = os.path.join(OUTPUT_DIR_TEXT, f"transcription_{timestamp}.txt")
    with open(transcription_file, 'w') as f:
        f.write(transcription)

    print(f"Transcription saved as {transcription_file}")

if __name__ == "__main__":
    process_audio_stream()
