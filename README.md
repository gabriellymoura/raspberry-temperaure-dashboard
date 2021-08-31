# raspberry-temperaure-dashboard

#### Requisitos / Antes de rodar...
  * MQTT Broker no Raspberry Pi.
  * Rodar o arquivo Python Server no Raspberry Pi:
  * Instalar Flask
  * Instalar Paho-MQTT
  * Instalar SocketI
       * **se por acaso der erro por falta de instação d biblioteca, instalar na raiz do projeto**
* Configurar SQLite
  * Criar banco
  * Criar tabela com as colunas

## 1. Rodando o projeto...

``` pyhton
python3 app.py
```

##### Referências:

[How to Install Mosquitto Broker on Raspberry Pi](https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/)
<br>
[ESP8266 Publishing DHT22 Readings with MQTT to Raspberry Pi](https://randomnerdtutorials.com/esp8266-publishing-dht22-readings-with-mqtt-to-raspberry-pi/)
<br>
[SQLite Database on a Raspberry Pi](https://randomnerdtutorials.com/sqlite-database-on-a-raspberry-pi/)
<br>
[ESP8266 Publishing DHT22 Readings to SQLite Database](https://randomnerdtutorials.com/esp8266-publishing-dht22-readings-to-sqlite-database/)
