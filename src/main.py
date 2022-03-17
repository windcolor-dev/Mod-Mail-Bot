import discord
from hash_maps import *
import time

hash_tables = hash_map(100)

# Replace this with your bot's token
token = 'YourTokenHere'

# Please see color-info.txt for information on colors.
color = 0x3498db

# Replace this with a channel that displays when a new message is received.
# Put this in the category that you want your mod-mail channels to appear in.
info_channel_id = 'ChannelIdNumber'

# If the bot's status should be set (configure below)
status_enabled = True

# Replace this with what you want your bot's status to be shown as
# This would set the bot's status to "Listening to your DMs"
bot_status = 'your DMs'

# If the bot should ping @here in the logs channel when a new message is 
# received.
ping_here = True

client = discord.Client()

@client.event
async def on_ready():
    print('The mod-mail bot has logged in as {0.user}'.format(client)) 
    await set_status()
  
async def set_status():
  time.sleep(2)
  if status_enabled == True:
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=bot_status))

@client.event
async def on_message(message):
    if message.author == client.user:
      return

    if message.content.startswith('!close'):
        if message.channel.name.endswith('-mod-mail'):
            if message.channel == hash_tables.get_val(message.author.name):
                hash_tables.delete_val(message.author.name)
                hash_tables.delete_val(message.channel)

        print('[LOGS] A mod mail channel was deleted')
        channelGet = client.get_channel(info_channel_id)
        await channelGet.send('[LOGS] A mod mail channel was deleted')
        await message.channel.delete()

    if hash_tables.get_val(message.channel) != 'No record found':
        userEmbed=discord.Embed(title='Message from ' + message.author.name, description=message.content, color=color)
        member = hash_tables.get_val(message.channel)
        userEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
        
        staffEmbed=discord.Embed(title='Message sent by ' + message.author.name, description=message.content, color=color)
        staffEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
        await member.send(embed=userEmbed)
        await message.delete()
        await message.channel.send(embed=staffEmbed)

    if str(message.channel.type) == 'private':
      if hash_tables.get_val(message.author.name) != 'No record found':
        channelGet = client.get_channel(info_channel_id)
        staffChannel = hash_tables.get_val(message.author.name)
        embed=discord.Embed(title='Message from ' + message.author.name + ':', description=message.content, color=color)
        embed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)    
        DMChannel = message.channel
        userEmbed=discord.Embed(title='Your Message:', description=message.content, color=color)
        userEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
        await staffChannel.send(embed=embed)
        await DMChannel.send(embed=userEmbed)
        
        await channelGet.send('[LOGS] A new message was received from ' + message.author.name + '.')
        if ping_here == True:
            await channelGet.send('@here')
            
        return

      channelGet = client.get_channel(info_channel_id)
      modMailChannel = await channelGet.guild.create_text_channel(name=message.author.name +'-mod-mail', category=channelGet.category)

      await channelGet.send('[LOGS] A new message was received from ' + message.author.name + '.')
      if ping_here == True:
          await channelGet.send('@here')

      hash_tables.set_val(message.author.name, modMailChannel)
      hash_tables.set_val(modMailChannel, message.author)
      
      channel = hash_tables.get_val(message.author.name)
      
      staffEmbed=discord.Embed(title='Message from ' + message.author.name + ':', description=message.content, color=color)
      staffEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)    
      
      userEmbed=discord.Embed(title='Your Message:', description=message.content, color=color)
      userEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)

      await channel.send(embed=staffEmbed)
      
      await message.channel.send('**Your message has been sent to mod-mail!**')

      await message.author.send(embed=userEmbed)

    
client.run(token)

