import time
from sensors import read_sensors
from display import update_display
from web_server import setup_server, handle_client

print("Iniciando sistema de monitoramento e servidor web...")

# Configura o servidor web na porta 80
server_socket = setup_server()

# Controle de tempo não-bloqueante
last_sensor_read = time.ticks_ms()
READ_INTERVAL_MS = 2000 

while True:
    # 1. Trata requisições do servidor web instantaneamente
    handle_client(server_socket)
    
    # 2. Leitura dos sensores a cada 2 segundos (sem bloquear a execução)
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_sensor_read) >= READ_INTERVAL_MS:
        data = read_sensors()
        update_display(data)
        print("Dados lidos:", data)
        last_sensor_read = current_time
        
    # 3. Micro-pausa obrigatória para o Wokwi processar o background
    time.sleep(0.05)