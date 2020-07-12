echo "bash -x $(pwd)/start.sh 2>/tmp/error_PimpMySuperwatt.log" > /etc/rc3.d/S01pimpMySuperWatt.sh
chmod a+x /etc/rc3.d/S01pimpMySuperWatt.sh
echo "Autostart activated in /etc/rc3.d/S01pimpMySuperWatt.sh"
echo "To remove just delete /etc/rc3.d/S01pimpMySuperWatt.sh"
