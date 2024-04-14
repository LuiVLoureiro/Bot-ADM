import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import json
import os
import pytz

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True 

client = discord.Client(intents=intents)

def save_initial_message(member_name, content, date_time):
    data = {
        "member": member_name,
        "message": content,
        "timestamp": date_time,
        "type": "inicial"
    }
    with open('frequencia.json', 'a', encoding='utf-8') as f:
        json.dump(data, f)
        f.write('\n')

def save_message(member_name, content, date_time):
    data = {
        "member": member_name,
        "message": content,
        "timestamp": date_time,
        "type": "final"
    }
    with open('frequencia.json', 'a', encoding='utf-8') as f:
        json.dump(data, f)
        f.write('\n')

async def schedule_tasks():
    await client.wait_until_ready()
    while not client.is_closed():
        timezone = pytz.timezone('America/Belem')
        now = datetime.now(timezone).strftime('%H:%M')
        print(now)
        if now == '18:00':
            await handle_task('13:24')
        elif now == '21:30':
            await handle_task('11:45')
        await asyncio.sleep(10)  # Sleep for 10 seconds before checking again

async def handle_task(time_str):
    guild = client.get_guild(1212192505240485898)
    member = discord.utils.get(guild.members, name="luiloure1ro")
    channel = client.get_channel(1228673076888080414)
    if member:
        message_prompt = {
            '18:00': 'Por Favor, apenas confirme sua frequência inicial',
            '21:30': 'Por Favor, confirme sua frequência final e descreva abaixo o que fez no dia. [Você tem 5 Minutos]'
        }.get(time_str, 'Undefined task time.')
        
        await channel.send(f'{member.mention} {message_prompt}')
        try:
            msg = await client.wait_for('message', timeout=300, check=lambda m: m.author == member and m.channel == channel)
            await channel.send(f'Dev Joshua confirmou sua frequência para {time_str}')
            await msg.add_reaction('👏')
            save_initial_message(member.display_name, msg.content, str(datetime.now()))
        except asyncio.TimeoutError:
            await channel.send('Dev Joshua não enviou nenhuma mensagem.')
            save_initial_message(member.display_name, "None", datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    else:
        await channel.send("Membro não encontrado.")

@client.event
async def on_message(message):
    if message.content.startswith('!freq'):
        try:
            await message.channel.send(file=discord.File('frequencia.json'))
        except Exception as e:
            await message.channel.send(f"Erro ao enviar o arquivo: {e}")
    elif message.content.startswith('!init'):
        try:
            asyncio.create_task(schedule_tasks())  # Start the task scheduler
        except Exception as e:
            await message.channel.send(f"Erro ao começar a task: {e}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    asyncio.create_task(schedule_tasks())  # Start the task scheduler when bot is ready

client.run(os.getenv('TOKEN_DISCORD'))
