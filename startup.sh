#!/bin/sh

while true
do
	# Start
	echo "Press CTRL+C to stop the script execution"
	cd /
	cd /home/pi/led-sign/

	echo "Wait for internet"
	sudo ./startup.py --led-cols=64 --led-brightness=50 > ./output.log 2>&1

	echo "Show downloading on sign"
	sudo ./awaiting-git.py --led-cols=64 --led-brightness=50 &

	echo "Pull from Git"
	cd /home/pi/led-sign/LED-sign/
	git pull
	sudo killall "python"

	echo "Start script"
	sudo ./sign.py --led-cols=64 --led-brightness=50 > ./output.log 2>&1

	echo "Restart"
	cd /
done
