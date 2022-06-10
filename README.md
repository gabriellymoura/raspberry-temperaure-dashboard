# raspberry-temperaure-dashboard

#### Requisitos / Antes de rodar...

- MQTT Broker no Raspberry Pi.
- Rodar o arquivo Python Server no Raspberry Pi:
  - Instalar Flask
  - Instalar Paho-MQTT
  - Instalar SocketI
    - **se por acaso der erro por falta de instação d biblioteca, instalar na raiz do projeto**
- Configurar SQLite
  - Criar banco
  - Criar tabela com as colunas

## 1. Rodando o projeto...

```pyhton
python3 app.py
```

## 2. Criando ou acessando o banco de dados...

**dados de exemplo:**

- maria db
- user: root
- password: root
- DATABASE: databaseMain
- TABLE: tableMain

```
sudo mysql -u root -p
> USE DATABASE databaseMain;
[dataBaseMain]> USE TABLE tableMain;
[dataBaseMain]> SELECT * FROM tableMain;
```

## 3. Alternando entre o WiFi e o Hotspot...

- 1 - entrar no arquivo **sudo nano /etc/wpa_supplicant/wpa_aupplicant.conf**
- 2 - alterar o nome do wifi add/removendo off no final (exemplo: moura -> mouraoff)
  - 2.1 - colocar o off para habilitar o hotspot, retirar (nome do wifi normal) para utilizar o wifi
  - 2.2 - salvar
- 3 - ativar usando **sudo chmod +x /usr/bin.autohotspotN**
- 4 - ativar usando **sudo systemctl enable autohotspot.service**

##### Referências:

[How to Install Mosquitto Broker on Raspberry Pi](https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/)
<br>
[ESP8266 Publishing DHT22 Readings with MQTT to Raspberry Pi](https://randomnerdtutorials.com/esp8266-publishing-dht22-readings-with-mqtt-to-raspberry-pi/)
<br>
[SQLite Database on a Raspberry Pi](https://randomnerdtutorials.com/sqlite-database-on-a-raspberry-pi/)
<br>
[ESP8266 Publishing DHT22 Readings to SQLite Database](https://randomnerdtutorials.com/esp8266-publishing-dht22-readings-to-sqlite-database/)
