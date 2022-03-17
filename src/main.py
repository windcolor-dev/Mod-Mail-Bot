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

# Init
client = discord.Client()

# Console logs
@client.event
async def on_ready():
    print('The mod-mail bot has logged in as {0.user}'.format(client)) 
    await set_status()
  
# Set bot status
async def set_status():
  time.sleep(2)
  if status_enabled == True:
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=bot_status))

# Listen to msgs
@client.event
async def on_message(message):
    if message.author == client.user:
      return

    # Close mod mail channels
    if message.content.startswith('!close'):
        if message.channel.name.endswith('-mod-mail'):
            
            # Delete values from our hash tables (channel is linked to user, user is linked to channel)
            hash_tables.delete_val(hash_tables.get_val(message.channel).name)
            hash_tables.delete_val(message.channel)

            # Logs
            print('[LOGS] A mod mail channel was deleted')
            channelGet = client.get_channel(info_channel_id)
            await channelGet.send('[LOGS] A mod mail channel was deleted')
            
            # Remove channel
            await message.channel.delete()

    # Update member using mod mail
    if hash_tables.get_val(message.channel) != 'No record found':
        # Create embeds of msgs to send to user
        userEmbed=discord.Embed(title='Message from ' + message.author.name, description=message.content, color=color)
        member = hash_tables.get_val(message.channel)
        userEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
        
        # Staff msg embed
        staffEmbed=discord.Embed(title='Message sent by ' + message.author.name, description=message.content, color=color)
        staffEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
        
        # Send embed to user
        await member.send(embed=userEmbed)
        
        # Replace msg with embed
        await message.delete()
        
        # Send embed to staff and replace msg
        await message.channel.send(embed=staffEmbed)

    # Initialize mod mail channel
    if str(message.channel.type) == 'private':
      # Send msg to channel if user is already using mod mail
      if hash_tables.get_val(message.author.name) != 'No record found':
            
        # Logs channel
        channelGet = client.get_channel(info_channel_id)
        
        # Mod mail channel
        staffChannel = hash_tables.get_val(message.author.name)
        
        # Create embeds from msg
        embed=discord.Embed(title='Message from ' + message.author.name + ':', description=message.content, color=color)
        embed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)    
        
        DMChannel = message.channel
        
        userEmbed=discord.Embed(title='Your Message:', description=message.content, color=color)
        userEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)
        
        # Send embeds
        await staffChannel.send(embed=embed)
        await DMChannel.send(embed=userEmbed)
        
        # Log
        await channelGet.send('[LOGS] A new message was received from ' + message.author.name + '.')
        if ping_here == True:
            await channelGet.send('@here')
            
        return
      
      # Logs channel
      channelGet = client.get_channel(info_channel_id)
      # Mod mail channel creation
      modMailChannel = await channelGet.guild.create_text_channel(name=message.author.name +'-mod-mail', category=channelGet.category)

      # Log new msg
      await channelGet.send('[LOGS] A new message was received from ' + message.author.name + '.')
      if ping_here == True:
          await channelGet.send('@here')

      # Use hash tables to store channels and users and link them together
      hash_tables.set_val(message.author.name, modMailChannel)
      hash_tables.set_val(modMailChannel, message.author)
      
      # Mod mail channel to send msgs in
      channel = hash_tables.get_val(message.author.name)
      
      # Create embeds
      staffEmbed=discord.Embed(title='Message from ' + message.author.name + ':', description=message.content, color=color)
      staffEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)    
      
      userEmbed=discord.Embed(title='Your Message:', description=message.content, color=color)
      userEmbed.set_footer(text=message.author.name, icon_url=message.author.avatar_url)

      # Send embeds
      await channel.send(embed=staffEmbed)
      
      await message.channel.send('**Your message has been sent to mod-mail!**')

      await message.author.send(embed=userEmbed)

    
# Start bot
client.run(token)

