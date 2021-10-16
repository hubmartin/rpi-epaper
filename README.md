# Raspberry PI e-paper network display

Create a screenshot of a webpage on your server and send it over SCP to the Raspberry Pi to display on the screen or e-paper

## Installation

```
cd ~
git clone https://github.com/hubmartin/rpi-epaper.git
cd rpi-epaper
```

## Usage

The project has `/server` an `/client` part/folders.

Server should run on your home server, client part is run on the Raspberry Pi where your ePaper is connected.

## Server

Use `/server/display.py` file to load a webpage with Selenium headless web browser, create a PNG image and send it to the device IP.
The script is using data from czech webserver for Czech Republic. You'll probably need to completely rewrite this script or find other weaher service which fits all data nicely on single small screen.

You can set `crontab` to periodically every 15 minute update screen

```
crontab -e
```

Then add this line:

```
*/15 * * * * ~/rpi-epaper/server/display.py
```

## Client

Client part waits for `client/image.png` to change, then it reloads picture to the epaper.

For running in background you can use PM2 process manager and set `client/epaper.py` to run after boot.

```
cd ~/rpi-epaper/client
pm2 start $(pwd)/epaper.py --name rpi-epaper-client --interpreter python3
pm2 save
```

## Raspberry Pi Zero W issues with WaveShare Smart Reset

WaveShare driver assumes that Python is realtime, which is not. So slow Rpi Zero sometimes does longer reset pulse and that causes power disconnect. I did some hardware modifiations. Also it wires 5 V directly to 3.3V GPIO which this hardware modification also fixes.

you may be running fine, but time from time when the Python script is run as a background service (with probably lower priority) and wireless transfer the Rpi has no time to generate precise Python pulses.

https://www.martinhubacek.cz/blog/waveshare-epaper-hat-issues/

## Rpi clean install steps

```
sudo raspi-config #enable SPI
sudo apt update
sudo apt install git python3-pip libopenjp2-7 libtiff5

pip3 install --upgrade setuptools
sudo pip3 install netifaces Pillow watchdog

git clone https://github.com/hubmartin/rpi-epaper.git

# Use systemd instead of pm2 which runs slow on Rpi Zero W/arm6
sudo cp rpi-epaper/client/epaper.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl start epaper.service
sudo systemctl enable epaper.service
```

