import time
from datetime import datetime
import paho.mqtt.client as mqtt
import json



timers = list()

class Timer():
    def __init__(self, name: str, duration: int, start: datetime):
        self.name = name
        self.duration = duration
        self.start = start

def create_timer(hours: int, minutes: int, seconds: int, name: str="") -> None:
    num_seconds = (((hours * 60) + minutes) * 60) + seconds
    if name == "":
        name_hours = f"{hours} hour " if (hours > 0) else ""
        name_minutes = f"{minutes} minute " if (minutes > 0) else ""
        name_seconds = f"{seconds} second" if (seconds > 0) else ""
        name = name_hours + name_minutes + name_seconds 
    new_timer = Timer(name=name, duration=num_seconds, start=datetime.now())
    
    timers.append(new_timer)

    return



def mqtt_on_connect(client, userdata, flags, rc, properties):
    print("timer process connected to mqtt broker with result code " + str(rc))
    client.subscribe("set timer")

def mqtt_on_message(client, userdata, msg):
    if msg.topic == "set timer":
        timer_args = json.loads(msg.payload.decode('utf-8'))
        create_timer(**timer_args)

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = mqtt_on_connect
mqtt_client.on_message = mqtt_on_message
mqtt_client.connect("10.0.0.244", 1883, 60)
mqtt_client.loop_start()



try:
    while True:
        print(timers)
        for idx, timer in enumerate(timers):
            if (datetime.now() - timer.start).total_seconds() >= timer.duration:
                mqtt_client.publish("ring timer", timer.name)
                timers[idx] = None
        timers = list(filter(lambda timer: timer is not None, timers))
                
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping timer process")

finally:
    mqtt_client.close()
    