import discord
import re
import json
import os
import time
client = discord.Client()

token = '

Config = json.load(open("config.json"))

PREFIX = Config["PREFIX"]

print(PREFIX)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    PREFIX = Config["PREFIX"]

    if message.author == client.user:
        return

    content = message.content.lower()
    args = message.content.split(" ")

    for arg in args:
        args[args.index(arg)] = arg.replace(PREFIX, "").lower()

    # print(args)

    if args[0] == "help":
        await help(message)
    elif args[0] == "ping":
        await ping(message)
    elif args[0] == "members":
        await message.channel.send("***ALL MEMBERS: ***" + str(message.guild.member_count))
    elif args[0] == "prefix":
        if len(args) >= 2:
            await setprefix(message, args[1])

        else:
            await prefix(message)
    elif args[0] == "send":
      if len(args) >= 2:
        await send(message, args)
    else:
      if content.startswith(PREFIX):
        await message.channel.send("Unknown Command!")
    
    args = []

async def on_member_join(member):
    print(member + " has joined")

async def ping(message):
    before = time.monotonic()
    msg = await message.channel.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await msg.edit(content=f"Pong!  `{int(ping)}ms`")

pack = ""

async def send(message, args):
    pack = ""
    for arg in args:
      if len(args) >= 2:
        pack = pack + " " + arg
    
    await message.channel.send(pack.replace("send ", ""))

async def help(message):
    embedVar = discord.Embed(title="**Help**", description="Bot Prefix: " + PREFIX, color=0x2E9AFE)
    embedVar.add_field(name="**General**", value="`help`, `members`, `ping`", inline=False)
    embedVar.add_field(name="**Moderation**", value="`kick`, `ban`, `unban`, `prefix`, `send`", inline=False)
    embedVar.add_field(name="*Server Members: " + str(message.guild.member_count) + "*", value="*ARIYA1234GAMER bot*")
    await message.channel.send(embed=embedVar)

async def prefix(message):
    await message.channel.send("Use " + PREFIX + "prefix [NewPrefix] To Change Prefix")

async def setprefix(message, arg):
    Config["PREFIX"] = arg
    await message.channel.send("Prefix changed To: **" + arg + "**")
    print(Config["PREFIX"])
    PREFIX = Config["PREFIX"]

client.run(token)
