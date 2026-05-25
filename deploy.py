import socket
import time
import glob

# Configuração da porta virtual do Wokwi
HOST = '127.0.0.1'
PORT = 4000

def enviar_em_blocos(s, texto, chunk_size=64, delay=0.01):
    """Envia texto em pequenos pedaços para evitar Buffer Overflow na placa."""
    dados = texto.encode('utf-8')
    for i in range(0, len(dados), chunk_size):
        s.sendall(dados[i:i+chunk_size])
        time.sleep(delay)

def injetar_arquivo(s, caminho_arquivo):
    nome_arquivo = caminho_arquivo.replace('\\', '/')
    
    print(f"-> Transferindo {nome_arquivo}...")
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Interrompe execução atual (Ctrl+C) e entra no Paste Mode (Ctrl+E)
    s.sendall(b'\x03\x05')
    time.sleep(0.5)

    cmd = ""
    # Se o arquivo estiver numa pasta (ex: umqtt/simple.py), cria a pasta no ESP32
    if '/' in nome_arquivo:
        pasta = nome_arquivo.split('/')[0]
        cmd += f"import os\ntry: os.mkdir('{pasta}')\nexcept: pass\n"

    # Prepara o script de gravação
    cmd += f"with open('{nome_arquivo}', 'w') as f:\n"
    cmd += f"    f.write(r'''{conteudo}''')\n"

    # Digita o código de forma fracionada
    enviar_em_blocos(s, cmd)
    time.sleep(0.5)

    # Executa o Paste Mode (Ctrl+D)
    s.sendall(b'\x04')
    time.sleep(1)
    print(f"   ✓ {nome_arquivo} injetado com sucesso!")

def main():
    print("=========================================")
    print("SCRIPT DE DEPLOY - WOKWI")
    print("=========================================")

    # Busca todos os arquivos .py no diretório
    todos_arquivos = glob.glob("**/*.py", recursive=True)
    arquivos_py = []
    
    # Filtro de segurança: ignora a pasta venv e o próprio script
    for arq in todos_arquivos:
        nome_min = arq.lower()
        if 'venv' not in nome_min and 'env' not in nome_min and 'deploy.py' not in nome_min:
            arquivos_py.append(arq)
            
    # Garante que o main.py seja o último a ser enviado
    if 'main.py' in arquivos_py:
        arquivos_py.remove('main.py')
        arquivos_py.append('main.py')

    if not arquivos_py:
        print("❌ Nenhum arquivo do projeto encontrado para transferir.")
        return

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print(f"Conectado ao Wokwi (Porta {PORT}). Iniciando injeção...\n")

        # Para qualquer loop infinito rodando no ESP32
        s.sendall(b'\x03')
        time.sleep(0.5)

        for arquivo in arquivos_py:
            injetar_arquivo(s, arquivo)

        print("\n✅ Todos os arquivos foram sincronizados!")
        print("Reiniciando a placa (Soft Reboot)...")
        # Envia Ctrl+D no terminal limpo para reiniciar a placa
        s.sendall(b'\x04') 
        s.close()

    except ConnectionRefusedError:
        print("\n❌ ERRO: Conexão recusada.")
        print("Certifique-se de que a simulação no Wokwi está rodando (Play) e aguardando na tela preta.")

if __name__ == '__main__':
    main()