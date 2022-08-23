
from sinric import SinricPro
import asyncio
import paho.mqtt.client as paho
import json
import credentials

mqtt_client= paho.Client("Test")

APP_KEY = 'd0d861a1-9302-403a-98ca-fd79304c040f'
APP_SECRET = '396f2c38-c5dc-40ca-aa19-a6ab38a2180e-9a18e27d-da3e-463a-9e95-711cd9e2b3b8'
LIGHT_ID = '6303af6ddb270037341d6f64'

def power_state(did, state):
    # Alexa, turn ON/OFF Device
    print(did, state)

    if(state == "On"):
        mqtt_client.publish("lamp_network/mode_request", "{\"mode\":\"1\",\"id_mask\":255}")
        mqtt_client.publish("lamp_network/mode_request_feedback", "{\"mode\":\"1\",\"id_mask\":255}")
        print("Switching lamp ON")
    else:
        mqtt_client.publish("lamp_network/mode_request", "{\"mode\":\"0\",\"id_mask\":255}")
        mqtt_client.publish("lamp_network/mode_request_feedback", "{\"mode\":\"0\",\"id_mask\":255}")
        print("Switching lamp OFF")
    return True, state


def set_brightness(did, state):
    # Alexa set device brightness to 40%
    print(did, 'BrightnessLevel : ', state)

    message = json.dumps({'intensity': int(state/10),'id_mask': 255})
    mqtt_client.publish("lamp_network/light_intensity", message)

    return True, state


def adjust_brightness(did, state):
    # Alexa increase/decrease device brightness by 44
    print(did, 'AdjustBrightnessLevel : ', state)

    return True, state


def set_color(did, r, g, b):
    # Alexa set device color to Red/Green
    print(did, 'Red: ', r, 'Green: ', g, 'Blue : ', b)

    message = json.dumps({'R': r, 'G': g, 'B': b, 'id_mask': 255})
    mqtt_client.publish("lamp_network/light_color", message)

    return True


def set_color_temperature(did, value):
    print(did, value)

    message = json.dumps({'R': 250, 'G': 250, 'B': 250, 'id_mask': 255})
    mqtt_client.publish("lamp_network/light_color", message)

    return True


def increase_color_temperature(device_id, value):
    return True, value


def decrease_color_temperature(device_id, value):
    return True, value


callbacks = {
    'powerState': power_state,
    'setBrightness': set_brightness,
    'adjustBrightness': adjust_brightness,
    'setColor': set_color,
    'setColorTemperature': set_color_temperature,
    'increaseColorTemperature': increase_color_temperature,
    'decreaseColorTemperature': decrease_color_temperature
}

if __name__ == '__main__':

    print("connecting to broker ")
    mqtt_client.connect("192.168.0.41",1883)#("localhost",1883)#connect
    mqtt_client.loop_start() #start loop to process received messages

    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [LIGHT_ID], callbacks, enable_log=True, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect())

# To update the light state on server.
# client.event_handler.raiseEvent(lightId, 'setPowerState',data={'state': 'On'})
# client.event_handler.raiseEvent(device_id1, 'setColor',data={'r': 0,'g': 0,'b': 0})
# client.event_handler.raiseEvent(device_id1, 'setColorTemperature',data={'colorTemperature': 2400})
