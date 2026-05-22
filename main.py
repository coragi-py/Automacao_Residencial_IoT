import time
from sensors import read_sensors
from display import update_display
from web_server import setup_server, handle_client
from mqtt_handler import setup_mqtt, publish_telemetry

print("Iniciando sistema de monitoramento, web server e MQTT...")

# Configura o servidor web na porta 80
server_socket = setup_server()

# Configura e conecta o MQTT
try:
    mqtt_client = setup_mqtt()
except Exception as e:
    print("Falha ao conectar MQTT:", e)
    mqtt_client = None

# Controle de tempo não-bloqueante
last_sensor_read = time.ticks_ms()
READ_INTERVAL_MS = 2000 

while True:
    # 1. Trata requisições do servidor web local instantaneamente
    handle_client(server_socket)
    
    # 2. Verifica se há novos comandos via MQTT (Subscribe)
    if mqtt_client:
        try:
            mqtt_client.check_msg()
        except OSError:
            pass # Ignora erros temporários de conexão
    
    # 3. Leitura dos sensores e publicação a cada 2 segundos
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_sensor_read) >= READ_INTERVAL_MS:
        data = read_sensors()
        update_display(data)
        
        # Publica os dados de telemetria no broker (Publish)
        if mqtt_client:
            try:
                publish_telemetry(data)
                print("Telemetria publicada MQTT:", data)
            except OSError:
                pass
                
        last_sensor_read = current_time
        
    # 4. Micro-pausa obrigatória para estabilidade do Wokwi
    time.sleep(0.05)