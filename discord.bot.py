import discord
from discord.ext import commands
from datetime import datetime, timedelta

# Variables
idepoklucz = False
status_biura = False
scanned_results = "scanner_results.txt"
bot_token = 'token'
last_key_fetch_time = None  # Time when /idepoklucz was used

async def read_last_line(filename):
    with open(filename, "rb") as file:
        file.seek(-2, 2)  # move coursor to last-1 row
        while file.read(1) != b"\n": 
            file.seek(-2, 1)
        return file.readline().decode().strip()  # read last line and decode


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
    global status_biura
    last_key_fetch_time = datetime.now()  # Save the time when /idepoklucz was used
    if status_biura == False:
        await ctx.send('Super! Jeśli ktos wpiszę te komendę zostanie powiadomiony o twoim dzielnym dokonaniu :)')
        idepoklucz = True
    else:
        await ctx.send('Biuro już jest otwarte :)')


@bot.command()
async def biuro(ctx):
    global idepoklucz, last_key_fetch_time, status_biura
    last_line = await read_last_line(scanned_results)
    
    # split date and status
    date_str, status = last_line.split(";")
    
    # check if 10 minut was left
    if last_key_fetch_time and datetime.now() - last_key_fetch_time < timedelta(minutes=10):
        if idepoklucz == True and status == "false":
            await ctx.send('Ktoś już poszedł po klucz! Poczekaj na swego wybawcę pod biurem')
        return  # Prevent checking the status from the file while within the 10-minute window
    
    # After 10 minutes or no recent use of /idepoklucz, proceed with normal status check
    if status == "true":
        await ctx.send(f"Biuro jest **otwarte**")
        idepoklucz = False
        status_biura = True
    elif status == "false":
        await ctx.send(f"Biuro jest **zamknięte**")
        status_biura = False
    else:
        await ctx.send("Błąd: Nieprawidłowy status w pliku.")
# Start the bot
bot.run(bot_token)
