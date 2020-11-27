# ComAdd
This script prevent you from distractions

## How this work?
The scripts will kill the programs in blocklist if they exist, add websites in blocklist to hostfile and track the usuage time of them.
<br>Between the session, there will be a small break for you.

## Requirement
- Python 3.7

## Installation
```bash
git clone https://github.com/raspiduino/comadd.git
cd comadd
pip install pywin32 matplotlib numpy==1.19.3
sudo apt-get install -y xdotool # If you are on Linux
comadd.py
```
</br>Note: You need to change the setting the first time you use this script.
### Install the extension
- Goto chrome://extensions/ and click Developer mode
- Click on Load unpacked and choose the extension folder in the repo
- Done!

## Warnings
- You need to run this script as <b>Administrator</b>/<b>root</b>
- Some time the Windows Defender may warn this script as <b><i>HostsFileHijack</i></b>. This is wrong positive because this script need to edit the hostfile for blocking websites in block list. So allow the script to do that. <br>Note: if you see another program flag at this, be careful that it maybe the true virus. So please backup your hostfile.

## License
Under <a href="https://github.com/raspiduino/comadd/blob/master/LICENSE">GPL-v3</a>
