# Welcome to PimpMySuperWatt repository V2

![Overview](https://github.com/coxifred/PimpMySuperWatt/blob/master/doc/pimpMySuperWatt2.png?raw=true)

# What is it ?

This is the version 2.0, this version is dedicated to Axpert MAx 7.2K owners (Should also work with others models)
This software will drive your inverter, expose & stores metrics (including Pylontech Battery stats)

`InfluxDb` and `Grafana` are embbeded inside the container (Can be disabled).

Version 1.0 still available [here](https://github.com/coxifred/pimpMySuperWatt/tree/1.0)

*The Axpert max 7.2kw looks like this:*

![Axpert-max7.2](https://github.com/coxifred/PimpMySuperWatt/blob/master/doc/axpertMax7-2.png?raw=true)

This inverter contains 1 for communication (RJ45 look).

# What do you need ?

   - ARM Raspberry or AMD64 linux compatible hardware, and a communication cable [communication cable](https://www.amazon.fr/dp/B00QUZY4UG?ref=ppx_yo2ov_dt_b_fed_asin_title)
   - Python 3.9.18 (no guarantee that others versions works, viva Python !)
   - docker/docker-compose for simplicity

# Features:

   - Send all available commands to Axpert Max (All implemented)
   - API exposure (for Domotic/Automation usages)

# Look'n feel:

## Small control-ui (Phone responsive)

![Overview](https://github.com/coxifred/PimpMySuperWatt/blob/master/doc/pimpPhone.png?raw=true)

## Embedded `Grafana` dashboard



# `Docker` installation AMD64

```bash
git clone https://github.com/coxifred/pimpMySuperWatt.git
cd pimpMySuperWatt
docker-compose up
```

# Docker installation ARM (Raspberry)

> To do.

# Installation without `Docker` (You have to manage yourself `Grafana` and `InfluxDb` installations)

> Please use python 3.9.18 (i had trouble with fresh versions)

```bash
git clone https://github.com/coxifred/pimpMySuperWatt.git
cd pimpMySuperWatt
python3 -m venv venv
chmod a+x venv/bin/*
venv/bin/activate
venv/bin/pip3 install -r requirements.txt
./start.sh
```

# Configuration

## Configuration file is superwatt.json

```json
{
        "instance"              : "AxpertMax 7.2K",      <-  Free label
        "debug"                 : true,                  <- debug mode
        "debugClass"            : [],                    <- you can specify custom classes for debug, ie: ["CORE.queryExternalPower","CORE.sendToInflux"]
        "communicationClass"    : "usbConnector",        <- Class connector (usbConnector for the moment)
        "portPath"              : "/dev/ttyUSB0",        <- the port Path
        "webserver"             : true,                  <- If you want a web interface
        "webserverDebug"        : false,                 <- debug web 
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
        "queryPoolingInterval"  : 30,                     <- Inverter will be queried every 30s (min 2s)
        "queryPluginInterval"  : 30                       <- Plugin solicitation    

}
```
## Docker-compose

```yaml
version: "2"
services:
  "pimpmysuperwatt":
    container_name: "pimpmysuperwatt"
    privileged: true
    image: "pimpmysuperwatt:2.0"
    environment:
       # Start or not embedded services
       GRAFANA_START: "Y"
       INFLUXDB_START: "Y"
       # Debug mode, see also debugClass in superwatt.json
       # PIMP_DEBUG: "Y"
    #volumes:
      # Override configuration if needed
      #- /root/pimpmysuperwatt/superwatt.json:/pimpmysuperwatt/superwatt.json
      #- /root/pimpmysuperwatt/plugins/solarposition/solarposition.json:/pimpmysuperwatt/plugins/solarPosition/solarposition.json

      # Persist your influxdb data
      #- /root/pimpmysuperwatt/influxdb/data:/influxdb-1.8.10-1/data

      # Persist your grafana modifications
      #- /root/pimpmysuperwatt/grafana/data:/grafana-v11.2.2/data
     
      
    restart: always
    ports:
      # PimpMySuperWatt UI
      - "61000:61000"
      # Grafana dashboard
      - "61001:3000"
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0
```
# Web Interface

Simply connect with:

- [x] http://<your_ip>:61000 and wait for informations
- [x] http://<your_ip>:61001 for grafana dashboard

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

# Troubleshootings:

> Log says can't connect to usb

  Wait at least to the 40 tries, sometimes, it takes time to connect.

> No data available in `Grafana` dashboard

  Wait at least 5mn after docker start.


# TODO:

- [] Raspberry `Docker` build.
- [] Enable/Disable debug from UI.
- [] Events history diplay on UI.
