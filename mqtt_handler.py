import json
from umqtt.simple import MQTTClient
from machine import Pin

# Mapeamento estrito para controle dos atuadores via MQTT
led = Pin(2, Pin.OUT)
relay = Pin(4, Pin.OUT)
buzzer = Pin(5, Pin.OUT)

# Configurações do Broker HiveMQ
MQTT_CLIENT_ID = "esp32_iot_academic_m2_12345" # Adicione números aleatórios para evitar colisão
MQTT_BROKER = "broker.hivemq.com"
MQTT_TELEMETRY_TOPIC = b"automa/m2/telemetry"
MQTT_COMMAND_TOPIC = b"automa/m2/commands"

client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, keepalive=60)

def sub_cb(topic, msg):
    try:
        # Decodifica o payload JSON. Ex esperado: {"device": "led", "action": "on"}
        command = json.loads(msg.decode('utf-8'))
        device = command.get("device")
        action = command.get("action")
        
        # Altera fisicamente o pino. A página web (web_server.py) refletirá a mudança na próxima recarga.
        if device == "led":
            led.value(1 if action == "on" else 0)
        elif device == "relay":
            relay.value(1 if action == "on" else 0)
        elif device == "buzzer":
            buzzer.value(1 if action == "on" else 0)
            
        print("Comando executado via MQTT: {} -> {}".format(device, action))
    except Exception as e:
        print("Erro ao processar comando MQTT:", e)

def setup_mqtt():
    client.set_callback(sub_cb)
    print("Conectando ao broker MQTT HiveMQ...")
    client.connect()
    client.subscribe(MQTT_COMMAND_TOPIC)
    print("Conectado ao HiveMQ e inscrito no tópico de comandos!")
    return client

def publish_telemetry(sensor_data):
    # Envia os dados dos 4 sensores em formato JSON
    payload = json.dumps(sensor_data)
    client.publish(MQTT_TELEMETRY_TOPIC, payload)