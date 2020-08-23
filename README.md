# Welcome to PimpMySuperWatt repository

![Overview](https://github.com/coxifred/PimpMySuperWatt/blob/master/doc/pimpMySuperWatt.png?raw=true)

# What is it ?

This little software allows you to retrieve parameters and real-time status of an inverter. Compatible with superWatt VM2 inverter also knows Voltronic Axpert VMII (3K/5K).

*It's look like this:*

![SuperWatt-VM2](https://github.com/coxifred/PimpMySuperWatt/blob/master/doc/superwatt-vm2.png?raw=true)

This inverter contains 2 ports for communication (USB and Serial). This program works (for the moment) with USB cable.

# What do you need ?

   - Raspberry or linux compatible hardware, and an usb cable.
   - Java for gradle dependencies resolutions.
   - Python 3.7.3 (no guarantee that others versions works, viva Python !)

# How to install/launch

```bash
git clone https://github.com/coxifred/pimpMySuperWatt.git
cd pimpMySuperWatt
./start.sh or ./debug.sh
```
output:

```bash

> Task :python:checkPython
Using python 3.7.3 from /root/pimpMySuperWatt/python/.gradle/python (.gradle/python/bin/python)
Using pip 20.1.1 from /root/pimpMySuperWatt/python/.gradle/python/lib/python3.7/site-packages/pip (python 3.7)

> Task :python:runPython
[python] .gradle/python/bin/python ./superwatt.py --debug superwatt.json
         2020-07-07 22:57:11.934332 [MainThread] INF CORE Instanciate Singleton
         2020-07-07 22:57:12.101406 [MainThread] INF CORE Starting PimpMySuperWatts on pimpMySuperWatt
         2020-07-07 22:57:12.102219 [MainThread] INF CORE Analysing arguments
         2020-07-07 22:57:12.114759 [MainThread] INF CORE Debug activated
         2020-07-07 22:57:12.141037 [MainThread] INF CORE Config file exist /root/pimpMySuperWatt/python/superwatt.json
```

* Note 1: start.sh or debug.sh launch gradlew in background (nohup).
* Note 2: A log is created under /tmp and named superwatt.log
* Note 3: stop.sh to stop it.

# Configuration

Configuration file is superwatt.json

```json
{
        "instance"              : "SuperWatt Garage",    <-  Free label
        "debug"                 : true,                  <- debug mode 
        "communicationClass"    : "usbConnector",        <- Class connector (usbConnector for the moment)
        "portPath"              : "/dev/ttyUSB0",        <- the port Path
        "webserver"             : true,                  <- If you want a web interface
        "webserverDebug"        : true,                  <- debug web 
        "webClass"              : "site",                <- Class for app web.
        "httpBind"              : "0.0.0.0",             <- Binding ip address for web
        "httpPort"              : 60000,                 <- Port for http interface      
        "mqttServers"           : [                      <- If you want to publish to a mqtt broker (or multiples)
                                   {
                                    "mqttServer"     : "192.168.2.30",
                                    "mqttServerPort" : 1883,
                                    "mqttTopic"      : "pimpMySuperWatt/superWattGarage"
                                   }
                                  ],
        "influxDbUrls"          : [                      <- If you want to push results in an influxDb instance (or multiples)
                                   {
                                    "username"  : "root",
                                    "password"  : "root",
                                    "dbName"    : "pimpMySuperWatt",
                                    "dbHost"    : "192.168.2.51",
                                    "dbPort"    : "8086"
                                   }
                                  ],
        "queryPoolingInterval"  : 30                     <- Inverter will be queried every 30s 
}
```

# Web Interface

Simply connect with http://<your_ip>:60000, and wait for informations

API available (See buttons)

![SuperWatt-VM2](https://github.com/coxifred/PimpMySuperWatt/blob/master/doc/Screenshot_web.jpg?raw=true)

# InfluxDb and Grafana Dashboard Demo

Here is a sample dashboard for grafana. <a href=https://raw.githubusercontent.com/coxifred/pimpMySuperWatt/master/doc/pimpMySuperWatt_GrafanaDashboard.json>Click here</a> to download it.

See the demo ? login guest password guest [Click here for DEMO](http://gorilla.ddns.net:3000/d/9NvfTYMMk/pimpmysuperwatt?orgId=1&refresh=30s)

![Grafana](https://github.com/coxifred/pimpMySuperWatt/blob/master/doc/grafana.jpg?raw=true)

# Plugins

  * **solarPosition**
    
    Provides to influxDb sun azimuth and zenith. Just fill python/plugins/solarPosition/solarPosition.json file with your latitude and longitude.
    
    ```json
    {
        "latitude"              : 47.0000,
        "longitude"             : 6.0000,
        "dst"                   : 1
    }
    ```
    
    See azimut and zenith in Grafana with your pv production :
    
    ![SolarPosition](https://github.com/coxifred/PimpMySuperWatt/blob/master/doc/solar_position.jpg?raw=true)

# Docker installation:

  *Create your own configuration:*
  
    - /superwatt.json
    - /solarposition.json

  *Create this docker compose file:*
  
  ```bash
  version: "2"
  services:
  "pimpmysuperwatt":
    privileged: true
    image: "coxifred/pimpmysuperwatt"
    container_name: "pimpmysuperwatt"
    restart: always
    ports:
      - "61000:60000"
    volumes:
      - /superwatt.json:/superwatt.json
      - /solarPosition.json:/plugins/solarPosition/solarPosition.json
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0
  ```
  
  *Then simply run:* 
  
  ```bash
  docker-compose up -d
  ```
  
  Should be running under http://<your_host>:61000
