# hestia
Hestia is a secure, customizable home automation assistant, second memory, and chatbot.

5/17/2024:

If using an M1 Mac, you may receive an error when installing pyaudio. In that case, you should use run `brew install portaudio` before trying again.

According to picovoice, the wake word models (.ppn) are specifically created for Mac. I'm not sure if they still work on windows. It's worth giving it a shot. Otherwise, you'll need to make a free https://console.picovoice.ai/ account and "train" your own model from there because I'm already using 2/3 free model credits on my own lol. And then set your API key as PV_ACCESS_KEY in your env.

Don't forget to install requirements.txt with pip3 install -r requirements.txt!

Sometimes I would get a buffer overflow bug with the line pcm = audio_stream.read(porcupine.frame_length) so then I just set it to not raise an overflow error :sob:. I don't think it really matters since we're just constantly reading. Also, I stop reading during whatever we're executing on wake word detection, so maybe that will also help prevent buffer overflows because there's less time where the microphone is active but we're not emptying the buffer (shrugs).

Also, since we have two wake words that have a shared "subphoneme (?)", right now I have a guard that prevents "hey hestia" from being read as both "hestia" and "hey hestia", just by asking "if you've already recognized a keyword in the last second, don't recognize another one yet". I don't think we'll need this once we're actually making a speech recognition API call because then the next read won't come until significantly later?
