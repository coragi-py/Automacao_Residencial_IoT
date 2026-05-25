import socket
from machine import Pin

# Inicialização dos atuadores
led = Pin(2, Pin.OUT)
relay = Pin(4, Pin.OUT)
buzzer = Pin(5, Pin.OUT)

def get_html():
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
            .btn-on { background-color: #4CAF50; }
            .btn-off { background-color: #D32F2F; }
            p { font-size: 18px; color: #333; }
        </style>
        <script>
            // Script Mágico AJAX: Envia o comando em segundo plano
            function toggleDevice(device) {
                fetch('/?' + device + '=toggle')
                .then(response => {
                    // Após o ESP32 confirmar a ação, recarrega os textos suavemente
                    window.location.reload();
                });
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h2>Controle Local</h2>
            
            <p>Luz (LED): <strong>""" + ("LIGADA" if led.value() else "DESLIGADA") + """</strong></p>
            <button class="button """ + ("btn-on" if led.value() else "btn-off") + """" onclick="toggleDevice('led')">Ligar/Desligar Luz</button>
            
            <p>Ar-Condicionado (Relé): <strong>""" + ("LIGADO" if relay.value() else "DESLIGADO") + """</strong></p>
            <button class="button """ + ("btn-on" if relay.value() else "btn-off") + """" onclick="toggleDevice('relay')">Ligar/Desligar Ar</button>
            
            <p>Alarme (Buzzer): <strong>""" + ("LIGADO" if buzzer.value() else "DESLIGADO") + """</strong></p>
            <button class="button """ + ("btn-on" if buzzer.value() else "btn-off") + """" onclick="toggleDevice('buzzer')">Ligar/Desligar Alarme</button>
        </div>
    </body>
    </html>"""
    return html

def setup_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)
    s.setblocking(False)
    return s

def handle_client(s):
    try:
        conn, addr = s.accept()
    except OSError:
        return 
        
    try:
        conn.settimeout(2.0) 
        request = conn.recv(1024).decode('utf-8')
        
        if request:
            # 1. Se a requisição for um comando AJAX invisível
            if '/?led=toggle' in request:
                led.value(not led.value())
                print("🌐 [Web Server] Alternar LED ->", led.value())
                conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nOK")
                
            elif '/?relay=toggle' in request:
                relay.value(not relay.value())
                print("🌐 [Web Server] Alternar RELE ->", relay.value())
                conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nOK")
                
            elif '/?buzzer=toggle' in request:
                buzzer.value(not buzzer.value())
                print("🌐 [Web Server] Alternar BUZZER ->", buzzer.value())
                conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nOK")
                
            # 2. Se for o carregamento inicial da página inteira
            else:
                response = get_html()
                http_response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    "Connection: close\r\n\r\n"
                    + response
                )
                conn.sendall(http_response.encode('utf-8'))
                
    except Exception as e:
        print("⚠ Erro ao processar requisição HTTP:", e)
    finally:
        conn.close()