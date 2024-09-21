import pyaudio
import wave

# Define the audio file path
audio_file = 'StarWars60.wav'

# Open the audio file
wf = wave.open(audio_file, 'rb')

# Create an interface to PortAudio
p = pyaudio.PyAudio()

# Open a .Stream object to write the WAV file to the audio output
# 'format' gets the sample format from the WAV file
# 'channels' gets the number of channels (1 for mono, 2 for stereo, etc.)
# 'rate' gets the frame rate (samples per second)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# Read data in chunks
chunk = 1024
data = wf.readframes(chunk)

# Play the sound by writing the audio data to the stream
while data:
    stream.write(data)
    data = wf.readframes(chunk)

# Stop and close the stream
stream.stop_stream()
stream.close()

# Close PyAudio
p.terminate()

# Close the WAV file
wf.close()
