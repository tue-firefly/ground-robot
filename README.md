# ground-robot
Who needs wings when you have wheels? - Or scripts for working with the ground robots.

## Contents
Some of the more important scripts:
* `remote_control.py` This runs on the Raspberry Pi, and allows you to control the ground robot over UDP
* `manual_control.py` Allows you to control a ground robot with the WASD keys. You can run this script on both the Raspberry Pi as well as locally. Pass as the first parameter either the IP of the ground robot to connect to, or the serial port of the arduino if you attach it directly to your development machine.
* `deploy/deploy.py` This python script can scan your LAN for ground robots and deploy `remote_control.py` and other required scripts to all of them. More on this in **Getting Started**
* `test-controller/controller.py` Container a very rudimentary set-point controller for a single robot, it relies on [topcam-tracker](https://github.com/tue-firefly/topcam-tracker) to obtain the position of the ground robot.

## Ground robot preparation
The SD cards of the Ground robots should already have a *volatile* Raspbian image flashed, which makes it safe to turn them off with the power switch without a proper shutdown. However, this also implies that all changes you make while the Pi's are on will be **deleted** once you power them off, so do not store your progress on the SD cards.
The volatile image is not yet publicly available, but in time this will be addressed.

## Getting started
1. First you need to install the following dependencies:
  * [Python 3](https://python.org)
  * paramiko (install using pip, run `pip install paramiko` in a terminal)
  * pyserial (`pip install pyserial`)
2. Make sure your ground robots are switched on, and that they are connected to the same network as your development machine.
3. Run `python3 deploy/deploy.py` and follow the on-screen prompts to deploy `remote_control.py` to all Pi's. 
  * If this is the first time you deploy since turning the Pi's on, a few required dependencies will be automatically installed. To do this the Pi's have to connect to the internet via the `Tue-Guest` network, wait for them to return to the original network. If you run the deploy script again after 2 minutes they should re-appear in the list of robots found. accept the prompt and re-deploy.
4. Once the deployment succeeds (typically in about 15 seconds) the motors will make a buzzing tune to signal they are ready to receive commands. run `python3 manual_control.py <IP>` and drive them around to make sure that everything works as expected

## Development
### Arduino controller
You need to use [this controller](https://github.com/tue-firefly/omnibot-controller) with the `remote_control.py` script. The deploy scripts can automatically flash a new version of the controller to all robots if clone this repository and the above mentioned repo according to this directory structure:
```
some-directory/
  ground-robot/
  omnibot-controller/
```
After saving you changes to `omnibot-controller/controller/controller.ino`, if you run `python3 deploy/deploy.py` the deploy script will find the arduino script and instruct all Pi's to flash it to their attached Arduino.

### `remote_control.py`
Save you changes and redeploy using `python3 deploy/deploy.py`, after you hear the buzzing sound all your Pi's will run the new remote_control.py.

#### Debugging
connect to the Pi in question via ssh. 
To check whether or not the `remote_control` script is running, you can run `sudo systemctl status remote_control`.

To show the logs execute `sudo journalctl -u remote_control`. This contains an installation log and any crashes of the python script. **N.B. remote_control.py will automatically try to restart if a crash occurs**. Once you believe to have fixed the issue, you can redeploy and the new version will start.
