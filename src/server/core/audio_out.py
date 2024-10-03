import pyaudio
from pydub import AudioSegment
from io import BytesIO

def play_audio_with_pyaudio(audio_stream):
    # Load the audio from the BytesIO stream (assuming MP3 format)
    audio = AudioSegment.from_file(audio_stream, format="mp3")

    # Extract raw audio data
    raw_data = audio.raw_data
    
    # Get audio properties
    sample_width = audio.sample_width
    channels = audio.channels
    frame_rate = audio.frame_rate

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream with the correct settings
    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=channels,
                    rate=frame_rate,
                    output=True)

    # Play the audio
    stream.write(raw_data)

    # Close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
