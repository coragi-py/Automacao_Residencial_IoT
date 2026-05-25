import time
from sensors import read_sensors
from display import update_display
from web_server import setup_server, handle_client
from mqtt_handler import setup_mqtt, publish_telemetry

print("Iniciando sistema...")
server_socket = setup_server()

try: 
    mqtt_client = setup_mqtt()
except Exception as e: 
    mqtt_client = None

last_read = time.ticks_ms()

while True:
    # 1. Atende o Servidor Web (Navegador)
    handle_client(server_socket)
    
    # 2. Atende os comandos vindos do MQTT/Node-RED
    if mqtt_client:
        try: 
            mqtt_client.check_msg()
        except OSError: 
            pass
            
    # 3. Lê os sensores e envia telemetria a cada 2 segundos (2000ms)
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_read) >= 2000:
        data = read_sensors()
        update_display(data)
        if mqtt_client:
            try: 
                publish_telemetry(data)
            except OSError: 
                pass
        last_read = current_time
        
    # -----------------------------------------------------------------
    # Dá 50 milissegundos para o processador do 
    # ESP32 respirar e processar os pacotes de rede sem dar Timeout!
    # -----------------------------------------------------------------
    time.sleep(0.05)