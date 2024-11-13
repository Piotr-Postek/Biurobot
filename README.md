# Discord bot using raspberryPi 3
## About
This is a simple program to run on your Raspberry Pi to find out if your office is open or closed.  The RPI uses Bluetooth to find beacons and return the status to the Discord app when you send the **/biuro** command.

The project is divided into two files. The first is responsible for communication on the discord channel, and the second is a simple scanner that writes the response to the output file. In this case, dividing the program into two scripts guarantees an immediate response after the command and with a scanning interval set to 1 minute.

General principle of operation. DiscordBot service is running on the device and the scanning script is run via cron every 1 minute. The scanning script saves the result in the data;status format in the output file. The discord script reads the last line in this file and based on it returns the office status in the application.


### Dependencies
- [discord.py](https://github.com/Rapptz/discord.py)
- Python3.12
- Bluepy3

## Discord APP

1. Go to [dev.discord](https://discord.com/developers/applications)
2. Create an application
3. Go to OAuth2 
	- Set the scope to bot
    ![image](https://github.com/user-attachments/assets/c4dbb0aa-a279-4770-bfb0-5d6c21765cd9)
    - Set the bot permision as below
    ![image](https://github.com/user-attachments/assets/4179c727-41b8-448c-a9bd-4205ee7e471e)
    - Copy the generated URL and run it in yout browser, then install the bot on your server
      ![image](https://github.com/user-attachments/assets/97987ab5-5632-44d4-97f9-a1bb39bf752b)
4. In the bot panel set
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
    ![image](https://github.com/user-attachments/assets/828b1eac-545b-434b-9d3b-988e5d92cad4)
5. After completing all steps, copy your token and paste it into the script on rpi
   ![image](https://github.com/user-attachments/assets/00250f80-3fd5-48e9-a360-2ee27c058a42)



# Prepare system requirements

### System update
``` 
apt-get update
apt-get upgrade
apt-get dist-upgrade
```
### Install packages
```
apt-get install libssl-dev
apt-get install libffi-dev
apt-get install libsqlite3-dev
```
### Install Pyhon3.12
1.  Download and unzip packages
```
	wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
	tar -xf Python-3.12.0.tgz
```
2.  Go to python location and run configuration file
```
	cd Python-3.12.0
	./configure --enable-optimizations
```
3. Run make command
```
	make -j 8
	make altinstall
```
4. Verify installation
```
	python3.12 --version
```
5. Install python pip
```
	sudo apt install python3-pip
```
---
## Install [discord.py](https://github.com/Rapptz/discord.py) library 
1. Oficial release
	- python3 -m pip install -U discord.py
2.  Install development version
	- git clone https://github.com/Rapptz/discord.py
	- cd discord.py
	- python3 -m pip install -U .[voice]

# First use
Add header line to use discord lib
```
import discord
from discord.ext import commands
```
Set up intents and create bot
```
# Set up intents
intents = discord.Intents.default()  # Default intents, but you can enable more as needed
intents.message_content = True  # Allow the bot to read message content

# Create bot instance with intents
bot = commands.Bot(command_prefix='/', intents=intents)
```
Add line to show logged user
```
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
```
Add first command
```
@bot.command()
async def hello(ctx):
    await ctx.send('Hello World!!!')
```
Start your Bot
```
bot.run(bot_token)
```

Run your bot in console 
>$ python3.12 discord_bot.py

# Prepare service

```
Description=DiscordBot					# service name
Wants=network.target
After=syslog.target network-online.target

[Service]
WorkingDirectory=/home/rpi/discord.bot	#script working directory
User=root								# run as a root
ExecStart=/usr/bin/python3.12 /home/rpi/discord.bot/discord-bot.py
Restart=on-failure						# service will restart after fail
RestartSec=10							# restart interval
KillMode=process
StandardOutput=null

[Install]
WantedBy=multi-user.target
```

Create service file in ```/etc/systemd/system/<name>.service```. 

```ExecStart=/usr/bin/python3.12 /home/rpi/discord.bot/discord-bot.py``` - this path is responsible for run script. ```/usr/bin/python3.12``` is location, where is installed python, ```/home/rpi/discord.bot/discord-bot.py``` is script location.

# Scanner

Import file dependencies
```
from datetime import datetime
from bluepy.btle import Scanner
```

Function to write result into file
```
def add_entry_to_file(filename, message):
    with open(filename, "a") as file:
        file.write(message)
        file.flush()
```

Get actual time
```
def  get_current_time_formatted():
	#Get the current time formatted as a string.
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```
Scanner
```
def  scan_devices(scan_time=10.0):
	# Scan for devices for a specified duration.
	scanner =  Scanner()
	return scanner.scan(scan_time)
```

Example of implementation logic
```
def  check_device_by_mac(target_mac,  devices,  log_file):
	# Check if a device with the target MAC address is in the scanned devices and log the result.
	found =  False

	for dev in devices:
		print(f"Found device: {dev.addr}")

		if dev.addr.lower()  == target_mac.lower():
			found_message =  f"Device with MAC address {target_mac} found!\n"
			print(found_message,  end="")
			status_message =  "true\n"
			write_message =  f"{get_current_time_formatted()};{status_message}"
			add_entry_to_file(log_file, write_message)
			found =  True
			break
			
	if  not found:
		not_found_message =  f"Device with MAC address {target_mac} not found.\n"
		print(not_found_message,  end="")
		status_message =  "false\n"
		write_message =  f"{get_current_time_formatted()};{status_message}"
		add_entry_to_file(log_file, write_message)
```

Usage
```
target_mac =  "EE:EE:EE:EE:EE:EE"  # Replace with the target BLE MAC address
devices =  scan_devices()
check_device_by_mac(target_mac, devices, log_file)
```

# Cron
```
######################################################################
#  * * * * * --- command
#  _ _ _ _ _
#  | | | | |
#  | | | | ----- week day    ( 0 - 7 )
#  | | | ------- month       ( 1 - 12 )
#  | | --------- month day   ( 1 - 31 )
#  | ----------- hour        ( 0 - 23 )
#  ------------- min         ( 0 - 59 )

*/1 * * * * /path/to/your/script
```

