TEMP=$(cat /sys/bus/w1/devices/28-031590486eff/w1_slave | grep -o -e "[0-9]\+$")

echo $TEMP
