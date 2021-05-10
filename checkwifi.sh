# This small program pings the IP address of the local router once, and then checks if the ping returns as "True". If not, it shuts down the Pi's WiFi connection and then starts it again to reconnect. Otherwise, a success message is logged to the "log" file.
# This code is heavily based on code from this blog post by Thijs Bernolet: https://weworkweplay.com/play/rebooting-the-raspberry-pi-when-it-loses-wireless-connection-wifi/
ping -c1 192.168.0.1 > /dev/null
if [ $? != 0 ]
then
  echo "No network connection, restarting wlan0" >> /home/pi/log
  ip link set wlan0 down
  sleep 5
  ip link set wlan0 up
else
  echo "Network appears to be up!" >> /home/pi/log
fi
