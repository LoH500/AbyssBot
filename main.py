import discord
import asyncio

client = discord.Client()
answer = ['Total Hits']
text = open("save.txt", "r")
reader = text.readlines()
day = int(reader[0])
store = int(reader[1])
text.close()
save = open("save.txt", "w")
save.writelines([f'{str(day)}\n', str(store)])
save.close()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global day
    global answer
    global store
    global save

    if message.content.startswith('/reset') and message.author != client.user:
        day = 0
        store = 0
        save = open("save.txt", "w")
        save.writelines([f'{str(day)}\n', str(store)])
        save.close()
        await message.channel.send('===============================\nOk, Resetting Clan Battle')

    if message.content.startswith('===============================\nDay ') and message.author == client.user:
        emoji = ('1️⃣', '2️⃣', '3️⃣', '⏪')
        for x in emoji:
            await message.add_reaction(x)
        return

    if message.content.startswith('/next') and message.author != client.user and day != 5 and day != 0:
        await message.delete()
        day += 1
        store = await message.channel.send(f'===============================\nDay {str(day)} of Clan Battle\n'
                                           'React :one: For your First hit\nReact :two: For your Second hit\n'
                                           'React :three: For your Third hit\nReact :rewind: If you have Reset an '
                                           'attack')
        store = store.id
        save = open("save.txt", "w")
        save.writelines([f'{str(day)}\n', str(store)])
        save.close()
        return

    elif day == 5 and message.author != client.user and message.content.startswith('/next'):
        await message.delete()
        day = 0
        save = open("save.txt", "w")
        save.writelines([f'{str(day)}\n', str(store)])
        save.close()
        await message.channel.send('===============================\nClan Battle has ended\nGood Job Abyss')
        return

    if message.content.startswith('/start') and day == 0 and message.author != client.user:
        await message.delete()
        day += 1
        store = await message.channel.send(f'===============================\nDay {str(day)} of Clan Battle\n'
                                           'React :one: For your First hit\nReact :two: For your Second hit\n'
                                           'React :three: For your Third hit\nReact :rewind: If you have Reset an '
                                           'attack')
        store = store.id
        save = open("save.txt", "w")
        save.writelines([f'{str(day)}\n', str(store)])
        save.close()
        return

    if message.content.startswith('/hits') and message.author != client.user and day != 0:
        hitlist = {}
        skip = []
        await message.delete()
        hits = await message.channel.history().find(lambda m: m.id == store)
        react = hits.reactions

        for y in await react[0].users().flatten():
            user = str(y)
            hitlist[user] = 1
        for y in await react[1].users().flatten():
            user = str(y)
            if user not in hitlist:
                hitlist.update({user: 1})
            else:
                count = hitlist[user]
                hitlist.update({user: count + 1})
        for y in await react[2].users().flatten():
            user = str(y)
            if user not in hitlist:
                hitlist.update({user: 1})
            else:
                count = hitlist[user]
                hitlist.update({user: count + 1})
        for y in await react[3].users().flatten():
            user = str(y)
            skip.append(user)
        hitlist.pop('BotBot#4939')
        skip.pop(0)
        for y in hitlist:
            if y in skip:
                answer.append(f"{y} = {hitlist[y]}/3 hits | Skip Used")
            else:
                answer.append(f"{y} = {hitlist[y]}/3 hits | Skip Available")
        await message.channel.send('\n'.join('{}' for _ in range(len(answer))).format(*answer))
        answer.clear()
        answer.append('Total Hits')
        return

    if message.content.startswith('\n'.join('{}' for _ in range(len(answer))).format(*answer)):
        await asyncio.sleep(60)
        await message.delete()
        return


asyncio.run(client.run('NTgxMjg1OTQxMDUwNzM2NjUw.XOdCuA.MR6mdDZWQ7Td4HUDdeAreayt0kI'))