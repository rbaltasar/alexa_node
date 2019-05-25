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

lamp_id = ""
bedroom_id = ""
terrace_id = ""
reminder_id = ""

def handle_lamp_request(request):

    action = request["action"]
    value = request["value"]

    if(action == "setPowerState"):
        if(value == "ON"):
            client.publish("lamp_network/mode_request", "{\"mode\":\"1\",\"id_mask\":255}")
            print("Switching lamp ON")
        else:
            client.publish("lamp_network/mode_request", "{\"mode\":\"0\",\"id_mask\":255}");
            print("Switching lamp OFF")

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

def handle_reminder_request(request):

    pass


def on_message(ws, message):

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
		header={'Authorization:' +  base64.b64encode('apikey:')},
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()

if __name__ == "__main__":
    initiate()
