from machine import Pin, ADC
import dht

# Mapeamento estrito de hardware (GPIOs da Etapa 1)
dht_sensor = dht.DHT22(Pin(15))
ldr_sensor = ADC(Pin(34))
ldr_sensor.atten(ADC.ATTN_11DB) # Configuração para leitura até 3.3V
pir_sensor = Pin(27, Pin.IN)
btn_sensor = Pin(14, Pin.IN, Pin.PULL_UP)

def read_sensors():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
    except OSError:
        # Tratamento caso o sensor falhe na leitura
        temp = 0.0
        hum = 0.0
        
    ldr_val = ldr_sensor.read()
    pir_val = pir_sensor.value()
    # O botão com pull-up interno retorna 0 quando pressionado e 1 quando solto
    btn_val = btn_sensor.value() 
    
    return {
        "temp": temp,
        "hum": hum,
        "ldr": ldr_val,
        "pir": pir_val,
        "btn": btn_val
    }