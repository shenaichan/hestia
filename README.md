# hestia
Hestia is a secure, customizable home automation assistant, second memory, and chatbot.

## 5/18/2024

set up basic django server & react client. I think you need to cd into `/src/client` and then run `npm install` to get the relevant packages listed in `package-lock.json`. also added some more python packages to the virtual env so just make a habit of running `pip3 install -r requirements.txt` whenever you pull.

rationale for using django and react:
- react: seems like a pretty popular and powerful frontend framework, i will also say that once you get used to it it is quite sleek and makes it easy to extend small webapps to more complicated ones.
- django: had a hard time settling on a framework that could serve the client & provide simple backend logic, but i decided i wanted the server and the other home assistant process(es) to both be in Python so that when we set up mqtt it's the same API language. it's less important to me that the client and server both be written in the same lang (JS) since there's just so much more support out there for configuring webapp frontends and backends to play nice with each other. so that basically left flask or django and i was just getting tired of using flask honestly and figured i should try to learn something new. also django has a built-in ORM for the db which seemed quite tidy to me.

used this tut: https://medium.com/@devsumitg/how-to-connect-reactjs-django-framework-c5ba268cb8be

setting up basic MQTT communication. using the paho-mqtt python module. you also need to locally install an MQTT broker, I used mosquitto. on Mac you can run `brew install mosquitto`. for future reference:
<blockquote> 

You can make changes to the configuration by editing:
    /opt/homebrew/etc/mosquitto/mosquitto.conf

To start mosquitto now and restart at login:
  brew services start mosquitto

Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/mosquitto/sbin/mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf

</blockquote>

changed to .env file for secret keys, removed starter insecure django secret key, edited .ppn paths in main


## 5/17/2024

If using an M1 Mac, you may receive an error when installing pyaudio. In that case, you should run `brew install portaudio` before trying again.

According to picovoice, the wake word models (.ppn) are specifically created for Mac. I'm not sure if they still work on windows. It's worth giving it a shot. Otherwise, you'll need to make a free https://console.picovoice.ai/ account and "train" your own model from there because I'm already using 2/3 free model credits on my own lol. And then set your API key as `PV_ACCESS_KEY` in your env.

Don't forget to install requirements.txt with `pip3 install -r requirements.txt`!

Sometimes I would get a buffer overflow bug with the line pcm = audio_stream.read(porcupine.frame_length) so then I just set it to not raise an overflow error :sob:. I don't think it really matters since we're just constantly reading. Also, I stop reading during whatever we're executing on wake word detection, so maybe that will also help prevent buffer overflows because there's less time where the microphone is active but we're not emptying the buffer (shrugs).

Also, since we have two wake words that have a shared "subphoneme (?)", right now I have a guard that prevents "hey hestia" from being read as both "hestia" and "hey hestia", just by asking "if you've already recognized a keyword in the last second, don't recognize another one yet". I don't think we'll need this once we're actually making a speech recognition API call because then the next read won't come until significantly later?