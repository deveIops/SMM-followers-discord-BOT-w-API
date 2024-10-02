import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SMMFOLLOWS_API_KEY = os.getenv('SMMFOLLOWS_API_KEY')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

CHANNEL_IDS_TO_REACT = [id salon auto react]
CUSTOM_EMOJI_ID = emoji que le bot va autoreact

intents = discord.Intents.default()
intents.message_content = True  
intents.presences = True  
intents.members = True 

bot = commands.Bot(command_prefix='!', intents=intents)

client_number = 0

USD_TO_EUR_CONVERSION_RATE = 0.85

def extract_tiktok_username(target: str) -> str:
    if target.startswith("https://www.tiktok.com/@") or target.startswith("https://tiktok.com/@"):
        return target.split('@')[-1]
    return target

def extract_instagram_username(target: str) -> str:
    if target.startswith("https://www.instagram.com/") or target.startswith("https://instagram.com/"):
        return target.rstrip('/').split('/')[-1]
    return target

def extract_twitch_username(target: str) -> str:
    if target.startswith("https://www.twitch.tv/") or target.startswith("https://twitch.tv/"):
        return target.rstrip('/').split('/')[-1]
    return target

async def check_order_status(order_id, channel_id, link, amount):
    api_url = "https://smmfollows.com/api/v2"
    payload = {
        'key': SMMFOLLOWS_API_KEY,
        'action': 'status',
        'order': order_id
    }

    response = requests.post(api_url, data=payload)

    try:
        result = response.json()
    except ValueError:
        return

    if result.get('status') == 'Completed':
        charge_usd = float(result.get('charge', 0))
        charge_eur = charge_usd * USD_TO_EUR_CONVERSION_RATE

        channel = bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title="Commande terminée",
                description=f"{amount} followers envoyés avec succès vers : [{link}]({link})",
                color=discord.Color.green()
            )
            embed.add_field(name="Charge", value=f"{charge_eur:.2f} EUR", inline=True)
            await channel.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def tiktok(ctx, amount: int, target: str):
    await ctx.message.delete()
    global client_number
    client_number += 1 
    username = extract_tiktok_username(target)
    link = f"https://www.tiktok.com/@{username}"

    api_url = "https://smmfollows.com/api/v2"
    payload = {
        'key': SMMFOLLOWS_API_KEY,
        'action': 'add',
        'service': 13829,
        'link': link,
        'quantity': amount
    }

    response = requests.post(api_url, data=payload)

    try:
        result = response.json()
    except ValueError:
        await ctx.send("Erreur : Réponse invalide de l'API SMMFollows.")
        return

    if 'order' in result:
        order_id = result['order']
        embed = discord.Embed(
            title="Commande de followers TikTok passée avec succès",
            description=f"Votre commande de {amount} followers pour [{username}]({link}) a été passée.",
            color=discord.Color.from_rgb(255, 255, 255)
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="Quantité", value=amount, inline=True)
        embed.add_field(name="Cible", value=f"[{username}]({link})", inline=True)
        embed.add_field(name="Temps estimé", value="Varie en fonction de la charge du serveur", inline=True)

        await ctx.send(embed=embed)

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await channel.send(
                f"Client numéro {client_number}\n"
                f"[Lien TikTok]({link})\n"
                f"Quantité envoyée : {amount}\n"
                f"Date : {date_str}"
            )
        
        bot.loop.create_task(check_order_status(order_id, CHANNEL_ID, link, amount))
    else:
        embed = discord.Embed(
            title="Erreur lors de la commande",
            description="Une erreur est survenue lors de la tentative de passer votre commande.",
            color=discord.Color.red()
        )
        embed.add_field(name="Détails", value=result.get('error', 'Erreur inconnue'), inline=False)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def insta(ctx, amount: int, target: str):
    await ctx.message.delete()
    global client_number
    client_number += 1 
    username = extract_instagram_username(target)
    link = f"https://www.instagram.com/{username}"

    api_url = "https://smmfollows.com/api/v2"
    payload = {
        'key': SMMFOLLOWS_API_KEY,
        'action': 'add',
        'service': 12811,
        'link': link,
        'quantity': amount
    }

    response = requests.post(api_url, data=payload)

    try:
        result = response.json()
    except ValueError:
        await ctx.send("Erreur : Réponse invalide de l'API SMMFollows.")
        return

    if 'order' in result:
        order_id = result['order']
        embed = discord.Embed(
            title="Commande de followers Instagram passée avec succès",
            description=f"Votre commande de {amount} followers pour [{username}]({link}) a été passée.",
            color=discord.Color.from_rgb(255, 255, 255)
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="Quantité", value=amount, inline=True)
        embed.add_field(name="Cible", value=f"[{username}]({link})", inline=True)
        embed.add_field(name="Temps estimé", value="Varie en fonction de la charge du serveur", inline=True)

        await ctx.send(embed=embed)

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await channel.send(
                f"Client numéro {client_number}\n"
                f"[Lien Instagram]({link})\n"
                f"Quantité envoyée : {amount}\n"
                f"Date : {date_str}"
            )
        
        bot.loop.create_task(check_order_status(order_id, CHANNEL_ID, link, amount))
    else:
        embed = discord.Embed(
            title="Erreur lors de la commande",
            description="Une erreur est survenue lors de la tentative de passer votre commande.",
            color=discord.Color.red()
        )
        embed.add_field(name="Détails", value=result.get('error', 'Erreur inconnue'), inline=False)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def twitch(ctx, amount: int, target: str):
    await ctx.message.delete()
    global client_number
    client_number += 1 
    username = extract_twitch_username(target)
    link = f"https://www.twitch.tv/{username}"

    api_url = "https://smmfollows.com/api/v2"
    payload = {
        'key': SMMFOLLOWS_API_KEY,
        'action': 'add',
        'service': 7764,
        'link': link,
        'quantity': amount
    }

    response = requests.post(api_url, data=payload)

    try:
        result = response.json()
    except ValueError:
        await ctx.send("Erreur : Réponse invalide de l'API SMMFollows.")
        return

    if 'order' in result:
        order_id = result['order']
        embed = discord.Embed(
            title="Commande de followers Twitch passée avec succès",
            description=f"Votre commande de {amount} followers pour [{username}]({link}) a été passée.",
            color=discord.Color.from_rgb(255, 255, 255)
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="Quantité", value=amount, inline=True)
        embed.add_field(name="Cible", value=f"[{username}]({link})", inline=True)
        embed.add_field(name="Temps estimé", value="Varie en fonction de la charge du serveur", inline=True)

        await ctx.send(embed=embed)

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await channel.send(
                f"Client numéro {client_number}\n"
                f"[Lien Twitch]({link})\n"
                f"Quantité envoyée : {amount}\n"
                f"Date : {date_str}"
            )
        
        bot.loop.create_task(check_order_status(order_id, CHANNEL_ID, link, amount))
    else:
        embed = discord.Embed(
            title="Erreur lors de la commande",
            description="Une erreur est survenue lors de la tentative de passer votre commande.",
            color=discord.Color.red()
        )
        embed.add_field(name="Détails", value=result.get('error', 'Erreur inconnue'), inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def bal(ctx):
    api_url = "https://smmfollows.com/api/v2"
    payload = {
        'key': SMMFOLLOWS_API_KEY,
        'action': 'balance'
    }

    response = requests.post(api_url, data=payload)

    try:
        result = response.json()
    except ValueError:
        await ctx.send("Erreur : Réponse invalide de l'API SMMFollows.")
        return

    if 'balance' in result:
        balance_usd = float(result['balance'])
        currency = result.get('currency', 'USD')

        if currency == 'USD':
            balance_eur = balance_usd * USD_TO_EUR_CONVERSION_RATE
            embed = discord.Embed(
                title="Balance actuelle",
                description=(
                    f"Votre balance actuelle est de **{balance_usd:.2f} USD** "
                    f"({balance_eur:.2f} EUR après conversion)."
                ),
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="Balance actuelle",
                description=f"Votre balance actuelle est de **{balance_usd:.2f} {currency}**.",
                color=discord.Color.green()
            )

        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Erreur lors de la récupération de la balance",
            description="Une erreur est survenue lors de la tentative de récupérer la balance.",
            color=discord.Color.red()
        )
        embed.add_field(name="Détails", value=result.get('error', 'Erreur inconnue'), inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def pay(ctx):
    message = (
        "__**Veuillez utiliser les informations ci-dessous pour effectuer votre paiement.**__\n\n"
        "**Litecoin : **\n"
        "`ton adresse litecoin`\n\n"
        "**PayPal :**\n"
        "`ton mail paypal`\n\n"
        "**Pour les paiements par PayPal, veuillez envoyer par amis et proches et ne surtout pas mettre de notes. "
        "Si vous ne respectez pas ceci, nous nous réservons le droit de ne pas vous rembourser.**\n\n"
        "**Si vous changez de nom d'utilisateur pendant votre envoi, nous ne sommes pas responsables de la perte de vos followers.**\n\n"
        "__**Veille également à mettre ton compte en public ! (tu pourras le remettre en privé après la réception)**__"
    )
    await ctx.send(message)


async def load_cogs():
    await bot.load_extension('commands.ticket')
    await bot.load_extension('commands.explication')

@bot.event
async def on_ready():
    await load_cogs()
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.channel.id in CHANNEL_IDS_TO_REACT and not message.author.bot:
        emoji = discord.utils.get(bot.emojis, id=CUSTOM_EMOJI_ID)
        if emoji:
            await message.add_reaction(emoji)
    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def rename(ctx, *, new_name: str):
    await ctx.channel.edit(name=new_name)
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def reward(ctx, amount: int, target: str):
    await ctx.message.delete()
    global client_number
    client_number += 1 
    username = extract_tiktok_username(target)
    link = f"https://www.tiktok.com/@{username}"

    api_url = "https://smmfollows.com/api/v2"
    payload = {
        'key': SMMFOLLOWS_API_KEY,
        'action': 'add',
        'service': 13825,  
        'link': link,
        'quantity': amount
    }

    response = requests.post(api_url, data=payload)

    try:
        result = response.json()
    except ValueError:
        await ctx.send("Erreur : Réponse invalide de l'API SMMFollows.")
        return

    if 'order' in result:
        order_id = result['order']
        embed = discord.Embed(
            title="Commande de followers TikTok passée avec succès",
            description=f"Votre commande de {amount} followers pour [{username}]({link}) a été passée.",
            color=discord.Color.from_rgb(255, 255, 255)
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="Quantité", value=amount, inline=True)
        embed.add_field(name="Cible", value=f"[{username}]({link})", inline=True)
        embed.add_field(name="Temps estimé", value="Varie en fonction de la charge du serveur", inline=True)

        await ctx.send(embed=embed)

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await channel.send(
                f"Client numéro {client_number}\n"
                f"[Lien TikTok]({link})\n"
                f"Quantité envoyée : {amount}\n"
                f"Date : {date_str}"
            )

        bot.loop.create_task(check_order_status(order_id, CHANNEL_ID, link, amount))
    else:
        embed = discord.Embed(
            title="Erreur lors de la commande",
            description="Une erreur est survenue lors de la tentative de passer votre commande.",
            color=discord.Color.red()
        )
        embed.add_field(name="Détails", value=result.get('error', 'Erreur inconnue'), inline=False)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def gw(ctx, amount: int, target: str):
    await ctx.message.delete()
    global client_number
    client_number += 1 
    username = extract_tiktok_username(target)
    link = f"https://www.tiktok.com/@{username}"

    api_url = "https://smmfollows.com/api/v2"
    payload = {
        'key': SMMFOLLOWS_API_KEY,
        'action': 'add',
        'service': 13826,  
        'link': link,
        'quantity': amount
    }

    response = requests.post(api_url, data=payload)

    try:
        result = response.json()
    except ValueError:
        await ctx.send("Erreur : Réponse invalide de l'API SMMFollows.")
        return

    if 'order' in result:
        order_id = result['order']
        embed = discord.Embed(
            title="Commande de followers TikTok passée avec succès",
            description=f"Votre commande de {amount} followers pour [{username}]({link}) a été passée.",
            color=discord.Color.from_rgb(255, 255, 255)
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="Quantité", value=amount, inline=True)
        embed.add_field(name="Cible", value=f"[{username}]({link})", inline=True)
        embed.add_field(name="Temps estimé", value="Varie en fonction de la charge du serveur", inline=True)

        await ctx.send(embed=embed)

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await channel.send(
                f"Client numéro {client_number}\n"
                f"[Lien TikTok]({link})\n"
                f"Quantité envoyée : {amount}\n"
                f"Date : {date_str}"
            )
        
        bot.loop.create_task(check_order_status(order_id, CHANNEL_ID, link, amount))
    else:
        embed = discord.Embed(
            title="Erreur lors de la commande",
            description="Une erreur est survenue lors de la tentative de passer votre commande.",
            color=discord.Color.red()
        )
        embed.add_field(name="Détails", value=result.get('error', 'Erreur inconnue'), inline=False)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def like(ctx, amount: int, link: str): 
    await ctx.message.delete()
    global client_number
    client_number += 1 

    api_url = "https://smmfollows.com/api/v2"
    payload = {
        'key': SMMFOLLOWS_API_KEY,
        'action': 'add',
        'service': 250,  
        'link': link,
        'quantity': amount
    }

    response = requests.post(api_url, data=payload)

    try:
        result = response.json()
    except ValueError:
        await ctx.send("Erreur : Réponse invalide de l'API SMMFollows.")
        return

    if 'order' in result:
        order_id = result['order']
        embed = discord.Embed(
            title="Commande de likes TikTok passée avec succès",
            description=f"Votre commande de {amount} likes pour la vidéo [{link}]({link}) a été passée.",
            color=discord.Color.from_rgb(255, 255, 255)
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="Quantité", value=amount, inline=True)
        embed.add_field(name="Cible", value=f"[Lien vidéo]({link})", inline=True)
        embed.add_field(name="Temps estimé", value="Varie en fonction de la charge du serveur", inline=True)

        await ctx.send(embed=embed)

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await channel.send(
                f"Client numéro {client_number}\n"
                f"[Lien vidéo TikTok]({link})\n"
                f"Quantité envoyée : {amount}\n"
                f"Date : {date_str}"
            )
        
        bot.loop.create_task(check_order_status(order_id, CHANNEL_ID, link, amount))
    else:
        embed = discord.Embed(
            title="Erreur lors de la commande",
            description="Une erreur est survenue lors de la tentative de passer votre commande.",
            color=discord.Color.red()
        )
        embed.add_field(name="Détails", value=result.get('error', 'Erreur inconnue'), inline=False)
        await ctx.send(embed=embed)
        
    
bot.run(DISCORD_TOKEN)
