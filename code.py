import pymongo
from pymongo import MongoClient
import asyncio
import random
import datetime
import re
import json
import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = commands.when_mentioned_or('cy|'), intents = discord.Intents.all(), owner_id = 338714886001524737)
client.remove_command('help')

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        time = 0
        matches = re.findall(time_regex, args)
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                await ctx.send(f'{value} не является правильным аргументом! Правильные: h|m|s|d')
            except ValueError:
                await ctx.send(f'{key} не число!')
        return time
#test space
@client.command()
async def niggers(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = '[осуждающее видео](https://vk.com/video-184856829_456240358)')
    await ctx.send(embed = emb)
#test space

#Mod
@client.command()
@commands.has_permissions(view_audit_log = True)
@commands.cooldown(1, 5, commands.BucketType.default)
async def dm(ctx, member: discord.User, *, text):
    await ctx.message.delete()
    emb = discord.Embed(description = f'{text}', colour = ctx.author.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
    await member.send(embed = emb)

@client.command(aliases = ['Kick', 'KICK'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason: str = None):
    await ctx.message.delete()
    if member.id != 338714886001524737:
            if reason == None:
                reason = 'Не указана.'
            if ctx.author.top_role == member.top_role:
                emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Кик отклонён.', colour = discord.Color.green())
                await ctx.send(embed = emb)
            elif member.top_role > ctx.author.top_role:
                emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Кик отклонён.', colour = discord.Color.green())
                await ctx.send(embed = emb)
            else:
                emb = discord.Embed(colour = member.color)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'Был кикнут', value = member.mention)
                emb.add_field(name = 'По причине', value = reason)
                emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
                await ctx.send(embed = emb)
                await member.kick(reason = reason)
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете кикнуть моего создателя!', colour = discord.Color.green())
        await ctx.send(embed = emb)

@client.command(aliases = ['Ban', 'BAN'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = None):
    await ctx.message.delete()
    if member.id != 338714886001524737:
        if reason == None:
            reason = 'Не указана.'
        if ctx.author.top_role == member.top_role:
            emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Бан отклонён.', colour = discord.Color.green())
            await ctx.send(embed = emb)
        elif member.top_role > ctx.author.top_role:
            emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Бан отклонён.', colour = discord.Color.green())
            await ctx.send(embed = emb)
        else:
            emb = discord.Embed(colour = member.color)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            emb.add_field(name = 'Был забанен', value = member.mention)
            emb.add_field(name = 'По причине', value = reason)
            emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
            await ctx.send(embed = emb)
            await member.ban(reason = reason)
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете забанить моего создателя!', colour = discord.Color.green())
        await ctx.send(embed = emb)

@client.command(aliases = ['Give', 'GIVE'])
@commands.has_permissions(manage_channels = True)
async def give(ctx, member: discord.Member, *, role: discord.Role):
    await ctx.message.delete()
    if role != None:
        if role > member.top_role and ctx.message.author.id != 338714886001524737:
            await ctx.send('Вы не можете выдать эту роль, так как она имеет более высокий ранг, чем ваша высшая роль.')
        elif role == ctx.author.top_role and ctx.message.author.id != 338714886001524737:
            await ctx.send('Вы не можете выдать эту роль кому-либо, так как она равна вашей высшей роли.')
        elif role.is_default():
            await ctx.send('Выдавать everyone? Всё с башкой хорошо?')
        else:
            await member.add_roles(role)
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
            emb.add_field(name = 'Была выдана роль', value = f'{role.mention} | {role.name} | ID {role.id}')
            emb.add_field(name = 'Выдана:', value = member.mention)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
            await channel.send(embed = emb)
    else:
        emb = discord.Embed(description = f'{ctx.author.mention}, я не могу найти {role.mention} в списке ролей.', colour = member.color, timestamp = ctx.message.created_at)
        await ctx.send(embed = emb)
            
@client.command(aliases = ['Take', 'TAKE'])
@commands.has_permissions(manage_channels = True)
async def take(ctx, member: discord.Member, *, role: discord.Role):
    await ctx.message.delete()
    if role != None:
        if role > ctx.author.top_role and ctx.message.author.id != 338714886001524737:
            await ctx.send('Вы не можете забрать эту роль, так как она имеет более высокий ранг, чем ваша высшая роль.')
        elif role == ctx.author.top_role and ctx.message.author.id != 338714886001524737:
            await ctx.send('Вы не можете забрать эту роль у кого-либо, так как она равна вашей высшей роли.')
        elif role.is_default():
            await ctx.send('Забирать everyone? Всё с башкой хорошо?')
        else:
            await member.remove_roles(role)
            channel = client.get_channel(714175791033876490)
            emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
            emb.add_field(name = 'Была забрана роль', value = f'{role.mention} | {role.name} | ID {role.id}')
            emb.add_field(name = 'Забрана:', value = member.mention)
            emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
            await channel.send(embed = emb)
    else:
        emb = discord.Embed(description = f'{ctx.author.mention}, я не могу найти {role.mention} в списке ролей.', colour = member.color, timestamp = ctx.message.created_at)
        await ctx.send(embed = emb)
            
@client.command(aliases = ['Mute', 'MUTE'])
@commands.has_permissions(manage_channels = True)
async def mute(ctx, member: discord.Member, time: TimeConverter, *, reason: str = None):
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, name = 'Muted')
    if member.id != 338714886001524737:
        if ctx.author.top_role == member.top_role and ctx.message.author.id != 338714886001524737:
            emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Мут отклонён.', colour = discord.Color.green())
            await ctx.send(embed = emb)
        elif ctx.author.top_role < member.top_role and ctx.message.author.id != 338714886001524737:
            emb = discord.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Мут отклонён.', colour = discord.Color.green())
            await ctx.send(embed = emb)
        else:
            if role != None:
                await member.add_roles(role)
                if reason == None:
                    reason = 'Не указана.'
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'В муте', value = f'{member.mention}')
                emb.add_field(name = 'По причине', value = reason)
                emb.add_field(name = 'Время мута', value = f'{time}s')
                emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
                await ctx.send(embed = emb, delete_after = time)
                await asyncio.sleep(time)
                if role != None:
                    if role in member.roles:
                        emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                        emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                        emb.add_field(name = 'Был в муте по причине', value = reason)
                        emb.add_field(name = 'Время мута составляло', value = f'{time}s')
                        emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
                        await member.remove_roles(role)
                        await ctx.send(f'{member.mention}', embed = emb)
                    else:
                        emb = discord.Embed(description = f'Снятие мута для {member.mention} не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = discord.Color.green())
                        await ctx.send(embed = emb)
                else:
                    emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять мут у {member.mention} из-за того, что роль Muted была удалена/отредактирована!', colour = discord.Color.green(), timestamp = ctx.message.created_at)
                    await ctx.send(embed = emb)
            else:
                await ctx.guild.create_role(name = 'Muted', colour = discord.Colour(0x000001))
                emb1 = discord.Embed(description = f'{ctx.author.mention}, По причине того, что я не нашёл нужную роль, была создана роль {role.name} с цветом {role.colour}.', colour = discord.Color.green(), timestamp = ctx.message.created_at)
                emb1.set_footer(text = 'Это сообщение должно показываться только 1 раз. Иначе, роль была удалена/отредактирована')
                await ctx.send(embed = emb1, delete_after = 3)
                await asyncio.sleep(3)
                await member.add_roles(role)
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
                emb.add_field(name = 'В муте', value = f'{member.mention}')
                emb.add_field(name = 'По причине', value = reason)
                emb.add_field(name = 'Время мута', value = f'{time}s')
                emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
                await ctx.send(embed = emb, delete_after = time)
                await asyncio.sleep(time)
                if role != None:
                    if role in member.roles:
                        emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                        emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                        emb.add_field(name = 'По причине', value = reason)
                        emb.add_field(name = 'Время мута составляло', value = f'{time}s')
                        emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
                        await ctx.send(f'{member.mention}', embed = emb)
                        await member.remove_roles(role)
                    else:
                        emb = discord.Embed(description = f'Снятие мута для {member.mention} не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = discord.Color.green())
                        emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
                        await ctx.send(embed = emb)    
    else:
        emb = discord.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете замутить моего создателя!', colour = discord.Color.green())
        emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
        await ctx.send(embed = emb)
        
@client.command(aliases = ['Unmute', 'UNMUTE'])
@commands.has_permissions(manage_channels = True)
async def unmute(ctx, member: discord.Member, *, reason = None):
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, name = 'Muted')
    if role != None:
        if role in member.roles:
            await member.remove_roles(role)
            if reason == None:
                reason = 'Не указана.'
            emb = discord.Embed(title = f'Принудительное снятие мута у {member}', colour = member.color, timestamp = ctx.message.created_at)
            emb.add_field(name = 'Снял мут', value = ctx.author.mention)
            emb.add_field(name = 'По причине', value = reason)
            emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
            await ctx.send(embed = emb)
        else:
            emb = discord.Embed(description = 'Снятие мута не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = discord.Color.green())
            emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
            await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'{ctx.author.mention}, Я не могу снять мут у {member.mention} из-за того, что роль Muted была удалена/отредактирована!', colour = discord.Color.green(), timestamp = ctx.message.created_at)
        emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
        await ctx.send(embed = emb)

@client.command(aliases = ['Clear', 'CLEAR'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount: int, confirm: str = None):
    await ctx.message.delete()
    if amount == 0:
        emb = discord.Embed(description = 'Удалять 0 сообщений?', colour = discord.Color.green())
        await ctx.send(embed = emb, delete_after = 3)
    elif amount == 1:
        emb = discord.Embed(description = f'удалено {amount} сообщение', colour = discord.Color.green())
        emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
        await ctx.channel.purge(limit = amount)
        await ctx.send(embed = emb, delete_after = 1)
    elif amount == 2:
        emb = discord.Embed(description = f'удалено {amount} сообщения', colour = discord.Color.green())
        emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
        await ctx.channel.purge(limit = amount)
        await ctx.send(embed = emb, delete_after = 1)
    elif amount == 3:
        emb = discord.Embed(description = f'удалено {amount} сообщения', colour = discord.Color.green())
        emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
        await ctx.channel.purge(limit = amount)
        await ctx.send(embed = emb, delete_after = 1)
    elif amount == 4:
        emb = discord.Embed(description = f'удалено {amount} сообщения', colour = discord.Color.green())
        emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
        await ctx.channel.purge(limit = amount)
        await ctx.send(embed = emb, delete_after = 1)
    elif amount >= 10:
        if confirm == 'confirm':
            await ctx.send(f'Через 3 секунды будет удалено {amount} сообщений')
            await asyncio.sleep(3)
            await ctx.channel.purge(limit = amount + 1)
            await ctx.send(f'удалено {amount} сообщений', delete_after = 2)
        if confirm == None:
            emb = discord.Embed(description = f'{ctx.author.mention}, для выполнения этой команды мне нужно ваше подтвеждение! (чувствительно к регистру)', colour = discord.Color.green())
            emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
            await ctx.send(embed = emb)
    else:
        emb = discord.Embed(description = f'удалено {amount} сообщений', colour = discord.Color.green())
        emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
        await ctx.channel.purge(limit = amount)
        await ctx.send(embed = emb, delete_after = 1)
#Mod

#Misc
@client.command(aliases = ['Guild', 'GUILD'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def guild(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    emb = discord.Embed(colour = discord.Color.green(), timestamp = ctx.message.created_at)
    emb.set_author(name = guild, icon_url = guild.icon_url)
    emb.add_field(name = 'ID сервера', value = guild.id)
    emb.add_field(name = 'Голосовой регион', value = guild.region)
    emb.add_field(name = 'Участников', value = guild.member_count)
    emb.add_field(name = 'Каналов', value = f'Текстовых {len(guild.text_channels)} | Голосовых {len(guild.voice_channels)}')
    limit = len(guild.roles)
    if limit > 21:
        emb.add_field(name = 'Роли', value = f'Слишком много для отрисовки ({len(guild.roles)-1}) [лимит 20]', inline = False)
    elif limit == 21:
        emb.add_field(name = f'Роли ({len(guild.roles)-1}) [лимит достигнут]', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
    elif limit == 20:
        emb.add_field(name = f'Роли ({len(guild.roles)-1}) [1 до лимита]', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
    elif limit == 19:
        emb.add_field(name = f'Роли ({len(guild.roles)-1}) [2 до лимита]', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
    elif limit == 18:
        emb.add_field(name = f'Роли ({len(guild.roles)-1}) [3 до лимита]', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
    else:
        emb.add_field(name = f'Роли ({len(guild.roles)-1})', value = ', '.join([role.mention for role in guild.roles[1:]]), inline = False)
    now = datetime.datetime.today()
    then = guild.created_at
    delta = now - then
    d = guild.created_at.strftime('%d/%m/%Y %H:%M:%S UTC')
    emb.add_field(name = 'Дата создания сервера', value = f'{delta.days} дней назад. ({d})', inline = False)
    emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
    emb.set_thumbnail(url = guild.icon_url)
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.default)
async def role(ctx, *, role: discord.Role):
    await ctx.message.delete()
    if role.mentionable == False:
        role.mentionable = 'Нет'
    elif role.mentionable == True:
        role.mentionable = 'Да'
    if role.managed == False:
        role.managed = 'Нет'
    elif role.managed == True:
        role.managed = 'Да'
    if role.hoist == False:
        role.hoist = 'Нет'
    elif role.hoist == True:
        role.hoist = 'Да'
    emb = discord.Embed(title = role.name, colour = role.colour)
    emb.add_field(name = 'ID', value = role.id)
    emb.add_field(name = 'Цвет', value = role.color)
    emb.add_field(name = 'Упоминается?', value = role.mentionable)
    emb.add_field(name = 'Управляется интеграцией?', value = role.managed)
    emb.add_field(name = 'Позиция в списке', value = role.position)
    now = datetime.datetime.today()
    then = role.created_at
    delta = now - then
    d = role.created_at.strftime('%d/%m/%Y %H:%M:%S UTC')
    emb.add_field(name = 'Создана', value = f'{delta.days} дня(ей) назад. ({d})', inline = False)
    emb.add_field(name = 'Показывает участников отдельно?', value = role.hoist)
    emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['Avatar', 'AVATAR'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def avatar(ctx, member: discord.Member = None):
    await ctx.message.delete()
    if member == None:
        member = ctx.author
    av = 'png'
    av1 = 'webp'
    av2 = 'jpg'
    emb = discord.Embed(colour = member.color)
    emb.add_field(name = '.png', value = f'[Ссылка]({member.avatar_url_as(format = av)})')
    emb.add_field(name = '.webp', value = f'[Ссылка]({member.avatar_url_as(format = av1)})')
    emb.add_field(name = '.jpg', value = f'[Ссылка]({member.avatar_url_as(format = av2)})')
    emb.set_image(url = member.avatar_url)
    emb.set_author(name = member)
    emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['me', 'Me', 'ME', 'About', 'ABOUT'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def about(ctx, member: discord.Member = None):
    await ctx.message.delete()
    if member == None:
        member = ctx.author
    if member.nick == None:
        member.nick = 'Н/Д'
    if member.bot == False:
        bot = 'Неа'
    elif member.bot == True:
        bot = 'Ага'
    emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
    emb.set_author(name = member)
    emb.add_field(name = 'ID', value = member.id)
    now = datetime.datetime.today()
    then = member.created_at
    delta = now - then
    d = member.created_at.strftime('%d/%m/%Y %H:%M:%S UTC')
    then1 = member.joined_at
    delta1 = now - then1
    d1 = member.joined_at.strftime('%d/%m/%Y %H:%M:%S UTC')
    emb.add_field(name = 'Создан', value = f'{delta.days} дня(ей) назад. ({d})', inline = False)
    emb.add_field(name = 'Вошёл', value = f'{delta1.days} дня(ей) назад. ({d1})', inline = False)
    emb.add_field(name = 'Упоминание', value = member.mention)
    emb.add_field(name = 'Raw имя', value = member.name)
    emb.add_field(name = 'Никнейм', value = member.nick)
    limit = len(member.roles)
    if limit > 21:
        emb.add_field(name = 'Роли', value = f'Слишком много для отрисовки ({len(member.roles)-1}) [лимит 20]', inline = False)
    elif limit == 21:
        emb.add_field(name = f'Роли ({len(member.roles)-1}) [лимит достигнут]', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
    elif limit == 20:
        emb.add_field(name = f'Роли ({len(member.roles)-1}) [1 до лимита]', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
    elif limit == 19:
        emb.add_field(name = f'Роли ({len(member.roles)-1}) [2 до лимита]', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
    elif limit == 18:
        emb.add_field(name = f'Роли ({len(member.roles)-1}) [3 до лимита]', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
    else:
        emb.add_field(name = f'Роли ({len(member.roles)-1})', value = ', '.join([role.mention for role in member.roles[1:]]), inline = False)
    emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
    emb.add_field(name = 'Бот?', value = bot)
    emb.set_thumbnail(url = member.avatar_url)
    emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
    await ctx.send(embed = emb)
        
@client.command()
@commands.cooldown(1, 5, commands.BucketType.default)
async def remind(ctx, time: TimeConverter, *, arg):
    await ctx.message.delete()
    emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'Напомню через', value = f'{time}s')
    emb.add_field(name = 'О чём напомню?', value = arg)
    emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
    await ctx.send(embed = emb, delete_after = time)
    await asyncio.sleep(time)
    emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'Напомнил через', value = f'{time}s')
    emb.add_field(name = 'Напоминаю о', value = arg)
    emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
    await ctx.send(f'{ctx.author.mention}', embed = emb)
#Misc

#Fun
@client.command()
@commands.cooldown(1, 3, commands.BucketType.default)
async def aye_balbec(ctx):
    await ctx.message.delete()
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_image(url = 'https://sun9-61.userapi.com/tja5cuQthduwgxq2yMigLiUxfYq_5fqiA6cJWg/sZOkbPajoSY.jpg')
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 3, commands.BucketType.default)
async def rp(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = '[Ныа](https://www.youtube.com/watch?v=idmTSW9mfYI)', colour = discord.Color.green())
    await ctx.send(embed = emb)
        
@client.command(aliases = ['.rap'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def rap(ctx):
    await ctx.message.delete()
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.set_image(url = 'https://thumbs.gfycat.com/MessyCarefreeHousefly-size_restricted.gif')
    await ctx.send(embed = emb)
        
@client.command()
@commands.cooldown(1, 5, commands.BucketType.default)
async def zatka(ctx):
    await ctx.message.delete()
    emb = discord.Embed(title = 'Форма заявки для Набор кадров', colour = ctx.author.color)
    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    emb.add_field(name = '(1). ZATKA в STEAM.  ZATKA_KING#8406 в Discord.', value = 'возраст 14+  часовой пояс IL +0.', inline = False)
    emb.add_field(name = '(2). Интересующая управление:', value = 'Discord', inline = False)
    emb.add_field(name = '(3). Опыт администрирования:', value = 'Есть.', inline = False)
    emb.add_field(name = 'творческие:', value = 'Есть.', inline = False)
    emb.add_field(name = 'технические навыки:', value = 'Нет.', inline = False)
    emb.add_field(name = '(4). Сколько часов готовы уделять работе', value = '[ 15+ в неделю ]', inline = False)
    emb.add_field(name = 'в какое время дня свободны', value = '16:00 до 22:00+', inline = False)
    await ctx.send(embed = emb)

@client.command(aliases = ['Cu', 'CU'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def cu(ctx):
    await ctx.message.delete()
    await ctx.send('Медь')
    
@client.command(aliases = ['c', 'C', 'coin', 'Coin', 'COIN', 'Coinflip', 'COINFLIP'])
@commands.cooldown(3, 3, commands.BucketType.default)
async def coinflip(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = 'Орёл!', colour = discord.Color.green())
    emb.set_image(url = 'https://cdn.discordapp.com/attachments/524213591084105729/763835275930632252/-removebg-preview.png')
    emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
    emb1 = discord.Embed(description = 'Решка!', colour = discord.Color.green())
    emb1.set_image(url = 'https://cdn.discordapp.com/attachments/524213591084105729/763837699240099890/-removebg-preview.png')
    emb1.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
    choices = [emb, emb1]
    rancoin = random.choice(choices)
    await ctx.send(embed = rancoin)
#Fun

#Embeds
@client.command(aliases = ['ctx'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def content(ctx, arg):
    await ctx.message.delete()
    message = await ctx.fetch_message(id = arg)
    if message.author == client.user:
        await ctx.send(f'```cy|say noembed "{message.content}"```')
    else:
        await ctx.send(f'```{message.content}```')

@client.command(aliases = ['emb_ctx'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def emb_content(ctx, arg):
    await ctx.message.delete()
    message = await ctx.fetch_message(id = arg)
    for emb in message.embeds:
        if message.author == client.user:
            await ctx.send(f'```cy|say "" "" t& {emb.title} d& {emb.description} f& {emb.footer.text} c& {emb.colour} a& {emb.author.name} img& {emb.image.url} fu& {emb.thumbnail.url}```')
        else:
            await ctx.send(f'```title {emb.title} description {emb.description} footer {emb.footer.text} color {emb.colour} author {emb.author.name} image {emb.image.url} footer img {emb.thumbnail.url}```')
            
@client.command(aliases = ['emb_e'])
@commands.has_permissions(mention_everyone = True)
@commands.cooldown(1, 20, commands.BucketType.default)
async def say_everyone(ctx, arg = None, text = None, t = None, d = None, img = None, f = None, c = None, a : discord.Member = None):
    await ctx.message.delete()
    if c == None:
        c = ctx.author.color
    else:
        c = int('0x' + c, 16)
    if a == None:
        a = ctx.author
    if img == None:
        img = ('')
    if f == None:
        f = ('')
    emb = discord.Embed(title = t, description = d, colour = c)
    emb.set_author(name = a, icon_url = a.avatar_url)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
    if arg == 'noembed':
        await ctx.send('@everyone ' + text)
    elif arg != 'noembed':
        await ctx.send('@everyone', embed = emb)
    
@client.command(aliases = ['Say', 'SAY'])
@commands.has_permissions(manage_channels = True)
async def say(ctx, arg = None, text = None, t = None, d = None, img = None, f = None, c = None, a : discord.Member = None, *, role: discord.Role = None):
    await ctx.message.delete()
    if c == None:
        c = ctx.author.color
    else:
        c = int('0x' + c, 16)
    if a == None:
        a = ctx.author
    if img == None:
        img = ('')
    if f == None:
        f = ('')
    if role != None:
        c = role.color
    emb = discord.Embed(title = t, description = d, colour = c)
    emb.set_author(name = a, icon_url = a.avatar_url)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
    if role is not None and arg != 'noembed':
        await ctx.send(f'{role.mention}', embed = emb)
    elif role is None and arg != 'noembed':
        await ctx.send(embed = emb)
    if arg == 'noembed':
        await ctx.send(text)

@client.command(aliases = ['emb_ed'])
@commands.has_permissions(manage_channels = True)
async def emb_edit(ctx, arg, t = None, d = None, img = None, f = None, c = None, a : discord.Member = None):
    await ctx.message.delete()
    message = await ctx.fetch_message(id = arg)
    if c == None:
        c = ctx.author.color
    else:
        c = int('0x' + c, 16)
    if a == None:
        a = ctx.author
    if img == None:
        img = ('')
    if f == None:
        f = ('')
    emb = discord.Embed(title = t, description = d, colour = c)
    emb.set_author(name = a, icon_url = a.avatar_url)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
    await message.edit(embed = emb)
    await ctx.send('👌', delete_after = 1)
    
@client.command(aliases = ['Edit', 'EDIT'])
@commands.has_permissions(manage_channels = True)
async def edit(ctx, arg, *, text):
    await ctx.message.delete()
    message = await ctx.fetch_message(id = arg)
    if text == '--delete':
        await message.edit(content = None)
        await ctx.send('👌', delete_after = 1)
    else:
        await message.edit(content = text)
        await ctx.send('👌', delete_after = 1)
#Embeds

#Cephalon
@client.command(aliases = ['Join', 'JOIN'])
async def join(ctx):
    await ctx.message.delete()
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
    else:
        emb = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = discord.Color.green())
        emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
        await ctx.send(embed = emb)
        return
    vc = await channel.connect()

@client.command(aliases = ['Ping', 'PING'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def ping(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = f'Pong! `{round(client.latency * 1000)} ms`', colour = discord.Color.green(), timestamp = ctx.message.created_at)
    await ctx.send(embed = emb)

@client.command(aliases = ['Info', 'INFO'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def info(ctx):
    await ctx.message.delete()
    emb = discord.Embed(colour = discord.Color.green())
    emb.set_author(name = client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = client.user.avatar_url)
    emb.add_field(name = 'Версия', value = '0.12.7.9018')
    emb.add_field(name = 'Написан на', value = 'discord.py')
    emb.add_field(name = 'Разработчик', value = 'сасиска#2472')
    emb.add_field(name = 'Веб-сайт', value = '```http://ru-unioncraft.ru/```')
    emb.add_field(name = 'Существую на', value = f'{len(client.guilds)} серверах')
    emb.set_footer(text = 'Данное приложение не имеет никакого причастия к игре Warframe.', icon_url = 'https://i.playground.ru/p/yVaOZNSTdgUTxmzy_qvzzQ.png')
    await ctx.send(embed = emb)

@client.command(aliases = ['invcy'])
@commands.cooldown(1, 3, commands.BucketType.default)
async def invite(ctx):
    await ctx.message.delete()
    emb = discord.Embed(description = '[Ссылка](https://discord.com/oauth2/authorize?client_id=764882153812787250&scope=bot&permissions=8) для быстрого приглашения бета версии на сервера. Эта версия отличается ранними апдейтами, но недоступна для массовой публики. Однако ссылку может получить каждый, прописав эту команду.', colour = discord.Color.green())
    await ctx.send(embed = emb)
#Cephalon
        
#корень
@client.command(aliases = ['Help', 'HELP'])
@commands.cooldown(1, 3, commands.BucketType.default)
async def help(ctx, arg = None):
    await ctx.message.delete()
    if arg == None:
        emb = discord.Embed(title = "Меню команд Cephalon Cy", description = 'Существует дополнительная помощь по командам, пропишите cy|help |команда|', colour = discord.Color.green())
        emb.add_field(name = 'cy|about', value = 'Показывает информацию о человеке.')
        emb.add_field(name = 'cy|avatar', value = 'Показывает аватар человека.')
        emb.add_field(name = 'cy|ban', value = 'Бан человека.')
        emb.add_field(name = 'cy|clear', value = 'Очистка чата.')
        emb.add_field(name = 'cy|dm', value = 'Пишет участнику любой написанный текст.')
        emb.add_field(name = 'cy|edit', value = 'Редактирует сообщение.', inline = False)
        emb.add_field(name = 'cy|say', value = 'От лица бота отправляется высоконастраеваемый эмбед. Может использоваться как say, так и emb')
        emb.add_field(name = 'cy|emb_ctx', value = 'Позволяет увидеть контент эмбеда.')
        emb.add_field(name = 'cy|emb_edit', value = 'Редактирует эмбед. Работает как VAULTBOT', inline = False)
        emb.add_field(name = 'cy|say_everyone', value = 'Совмещает в себе команды everyone и say.')
        emb.add_field(name = 'cy|everyone', value = 'Пишет сообщение от лица бота и пингует @everyone')
        emb.add_field(name = 'cy|give', value = 'Выдаёт роль.', inline = False)
        emb.add_field(name = 'cy|join', value = 'Бот заходит в голосовой канал.')
        emb.add_field(name = 'cy|kick', value = 'Кик человека.')
        emb.add_field(name = 'cy|mute', value = 'Мут человека.', inline = False)
        emb.add_field(name = 'cy|remind', value = 'Может напомнить вам о событии, которое вы не хотите пропустить.')
        emb.add_field(name = 'cy|role', value = 'Показывает информацию о роли')
        emb.add_field(name = 'cy|take', value = 'Забирает роль.', inline = False)
        emb.add_field(name = 'cy|unmute', value = 'Принудительный размут человека.')
        emb.add_field(name = 'Обозначение символов cy|help', value = '|| - опционально, <> - обязательно')
        emb.set_footer(text = 'Обратите внимание, что это Бета версия основного бота.')
        await ctx.send(embed = emb)
    elif arg == 'about':
        await ctx.send('```cy|about |@пинг|```')
    elif arg == 'avatar':
        await ctx.send('```cy|avatar |@пинг|```')
    elif arg == 'ban':
        await ctx.send('```cy|ban <@пинг> |причина|```')
    elif arg == 'clear':
        await ctx.send('```cy|clear <количество> |confirm|```')
    elif arg == 'dm':
        await ctx.send('```cy|dm <@пинг> <текст>```')
    elif arg == 'edit':
        await ctx.send('```cy|edit <ID> <новый текст>```')
    elif arg == 'say':
        await ctx.send('```cy|say |noembed| |text| |title текст| |description текст| |ссылка| |ссылка| |цвет| |@пинг/имя/ID| |@роль/название/ID|(cy|say "" "" "title" "description")```')
    elif arg == 'emb_ctx':
        await ctx.send('```cy|emb_ctx <ID>```')
    elif arg == 'emb_edit':
        await ctx.send('```cy|emb_edit <ID> |title текст| |description текст| |ссылка| |ссылка| |цвет| |@пинг|```')
    elif arg == 'say_everyone':
        await ctx.send('```cy|say_everyone |title текст| |description текст| |ссылка| |ссылка| |цвет| |@пинг/имя/ID| |@роль/название/ID|(cy|say_everyone "" "" "title" "description")```')
    elif arg == 'give':
        await ctx.send('```cy|give <@пинг> <@роль>```')
    elif arg == 'kick':
        await ctx.send('```cy|kick <@пинг> |причина|```')
    elif arg == 'mute':
        await ctx.send('```cy|mute <@пинг> <время(s,m,h,d(15s, 5m, 1h, 5d))> |причина|```')
    elif arg == 'remind':
        await ctx.send('```cy|remind <время(s,m,h,d(15s, 5m, 1h, 5d))> <текст>```')
    elif arg == 'role':
        await ctx.send('```cy|role <@роль>```')
    elif arg == 'take':
        await ctx.send('```cy|take <@пинг> <@роль>```')
    elif arg == 'unmute':
        await ctx.send('```cy|unmute <@пинг> |причина|```')
    else:
        emb = discord.Embed(description = 'Для этой команды не нужны аргументы', colour = discord.Color.green())
        emb.set_footer(text = 'Хотя, возможно, вы ввели команду неправильно?')
        await ctx.send(embed = emb)

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = 'Discord API'))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        emb = discord.Embed(description = f'{ctx.author.mention}, команда в кд, потерпи чутка!', colour = discord.Color.green())
        await ctx.send(embed = emb)
#корень
         
t = os.environ.get('t')
client.run(t)
