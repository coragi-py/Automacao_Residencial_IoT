## Bloco 1 (boot.py):

```
with open('boot.py', 'w') as f:
    f.write(r'''import network
import time
print("Iniciando o bootloader...")
print("Conectando à rede Wi-Fi Wokwi-GUEST...")
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect('Wokwi-GUEST', '')
print(station.ifconfig())
while not station.isconnected():
    print(".", end="")
    time.sleep(0.5)
print("\nConexão Wi-Fi estabelecida com sucesso!")
''')
```

## Bloco 2 (sensors.py):

```
with open('sensors.py', 'w') as f:
    f.write(r'''from machine import Pin, ADC
import dht
dht_sensor = dht.DHT22(Pin(15))
ldr_sensor = ADC(Pin(34))
ldr_sensor.atten(ADC.ATTN_11DB)
pir_sensor = Pin(27, Pin.IN)
btn_sensor = Pin(14, Pin.IN, Pin.PULL_UP)
def read_sensors():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
    except OSError:
        temp, hum = 0.0, 0.0
    return {"temp": temp, "hum": hum, "ldr": ldr_sensor.read(), "pir": pir_sensor.value(), "btn": btn_sensor.value()}
''')
```

## Bloco 3 (display.py):

```
with open('display.py', 'w') as f:
    f.write(r'''from machine import Pin, SoftI2C
import ssd1306
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
def update_display(sensor_data):
    oled.fill(0)
    oled.text("Status Sensores:", 0, 0)
    oled.text("Temp: {:.1f}C".format(sensor_data["temp"]), 0, 16)
    oled.text("Umid: {:.1f}%".format(sensor_data["hum"]), 0, 26)
    oled.text("Luz (LDR): {}".format(sensor_data["ldr"]), 0, 36)
    oled.text("Mov: {}".format("DETECTADO" if sensor_data["pir"] == 1 else "SEGURO"), 0, 46)
    oled.text("Porta: {}".format("ABERTA" if sensor_data["btn"] == 0 else "FECHADA"), 0, 56)
    oled.show()
''')
```

## Bloco 4 (web_server.py):

```
with open('web_server.py', 'w') as f:
    f.write(r'''import socket
from machine import Pin
led, relay, buzzer = Pin(2, Pin.OUT), Pin(4, Pin.OUT), Pin(5, Pin.OUT)
def get_html():
    return """<!DOCTYPE html><html><head><title>Automacao Residencial</title><meta name="viewport" content="width=device-width, initial-scale=1"><meta charset="UTF-8"><style>body{font-family:Arial;text-align:center;padding-top:30px;background-color:#e0e5ec;}.container{background-color:white;padding:20px;border-radius:12px;display:inline-block;min-width:300px;}.button{border:none;color:white;padding:15px;margin:10px 2px;cursor:pointer;border-radius:8px;width:100%;}.btn-on{background-color:#4CAF50;}.btn-off{background-color:#D32F2F;}</style></head><body><div class="container"><h2>Controle Local</h2><p>Luz (LED): <strong>""" + ("LIGADA" if led.value() else "DESLIGADA") + """</strong></p><a href="/?led=toggle"><button class="button """ + ("btn-on" if led.value() else "btn-off") + """">Alternar Luz</button></a><p>Ar-Condicionado: <strong>""" + ("LIGADO" if relay.value() else "DESLIGADO") + """</strong></p><a href="/?relay=toggle"><button class="button """ + ("btn-on" if relay.value() else "btn-off") + """">Alternar Ar</button></a><p>Alarme: <strong>""" + ("LIGADO" if buzzer.value() else "DESLIGADO") + """</strong></p><a href="/?buzzer=toggle"><button class="button """ + ("btn-on" if buzzer.value() else "btn-off") + """">Alternar Alarme</button></a></div></body></html>"""
def setup_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80)); s.listen(5); s.setblocking(False)
    return s
def handle_client(s):
    try:
        conn, addr = s.accept()
        conn.settimeout(0.5)
        req = conn.recv(1024).decode()
        if req:
            if '/?led=toggle' in req: led.value(not led.value())
            elif '/?relay=toggle' in req: relay.value(not relay.value())
            elif '/?buzzer=toggle' in req: buzzer.value(not buzzer.value())
        conn.send('HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n' + get_html())
        conn.close()
    except OSError: pass
''')
```

## Bloco 5 (mqtt_handler.py):

```
with open('mqtt_handler.py', 'w') as f:
    f.write(r'''import json
from umqtt.simple import MQTTClient
from machine import Pin
led, relay, buzzer = Pin(2, Pin.OUT), Pin(4, Pin.OUT), Pin(5, Pin.OUT)
CLIENT_ID = "esp32_iot_m2_12345"
BROKER = "broker.hivemq.com"
TOPIC_TEL = b"automa/m2/telemetry"
TOPIC_CMD = b"automa/m2/commands"
client = MQTTClient(CLIENT_ID, BROKER, keepalive=60)
def sub_cb(topic, msg):
    try:
        cmd = json.loads(msg.decode('utf-8'))
        dev, act = cmd.get("device"), cmd.get("action")
        val = 1 if act == "on" else 0
        if dev == "led": led.value(val)
        elif dev == "relay": relay.value(val)
        elif dev == "buzzer": buzzer.value(val)
    except Exception as e: pass
def setup_mqtt():
    client.set_callback(sub_cb)
    print("Conectando HiveMQ...")
    client.connect()
    client.subscribe(TOPIC_CMD)
    print("MQTT Conectado!")
    return client
def publish_telemetry(data):
    client.publish(TOPIC_TEL, json.dumps(data))
''')
```

## Bloco 6 (main.py):

```
with open('main.py', 'w') as f:
    f.write(r'''import time
from sensors import read_sensors
from display import update_display
from web_server import setup_server, handle_client
from mqtt_handler import setup_mqtt, publish_telemetry
print("Iniciando sistema...")
server_socket = setup_server()
try: mqtt_client = setup_mqtt()
except Exception as e: mqtt_client = None
last_read = time.ticks_ms()
while True:
    handle_client(server_socket)
    if mqtt_client:
        try: mqtt_client.check_msg()
        except OSError: pass
    if time.ticks_diff(time.ticks_ms(), last_read) >= 2000:
        data = read_sensors()
        update_display(data)
        if mqtt_client:
            try: publish_telemetry(data)
            except OSError: pass
        last_read = time.ticks_ms()
    time.sleep(0.05)
''')
```

## Importar bibliotecas depois de soft reset

```
import mip
mip.install('ssd1306')
mip.install('umqtt.simple')
```
