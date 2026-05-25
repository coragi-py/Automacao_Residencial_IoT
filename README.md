
# Projeto Acadêmico de Automação Residencial IoT 🏠🔌

Este repositório contém a documentação, firmware e diagramas de um sistema completo de **Automação Residencial (Internet das Coisas - IoT)** baseado no microcontrolador **ESP32** e programado em **MicroPython**. 

O sistema foi concebido de forma altamente modular e robusta, operando de maneira híbrida: oferece uma **interface web de controle local de baixa latência** (HTTP/AJAX) diretamente no chip, e se integra de forma assíncrona a uma **infraestrutura em nuvem** (MQTT/Node-RED) para dashboards, automação complexa, alertas por e-mail e registro histórico de dados (Data Logging) em planilhas digitais.

---

## 🛠️ Stack Tecnológica

* **Core Hardware / Firmware:** ESP32, MicroPython v1.28.
* **Protocolos de Rede:** * **HTTP:** Servidor embarcado assíncrono para controle local via navegador.
    * **MQTT:** Protocolo Pub/Sub leve para telemetria e comandos remotos via Broker Público HiveMQ.
* **Orquestração e Nuvem (Backend):** Node-RED (Processamento de fluxos de automação e regras de negócio).
* **Banco de Dados & Storage:** Google Sheets integrado via Google Apps Script (Web App POST requests).
* **Ambiente de Desenvolvimento & Simulação:** VS Code, Extensão Wokwi Local Simulator, Python 3.

---

## 🔌 Mapeamento de Hardware (GPIOs)

O circuito eletrônico virtual foi mapeado de forma estrita no simulador para garantir a consistência das portas entre o arquivo físico (`diagram.json`) e os drivers do MicroPython.

### Sensores (Entradas)
* **DHT22 (Temperatura e Umidade):** GPIO 15
* **LDR (Sensor de Luminosidade):** GPIO 34 (Leitura Analógica via ADC)
* **PIR (Sensor de Presença/Movimento):** GPIO 13
* **Push Button (Simulador de Contato Porta/Janela):** GPIO 12

### Atuadores (Saídas)
* **LED (Iluminação Principal):** GPIO 2
* **Módulo Relé (Ar-Condicionado / Cargas Pesadas):** GPIO 4
* **Buzzer (Alarme de Intrusão Sonoro):** GPIO 5
* **Display OLED (SSD1306 128x64):** Interface I2C (SCL: GPIO 22 | SDA: GPIO 21)

---

## 🚀 Como Executar o Projeto (Guia Rápido)

### Passo 1: Preparar o Ambiente
1. **Baixe o projeto:** Faça o download deste repositório (ZIP) ou use `git clone`.
2. **Abra a pasta** do projeto no **Visual Studio Code**.
3. Certifique-se de ter instalado: **Python 3**, a extensão **Wokwi Simulator** no VS Code e o **Node-RED** na sua máquina.

### Passo 2: Configurar a Nuvem (Node-RED)
1. Abra o Node-RED (`http://localhost:1880`).
2. Vá no menu > **Import** e selecione os arquivos `node-red-flow.json` e `node-red-alerts.json` desta pasta.
3. Se faltar o nó de e-mail, vá em *Manage Palette*, aba *Install*, e instale o `node-red-node-email`.
4. Dê um duplo clique nos nós de **Email** e **Google Sheets** para colocar suas credenciais e a URL do seu App Script.
5. Clique no botão vermelho **Deploy** no canto superior direito.

### Passo 3: Ligar a Placa Virtual
1. No VS Code, abra o arquivo `diagram.json`.
2. Clique no botão verde de **Play** do Wokwi (ou aperte `F1` > *Wokwi: Start Simulator*).
3. Aguarde o terminal preto do Wokwi carregar e parar na tela com os símbolos `>>>`. **Deixe rodando.**

### Passo 4: Enviar o Código (Deploy Automático)
1. Com a simulação rodando, abra um **Terminal** novo dentro do VS Code.
2. Digite o comando abaixo e aperte Enter:
   ```bash
   
   python deploy.py
3. O script vai enviar todos os arquivos sozinho. Aguarde a placa reiniciar e o terminal mostrar a mensagem: "MQTT Conectado!".

### Passo 5: Testar a aplicação!
Controle Web Local: Abra seu navegador (Chrome/Edge) e acesse http://127.0.0.1:8080. Clique nos botões para ligar/desligar o LED, Relé e Buzzer no simulador.

Dashboard em Nuvem: Acesse http://localhost:1880/ui para ver os gráficos de temperatura e umidade atualizando em tempo real.

Teste de Alarme: No Wokwi, simule movimento clicando no sensor PIR. Você receberá um e-mail de alerta gerado pelo Node-RED!
---

## 📂 Estrutura de Diretórios do Projeto

```text
.
├── diagram.json             # Mapeamento e conexões físicas do hardware virtual no Wokwi
├── wokwi.toml               # Configurações do simulador (Redirecionamento de portas e Firmware)
├── firmware.bin             # Imagem binária estável do MicroPython para o ESP32
├── deploy.py                # Utilitário customizado de automação de sincronização (Socket/Paste Mode)
├── main.py                  # Loop principal não-bloqueante e temporizado do firmware
├── boot.py                  # Inicializador do hardware e conexão à rede Wi-Fi virtual (Wokwi-GUEST)
├── sensors.py               # Módulo isolado de amostragem de dados e debounce de sensores
├── display.py               # Módulo de renderização visual local no painel OLED I2C
├── web_server.py            # Servidor Web assíncrono em bytes com endpoints AJAX/Fetch API
├── mqtt_handler.py          # Gerenciador do ciclo de vida da conexão MQTT (Pub/Sub)
├── ssd1306.py               # Driver de controle do controlador gráfico do Display OLED (Local)
└── umqtt/
    └── simple.py            # Biblioteca estável de comunicação cliente MQTT (Local)
