import discord
import asyncio
import time
import os
import urllib.request
import random
import cleverbot
from bs4 import BeautifulSoup
from datetime import datetime
import odds


editor = 'Flexo'

client = discord.Client()

# List for random game status generation
list1 = ["Elite: Dangerous", "Learning to Skynet", "Real Life: The Game"]

# List for help commands
help_list = ["@Humberto - Chat with Humberto", "!tick - Display time until Server Tick",
             "!youtube subject - Pull a random youtube video of subject", "!servertime - Display current server time",
             "!roll - Roll a random number between 1 - 100"]

# defining directory for images to be pulled from
image_dir = "C:/Users/Crunchy/PyCharmProjects/untitled1/"

# Lists for INC function.
i_inc = ["Intergalactic", "Interplanetary", "Interstellar", "Industrial", "Integrated", "Independent", "Incompetent",
         "Incomplete", "Irradiated"]
n_inc = ["Network", "Neutral", "National", "Negotiating", "Necromancer", "Nuclear", "Nebulous", "Normal", "Natural",
         "Nascent"]
c_inc = ["Council", "Consortium", "Club", "Country", "Cartel", "Cabinet", "Clique", "Channel"]




@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------------')
    # Wake up message
    await client.send_message(
        client.get_channel('193969061808308224'),
        editor + '\'s script is active'
    )


# Function to search for a youtube video and return a link.
@client.event
async def youtube_search(message):
    link_list = []
    text_to_search = message.content.replace('!youtube', '')
    print('Searching YouTube for:' + text_to_search)
    query = urllib.request.quote(text_to_search)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        link_list.append('https://www.youtube.com' + vid['href'])
    random_num = random.randint(0, len(link_list) - 1)
    await client.send_message(message.channel, "" + link_list[random_num])


# Test for a string within message
@client.event
async def find_in_message(msg, find):
    msg_text = msg.content
    for x in range(0, len(msg_text) - (len(find) - 1)):
        index = msg_text[x:len(find) + x]
        if index.lower() == find:
            return True


# Ask clever bot a question.
@client.event
async def ask_clever_bot(message):
    question = message.content.replace('<@193445599872286720>', '')
    cb1 = cleverbot.Cleverbot()
    answer = cb1.ask(question)
    await client.send_message(message.channel, answer)


# Rolling the odds for a user.
@client.event
async def roll_odds(user, message):
    rand_roll = random.randint(0, 100)
    await client.send_message(message.channel, '%s your roll is %s' % (user, rand_roll))


# Respond to Trigger fuction
@client.event
async def respond_to_trigger(message, trig, resp):
    msg = message.content
    for x in range(0, len(msg) - (len(trig) - 1)):
        index = msg[x:len(trig) + x]
        if index.lower() == trig:
            await client.send_message(message.channel, resp)


# Calculate server tick time
@client.event
async def tick_time():
    now_hour = datetime.utcnow().strftime('%H')
    now_hour = int(now_hour)
    now_min = datetime.utcnow().strftime('%M')
    now_min = int(now_min)
    now_sec = datetime.utcnow().strftime('%S')
    now_sec = int(now_sec)

    server_time = datetime(2005, 10, 1, 17, 0, 0)
    server_time_hour = server_time.strftime('%H')
    server_time_hour = int(server_time_hour)
    server_time_min = server_time.strftime('%M')
    server_time_min = int(server_time_min)
    server_time_sec = server_time.strftime('%S')
    server_time_sec = int(server_time_sec)

    delta_hour = server_time_hour - now_hour
    delta_min = server_time_min - now_min
    delta_sec = server_time_sec - now_sec

    if (delta_hour < 0):
        hour = 23 + delta_hour
    else:
        hour = delta_hour

    if (delta_min < 0):
        min = 59 + delta_min
    else:
        min = delta_min

    if (delta_sec < 0):
        sec = 59 + delta_sec
    else:
        sec = delta_sec

    msg = 'Approximate Server Tick in %d hours %d minutes and %d seconds' % (hour, min, sec)
    print(msg)
    return msg


