## Intro
This folder contains the Python code I used to run a catfeeder I created for my two cats on a raspberryPi.

## Run script on raspberryPi
To run the script and feed the cats every morning and evening at 7am and 7pm, add a crontab job with following line  

`0 7,19 * * * /usr/bin/python /home/pi/catfeeder/run.py`

