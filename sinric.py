#!/usr/bin/python
import websocket
import thread
import time
import base64
import json
import paho.mqtt.client as paho

client= paho.Client("AlexaNode")
print("connecting to broker ")
client.connect("localhost",1883)#("localhost",1883)#connect
client.loop_start() #start loop to process received messages

lamp_id = "5bf6f10db6b8c25922919a5e"
bedroom_id = "5c606a6c4ce891656a4229a8"
terrace_id = "5ce42c2c6aa4f1076d3bddf2"
goodnight_id = "5ceeb46d556b3025b935c7ee"
reminder_id = "5ce920e325b3d3191b7be2e4"
ngrok_tunnel = "5d0fc7cc1b911b7049eb7b5b"
music_node = "5d223a577bdf2c2c0409ecb2"
mini_music_node = "5d58324d1bddb66e3639f4a2"

class HSV2RGB:
    
    def convert(self,h,s,v):

        if(s <= 0.0):
            self.r = v
            self.g = v
            self.b = v
       
        hh = h;
        if(hh >= 360.0):
            hh = 0.0

        hh = hh/60.0
        i = hh
        ff = hh - i
        p = v * (1.0 - s)
        q = v * (1.0 - (s * ff))
        t = v * (1.0 - (s * (1.0 - ff)))

        
        if(i==0):
            self.r = v
            self.g = t
            self.b = p
        elif(i==1):
            self.r = q
            self.g = v
            self.b = p
        elif(i==2):
            self.r = p
            self.g = v
            self.b = t
        elif(i==3):
            self.r = p
            self.g = q
            self.b = v
        elif(i==4):
            self.r = t
            self.g = p
            self.b = v
        else:
            self.r = v
            self.g = p
            self.b = q

        self.r = int(self.r * 255)
        self.g = int(self.g * 255)
        self.b = int(self.b * 255)
    


def handle_lamp_request(request):

    action = request["action"]
    value = request["value"]

    if(action == "setPowerState"):
        if(value == "ON"):
            client.publish("lamp_network/mode_request", "{\"mode\":\"1\",\"id_mask\":255}")
	    client.publish("lamp_network/mode_request_feedback", "{\"mode\":\"1\",\"id_mask\":255}")
            print("Switching lamp ON")
        else:
            client.publish("lamp_network/mode_request", "{\"mode\":\"0\",\"id_mask\":255}")
	    client.publish("lamp_network/mode_request_feedback", "{\"mode\":\"0\",\"id_mask\":255}")
            print("Switching lamp OFF")

    elif(action == "SetColor"):
        converter = HSV2RGB()
        converter.convert(request["value"]["hue"],request["value"]["saturation"],request["value"]["brightness"])

        message = json.dumps({'R': converter.r, 'G': converter.g, 'B': converter.b, 'id_mask': 255})
        client.publish("lamp_network/light_color", message)

    elif(action == "SetColorTemperature"):

        message = json.dumps({'R': 250, 'G': 250, 'B': 250, 'id_mask': 255})
        client.publish("lamp_network/light_color", message)

    elif(action == "SetBrightness"):

        message = json.dumps({'intensity': int(request["value"]/10),'id_mask': 255})
        client.publish("lamp_network/light_intensity", message)


def handle_bedroom_request(request):

    action = request["action"]
    value = request["value"]

    if(action == "setPowerState"):
        if(value == "ON"):
            client.publish("bedroom_node/mode_request", "{\"mode\":\"1\"}")
            print("Switching bedroom ON")
        else:
            client.publish("bedroom_node/mode_request", "{\"mode\":\"0\"}")
            print("Switching bedroom OFF")

    elif(action == "SetColor"):
        converter = HSV2RGB()
        converter.convert(request["value"]["hue"],request["value"]["saturation"],request["value"]["brightness"])

        message = json.dumps({'R': converter.r, 'G': converter.g, 'B': converter.b, 'id_mask': 255})
        client.publish("bedroom_node/light_color", message)

    elif(action == "SetColorTemperature"):

        message = json.dumps({'R': 250, 'G': 250, 'B': 250})
        client.publish("bedroom_node/light_color", message)

    elif(action == "SetBrightness"):

        message = json.dumps({'intensity': int(request["value"]/10)})
        client.publish("bedroom_node/light_intensity", message)

def handle_terrace_request(request):
    action = request["action"]
    value = request["value"]

    if(action == "setPowerState"):
        if(value == "ON"):
            client.publish("terrace_node/mode_request", "{\"mode\":\"1\"}")
            print("Switching terrace ON")
        else:
            client.publish("terrace_node/mode_request", "{\"mode\":\"0\"}")
            print("Switching terrace OFF")

    elif(action == "SetColor"):
        converter = HSV2RGB()
        converter.convert(request["value"]["hue"],request["value"]["saturation"],request["value"]["brightness"])

        message = json.dumps({'R': converter.r, 'G': converter.g, 'B': converter.b, 'id_mask': 255})
        client.publish("terrace_node/light_color", message)

    elif(action == "SetColorTemperature"):

        message = json.dumps({'R': 250, 'G': 250, 'B': 250})
        client.publish("terrace_node/light_color", message)

    elif(action == "SetBrightness"):

        message = json.dumps({'intensity': int(request["value"]/10)})
        client.publish("terrace_node/light_intensity", message)

def handle_reminder_request(request):

    action = request["action"]
    value = request["value"]

    if(action == "setPowerState"):
        if(value != "ON"):
            client.publish("reminder_node/disableAll", "")
            print("Launching reminder enable all")


def handle_goodnight_request(request):

    action = request["action"]
    value = request["value"]

    if(action == "setPowerState"):
        if(value == "ON"):
            client.publish("reminder_node/goodnight", "")
            print("Launching goodnight reminder")

def handle_ngrok_tunnel_request(request):

    action = request["action"]
    value = request["value"]

    if(action == "setPowerState"):
        if(value == "ON"):
            client.publish("ngrok_node/activate", "")
            print("Activating ngrok tunnel")

def handle_music_node_request(request):

    action = request["action"]
    value = request["value"]

    if(action == "setPowerState"):
        if(value == "ON"):
            client.publish("music_node/start", "0")
            print("Starting music node")

def handle_mini_music_node_request(request):

    action = request["action"]
    value = request["value"]

    if(action == "setPowerState"):
        if(value == "ON"):
            client.publish("music_node/start", "1")
            print("Starting mini music node")


def on_message(ws, message):

    print(message)

    j = json.loads(message)

    deviceId = j["deviceId"]

    if(deviceId == lamp_id):
        handle_lamp_request(j)
    elif(deviceId == bedroom_id):
        handle_bedroom_request(j)
    elif(deviceId == terrace_id):
        handle_terrace_request(j)
    elif(deviceId == reminder_id):
        handle_reminder_request(j)
    elif(deviceId == goodnight_id):
        handle_goodnight_request(j)
    elif(deviceId == ngrok_tunnel):
        handle_ngrok_tunnel_request(j)
    elif(deviceId == music_node):
        handle_music_node_request(j)
    elif(deviceId == mini_music_node):
        handle_mini_music_node_request(j)

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"
    # Attemp to reconnect with 2 seconds interval
    time.sleep(2)
    initiate()

def on_open(ws):
    print "### Initiating new websocket connection ###"

def initiate():
    websocket.enableTrace(True)

    ws = websocket.WebSocketApp("ws://iot.sinric.com",
		header={'Authorization:' +  base64.b64encode('apikey:3cfe9698-1111-43b6-8931-3302da09352e')},
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()

if __name__ == "__main__":
    initiate()
