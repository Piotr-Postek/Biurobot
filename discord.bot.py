import discord
from discord.ext import commands

# Variables
idepoklucz = False
scanned_results = "scanned_results.txt"
bot_token = 'token'

async def read_last_line(filename):
    with open(filename, "rb") as file:
        file.seek(-2, 2)  # Przesunięcie kursora na przedostatni bajt pliku
        while file.read(1) != b"\n":  # Cofamy się do najbliższego znaku nowej linii
            file.seek(-2, 1)
        return file.readline().decode().strip()  # Odczytanie ostatniej linii i dekodowanie


# Set up intents
intents = discord.Intents.default()  # Default intents, but you can enable more as needed
intents.message_content = True  # Allow the bot to read message content

# Create bot instance with intents
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send('Siemanko!!! Z tej strony bot Roman. Wpisz polecenie /helpme aby dowiedzieć się co możesz zrobić')


@bot.command()
async def helpme(ctx):
    await ctx.send('Ota lista dostepnych komend:\n /biuro - sprawdza status biura\n /hello - przywitanie\n /helpme - lista dostepnych komend\n /idepoklucz - daj znać innym, że poszedłeś już po klucz\n')

@bot.command()
async def idepoklucz(ctx):
    global idepoklucz
    await ctx.send('Super! Jeśli ktos wpiszę te komendę zostanie powiadomiony o twoim dzielnym dokonaniu :)')
    idepoklucz = True

# Funkcja `biuro`, która odczytuje ostatnią linię i odpowiada na podstawie statusu
@bot.command()
async def biuro(ctx):
    global idepoklucz
    last_line = await read_last_line(scanned_results)
    
    # Rozdzielenie daty i statusu na podstawie średnika
    date_str, status = last_line.split(";")
    
    # Sprawdzenie statusu i wysłanie odpowiedniej wiadomości
    if idepoklucz == True and status=="false":
        await ctx.send('Ktoś już poszedł po klucz! Poczekaj na swego wybawcę pod biurem')
    elif status == "true":
        await ctx.send(f"Biuro jest **otwarte**")
        idepoklucz = False
    elif status == "false":
        await ctx.send(f"Biuro jest **zamknięte**")
    else:
        await ctx.send("Błąd: Nieprawidłowy status w pliku.")

# Start the bot
bot.run(bot_token)
