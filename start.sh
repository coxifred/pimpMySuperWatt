#!/bin/bash

pkill -9 -f "python ./superwatt.py"
pkill -9 -f "python3 ./superwatt.py"
nohup ./gradlew runPython > /dev/null 2>&1 &

tail -100f /tmp/pimpMySuperWatt.log



