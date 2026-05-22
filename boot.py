import network
import time

print("Iniciando o bootloader...")
print("Conectando à rede Wi-Fi Wokwi-GUEST...")

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect('Wokwi-GUEST', '')

while not station.isconnected():
    print(".", end="")
    time.sleep(0.5)

print("\nConexão Wi-Fi estabelecida com sucesso!")
print("Parâmetros de rede (IP, Máscara, Gateway, DNS):", station.ifconfig())