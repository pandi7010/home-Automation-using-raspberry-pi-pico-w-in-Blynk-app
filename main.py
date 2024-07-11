import time
import network
from machine import Pin
import BlynkLib
 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("ssid","Password")
 
BLYNK_AUTH = '******************'
 
# Wait for network connection
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    ip = wlan.ifconfig()[0]
    print('IP: ', ip)
 
# Connect to Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)
 
# Initialize the relay pins
relay1_pin = Pin(16, Pin.OUT)
relay2_pin = Pin(17, Pin.OUT)

# Register virtual pin handler
@blynk.on("V0") #virtual pin V1
def v0_write_handler(value): #read the value
    if int(value[0]) == 0:
        relay1_pin.value(1) #turn the relay1 on
    else:
        relay1_pin.value(0) #turn the relay1 off
 
@blynk.on("V1") #virtual pin V2
def v1_write_handler(value): #read the value
    if int(value[0]) == 0:
        relay2_pin.value(1) #turn the relay2 on
    else:
        relay2_pin.value(0) #turn the relay2 off
 
while True:
    blynk.run()
