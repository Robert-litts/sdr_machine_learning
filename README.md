# Remotely connect to your SDR over the network and use OpenAI Whisper to convert speech to text.
This repo uses rtl_sdr to connect to stream audio from a remotely networked SDR & perform speech to text. 

1. rtl_server.sh should be running on the remote SDR server. I am running it as a systemd process to persist across restarts (both of the process, and the LXC itself)
2. ```bash pip install requirements.txt ```
3.  ```python receive_audio_to_text.py```
4. Audio will be saved as .WAV files in 30 second chunks in ./audio and transcribed text will be in ./text
