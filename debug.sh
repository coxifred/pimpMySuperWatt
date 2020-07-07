#!/bin/bash

pkill -9 -f "python ./superwatt.py"
nohup ./gradlew debugPython > /dev/null 2>&1 &

tail -100f /tmp/pimpMySuperWatt.log



