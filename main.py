# This example requires the 'message_content' intent.

import discord
from discord.ext import commands, tasks
from datetime import datetime
import asyncio
import json
import os

print('TESTE')

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

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

@tasks.loop(seconds=1)  # Roda a tarefa uma vez a cada 24 horas
async def daily_task():
    tempo = datetime.now().time().strftime('%H:%M')
    print(tempo)
    if tempo == '18:00':
        guild = client.get_guild(1212192505240485898)
        member = discord.utils.get(guild.members, name="dark_player16.")
        channel = client.get_channel(1228673076888080414)
        if member:
            await channel.send(f'{member.mention} Por Favor, apenas confirme sua frequência inicial')
            try:
                def check(m):
                    return m.author == member and m.channel == channel

                # Espera por uma resposta por 5 minutos
                msg = await client.wait_for('message', timeout=300, check=check)
                if msg:
                    data = datetime.now().timetuple()
                    data_hoje = str(datetime.now())
                    await channel.send(f'Dev Joshua confirmou sua frequência inicial')
                    await msg.add_reaction('👏')
                    save_initial_message(member.display_name, msg.content, data_hoje)
            except asyncio.TimeoutError:
                await channel.send('Dev Joshua não enviou nenhuma mensagem.')
                save_initial_message(member.display_name, "None", datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        else:
            await channel.send("Membro não encontrado.")
        await asyncio.sleep(60)

    elif tempo == '11:':
        guild = client.get_guild(1212192505240485898)
        member = discord.utils.get(guild.members, name="dark_player16.")
        channel = client.get_channel(1228673076888080414)
        if member:
            await channel.send(f'{member.mention} Por Favor, confirme sua frequência final e descreva abaixo o que fez no dia. [Você tem 5 Minutos]')
            try:
                def check(m):
                    return m.author == member and m.channel == channel

                # Espera por uma resposta por 5 minutos
                msg = await client.wait_for('message', timeout=300, check=check)
                if msg:
                    data = datetime.now().timetuple()
                    data_hoje = str(datetime.now())
                    await channel.send(f'Dev Joshua enviou a mensagem e registrou sua frequencia em ***{data[2]}/{data[1]}/{data[0]}*** as ***{data[3]} Horas***')
                    await msg.add_reaction('👏')
                    save_message(member.display_name, msg.content, data_hoje)
            except asyncio.TimeoutError:
                await channel.send('Dev Joshua não enviou nenhuma mensagem.')
                save_message(member.display_name, "None", str(datetime.now()))
        else:
            await channel.send("Membro não encontrado.")
        await asyncio.sleep(60)
        
        
    

@client.event
async def on_message(message):
    if message.content.startswith('!freq'):
        try:
            # Envia o arquivo frequencia.json diretamente
            await message.channel.send(file=discord.File('frequencia.json'))
        except Exception as e:
            # Envie uma mensagem de erro se o arquivo não puder ser enviado
            await message.channel.send(f"Erro ao enviar o arquivo: {e}")
        
        

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    daily_task.start() 


tempo = datetime.now().time().strftime('%H:%M')
print(tempo)

client.run(os.getenv('TOKEN_DISCORD'))