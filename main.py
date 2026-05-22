import time
from sensors import read_sensors
from display import update_display

print("Iniciando sistema de monitoramento...")

while True:
    # 1. Realiza a leitura de todos os sensores
    data = read_sensors()
    
    # 2. Atualiza o display OLED com os dados obtidos
    update_display(data)
    
    # 3. Print no console para debug
    print("Dados lidos:", data)
    
    # Pausa de 2 segundos entre as leituras
    time.sleep(2)