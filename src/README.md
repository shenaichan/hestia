# hestia
Hestia is a secure, customizable home automation assistant, second memory, and chatbot.

## 5/23/2024 R

received the RPi5 and the 7" display screen, but it came with the wrong display cable, so I ordered another one, plus an HDMI converter to hook it up to a real monitor for testing. cannot test flashing the board yet because I have no display, but I downloaded/configured the OS onto a microSD and put it in the board, so we shall see tomorrow. 

caught up on documentation and cleaned up a bunch of code. figured out how to retrieve messages from the useWebSocket hook

## 5/22/2024 W

sort of had an existential crisis and attempted to reimplement backend in Flask bc it should have lower memory footprint, but then decided that it's probably okay either way (Django/Flask) and I should do whatever makes me less stressed. have been getting rather stressed out about this project for no good reason lmfao

watched a bunch of tutorials on threejs/react3fiber. heavily considering buying the $95 class but need to take some time to process spending that much money lol

added a react lib called useWebSocket which basically provides a hook interface for the websocket so it can be used nicely in react apps. I'm gonna be real I don't entirely understand what this means so I need to research more stuff. I just implemented "on connect" and have yet to figure out how to handle a message

## 5/21/2024 T

connected the django websocket consumer to MQTT message events ([commit](https://github.com/shenaichan/hestia/commit/fe18559a26e6e3fd892217689fc97702ef91746e)). this was also extremely annoying -- the main issue was figuring out how to send a message over a channel layer to a consumer from outside the context of a consumer (I'm used to doing this in Flask, where you just call a method on a socket object). my main takeaway is that WHENEVER YOU INTERFACE WITH THE CHANNEL LAYER YOU HAVE TO USE ASYNC_TO_SYNC IF THE FUNCTION CONTEXT IS SYNCHRONOUS! 

actually my main takeaway is that if there's a good offical tutorial for a library/framework that's applicable to the context that I'm using it in, I should read that carefully, first. 

I was spending a lot of time reading blog posts and asking ChatGPT questions, but my major breakthroughs happened when (1) I read the official tutorial and saw that you don't make an instance of the consumer object outside of the file, you need to call get_channel_layer and send over the channel layer. and you need to set the type of the message to the method that should handle it, but replace the method name with periods instead of underscores (seriously wtf lol) & (2) I was looking at stackoverflow answers that suggested I wasn't handling the async to sync conversion correctly for my channel_layer group add. this was also on the official tutorial, but I guess I didn't process that while I was reading it. I think I tend to be kind of impatient when I'm learning and implementing new things, and I need to slow down.

also cleared out the asgi.py file since I'm using routing.py for the asgi application configs. note to future self that if I ever want to extend this project to multiple authenticated users I will need to pay attention to middleware, and do something like this in routing.py:

```
django_asgi_app = get_asgi_application()

import chat.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
        ),
    }
)
```

see [channels docs](https://channels.readthedocs.io/en/stable/tutorial/part_2.html) for more details.

## 5/20/2024 M

set up the basic infrastructure for websockets ([commit](https://github.com/shenaichan/hestia/commit/8cc6e8f16d0178844ba7098e33d66a9dd97c7b9a)), with a connection between the django backend and the react/next frontend. lowkey this was really really annoying :skull: 

basically:
- download django channels, which is an extension library that helps support websockets within the django framework
- download daphne, which is an asynchronous server gateway interface required to run websockets on django, as it's supposed to help handle events that can happen basically whenever
- set the proxy on the client side to localhost:8000 (I am not actually sure if this is necessary)
- set up a websocket object on the client side, along with methods to handle connection, message receipt, etc.
- create a "consumer" class in hestia_api, which is basically the thing that manages messages being sent places (?) you can define methods for connection/disconnect/send/receive here
- set up configs for the:
  - websocket url pattern (ws/command/consumer obj)
  - application (asgit for http, websocket url pattern for websocket)
  - installed apps, asgi_app, channel layers
  - include websocket url pattern in the urlpatterns list in hestia_core/urls.py

## 5/19/2024 U

set up MQTT connection such that you can write to main.py from the CLI and write to the CLI from main.py. stands to reason that you can connect between two python files but will test later

watched a bunch of blender tutorials :+1: spent like 2 hours learning how to make a donut, WIP

## 5/18/2024 S

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

renamed backend core module from server to hestia_core for legibility (i dont think it broke anything buuuut :fingers_crossed:)

nabbed a dashboard template from https://github.com/devias-io/material-kit-react. i am slightly dubious as to whether introducing this much complexity (Material UI, Next.js as frontend) is a good idea but i think it will definitely help me learn!

## 5/17/2024 F

If using an M1 Mac, you may receive an error when installing pyaudio. In that case, you should run `brew install portaudio` before trying again.

According to picovoice, the wake word models (.ppn) are specifically created for Mac. I'm not sure if they still work on windows. It's worth giving it a shot. Otherwise, you'll need to make a free https://console.picovoice.ai/ account and "train" your own model from there because I'm already using 2/3 free model credits on my own lol. And then set your API key as `PV_ACCESS_KEY` in your env.

Don't forget to install requirements.txt with `pip3 install -r requirements.txt`!

Sometimes I would get a buffer overflow bug with the line pcm = audio_stream.read(porcupine.frame_length) so then I just set it to not raise an overflow error :sob:. I don't think it really matters since we're just constantly reading. Also, I stop reading during whatever we're executing on wake word detection, so maybe that will also help prevent buffer overflows because there's less time where the microphone is active but we're not emptying the buffer (shrugs).

Also, since we have two wake words that have a shared "subphoneme (?)", right now I have a guard that prevents "hey hestia" from being read as both "hestia" and "hey hestia", just by asking "if you've already recognized a keyword in the last second, don't recognize another one yet". I don't think we'll need this once we're actually making a speech recognition API call because then the next read won't come until significantly later?