# Define "INC" function
@client.event
async def inc_define(message):
    rand_i = random.randint(0, 8)
    rand_n = random.randint(0, 9)
    rand_c = random.randint(0, 7)
    await client.send_message(message.channel,
                              'INC stands for %s %s %s' % (i_inc[rand_i], n_inc[rand_n], c_inc[rand_c]))


@client.event
async def on_message(message):
    # Shortcuts
    channel = message.channel
    user = message.author
    msg = message.content
    # Channel IDs
    bots = '193969061808308224'

    # This prints conversations to the Python Console
    print("[%s] %s: %s" % (channel, user, msg))

    if msg.startswith('!editor') and channel.id == bots:
        await client.send_message(client.get_channel(bots), 'Current editor: ' + editor)

    # Force OS process termination
    if msg.startswith('!stop' + editor) and channel.id == bots:
        await client.send_message(client.get_channel(bots), editor + '\'s script was stopped')
        os._exit(0)

    # gets channel ID
    if msg.startswith('!channel'):
        await client.send_message(client.get_channel(bots), 'Channel ID is: ' + (channel.id))

    # gets user ID
    if msg.startswith('!user'):
        await client.send_message(message.channel, 'Your user ID is: ' + (user.id))

    # Server Tick Time
    if msg.startswith('!tick'):
        await client.send_message(message.channel, await tick_time())

    # copies the message after deleting
    if msg.startswith('!copy'):
        rpl = msg.replace('!copy', '')
        await client.delete_message(message)
        await client.send_message(message.channel, rpl)

    # help command
    if msg.startswith('!help'):
        await client.send_message(message.channel, "\n".join(help_list))

    # youtube
    if msg.startswith('!youtube'):
        await youtube_search(message)

    # cleverbot
    if msg.find('<@193445599872286720>') != -1:
        await ask_clever_bot(message)

    # roll
    if msg.startswith('!roll'):
        number = odds.roll_odds()
        await client.send_message(message.channel, 'Your random number is ' + number)

    # Scott Sterling
    if msg.startswith('Scott Sterling'):
        tmp = await client.send_message(message.channel, 'The Man!')
        await asyncio.sleep(1)
        await client.send_message(message.channel, 'The Myth!')
        await asyncio.sleep(1)
        await client.send_message(message.channel, 'The Legend!')

    # fetch scott sterling video
    if msg.find('show me Scott Sterling') != -1:
        await client.send_message(message.channel, 'https://youtu.be/8F9jXYOH2c0')

    # Bot Game status
    if msg.startswith('!gameon'):
        rand_roll = random.randint(0, 2)
        game_status = discord.Game(name=list1[rand_roll], url='put url here', type=0)
        await client.change_status(game=game_status)

    if msg.startswith('!gameelite'):
        game_status_temp = discord.Game(name="Elite: Dangerous", url='none', type=0)
        await client.change_status(game=game_status_temp)

    if msg.startswith('!gamespace'):
        game_status_sky = discord.Game(name="Space Engineers", url='none', type=0)
        await client.change_status(game=game_status_sky)

    if msg.startswith('!gameoff'):
        await client.change_status(game=None)

    # image posting code
    if msg.startswith('!pic'):
        await client.send_file(message.channel, image_dir + "janitor.jpg")

    # Server Time
    if msg.startswith('!servertime'):
        server_time = time.asctime(time.gmtime(time.time()))
        await client.send_message(message.channel, 'Current server time: ' + server_time)

    # Call What is INC function
    if msg.startswith('!define inc') or msg.startswith('!define INC'):
        await inc_define(message)


# Login and join chat
# NOT A PART OF on_message()
client.accept_invite('https://discord.gg/0zv7gFjB5rch8L2I')
client.run('MTkzNDQ1NTk5ODcyMjg2NzIw.CkXfwQ.610VHj2W49WR9IUzAWWcBL1APrg')
