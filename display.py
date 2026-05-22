from machine import Pin, SoftI2C
import ssd1306

# Inicialização do I2C nos pinos SDA(21) e SCL(22) definidos na Etapa 1
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def update_display(sensor_data):
    oled.fill(0) # Limpa o frame anterior
    oled.text("Status Sensores:", 0, 0)
    oled.text("Temp: {:.1f}C".format(sensor_data["temp"]), 0, 16)
    oled.text("Umid: {:.1f}%".format(sensor_data["hum"]), 0, 26)
    oled.text("Luz (LDR): {}".format(sensor_data["ldr"]), 0, 36)
    oled.text("Mov: {}".format("DETECTADO" if sensor_data["pir"] == 1 else "SEGURO"), 0, 46)
    oled.text("Porta: {}".format("ABERTA" if sensor_data["btn"] == 0 else "FECHADA"), 0, 56)
    oled.show()