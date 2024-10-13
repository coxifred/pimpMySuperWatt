#!/bin/bash

echo "Welcome to pimpmysuperwatt"

pkill -9 -f "superwatt.py --configFile  superwatt.json"
while [ ! -z $(pgrep -f "superwatt.py --configFile superwatt.json") ]
 do
  echo "Waiting stop"
  sleep 0.5
 done

if [ -z "${GRAFANA_START}" -o "${GRAFANA_START}" = "Y" -a -d /grafana-v11.2.2/bin ]
 then
  echo "Starting grafana in the background"
  cd /grafana-v11.2.2/bin ; ./grafana server --config /grafana-v11.2.2/conf/defaults.ini > /grafana-v11.2.2/data/grafana_start.log 2>&1 &
fi

if [ -z "${INFLUXDB_START}" -o "${INFLUXDB_START}" = "Y" -a -d /influxdb-1.8.10-1 ] 
 then
  echo "Starting influxdb in the background"
  cd /influxdb-1.8.10-1 ;  ./influxd -config /influxdb-1.8.10-1/influxdb.conf > /influxdb-1.8.10-1/data/influxdb_start.log 2>&1 &
fi

sleep 5

cd /pimpmysuperwatt
DEBUG=""
if [ "${PIMP_DEBUG}" = "Y" ] 
 then
  DEBUG="--debug"
fi

echo "Running ./venv/bin/python3 ./superwatt.py --configFile superwatt.json ${DEBUG}"
./venv/bin/python3 ./superwatt.py --configFile superwatt.json ${DEBUG}

echo "Sleeping 30s before exiting"
sleep 30
