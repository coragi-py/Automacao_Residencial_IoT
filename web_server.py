import socket
from machine import Pin

# Mapeamento estrito de hardware para atuadores (GPIOs da Etapa 1)
led = Pin(2, Pin.OUT)
relay = Pin(4, Pin.OUT)
buzzer = Pin(5, Pin.OUT)

def get_html():
    # Gera o HTML e CSS injetado de forma dinâmica para ser bidirecional
    html = """<!DOCTYPE html>
    <html>
    <head>
        <title>Automacao Residencial</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin: 0px auto; padding-top: 30px; background-color: #e0e5ec;}
            .container { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); display: inline-block; min-width: 300px;}
            .button { border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 10px 2px; cursor: pointer; border-radius: 8px; width: 100%; box-sizing: border-box; transition: background-color 0.3s;}
            .btn-on { background-color: #4CAF50; } /* Verde */
            .btn-off { background-color: #D32F2F; } /* Vermelho */
            p { font-size: 18px; color: #333; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Controle Local</h2>
            
            <p>Luz (LED): <strong>""" + ("LIGADA" if led.value() else "DESLIGADA") + """</strong></p>
            <a href="/?led=toggle"><button class="button """ + ("btn-on" if led.value() else "btn-off") + """">Alternar Luz</button></a>
            
            <p>Ar-Condicionado (Relé): <strong>""" + ("LIGADO" if relay.value() else "DESLIGADO") + """</strong></p>
            <a href="/?relay=toggle"><button class="button """ + ("btn-on" if relay.value() else "btn-off") + """">Alternar Ar</button></a>
            
            <p>Alarme (Buzzer): <strong>""" + ("LIGADO" if buzzer.value() else "DESLIGADO") + """</strong></p>
            <a href="/?buzzer=toggle"><button class="button """ + ("btn-on" if buzzer.value() else "btn-off") + """">Alternar Alarme</button></a>
        </div>
    </body>
    </html>"""
    return html

def setup_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)
    s.setblocking(False) # Configuração não bloqueante vital para não travar o main
    return s

def handle_client(s):
    try:
        conn, addr = s.accept()
        conn.settimeout(0.5)
        request = conn.recv(1024).decode()
        
        if request:
            # Lógica para tratar os comandos recebidos pelos botões HTML
            if '/?led=toggle' in request:
                led.value(not led.value())
            elif '/?relay=toggle' in request:
                relay.value(not relay.value())
            elif '/?buzzer=toggle' in request:
                buzzer.value(not buzzer.value())
        
        response = get_html()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError:
        pass # Ignora quando não há novas requisições (socket não bloqueante)