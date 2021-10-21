import discord
import asyncio

client = discord.Client()
answer = ['Hits']
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
        await message.delete()
        day = 0
        store = 0
        save = open("save.txt", "w")
        save.writelines([f'{str(day)}\n', str(store)])
        save.close()
        await message.channel.send('===============================\nOk, Resetting Clan Battle')

    if message.content.startswith('===============================\nDay ') and message.author == client.user:
        emoji = (f'<:physical:896277992966344714>', '<:physical2:896277452320542720>', '<:magic:896274632477376532>',
                 '❓', '⏪')
        for x in emoji:
            await message.add_reaction(x)
        return

    if message.content.startswith('/next') and message.author != client.user and day != 5 and day != 0:
        await message.delete()
        day += 1
        store = await message.channel.send(f'===============================\nDay {str(day)} of Clan Battle\n'
                                           'React <:physical:896277992966344714> For your First Physical Hit\n'
                                           'React <:physical2:896277452320542720> For your Second Physical Hit\n'
                                           'React <:magic:896274632477376532> For your First Magical Hit\n'
                                           'React ❓ For a Third Physical or Magical Hit\n'
                                           'React :rewind: If you have Reset An Attack')
        store = store.id
        save = open("save.txt", "w")
        save.writelines([f'{str(day)}\n', str(store)])
        save.close()
        return

    if message.content.startswith('/start') and day == 0 and message.author != client.user:
        await message.delete()
        day += 1
        store = await message.channel.send(f'===============================\nDay {str(day)} of Clan Battle\n'
                                           'React <:physical:896277992966344714> For your First Physical Hit\n'
                                           'React <:physical2:896277452320542720> For your Second Physical Hit\n'
                                           'React <:magic:896274632477376532> For your First Magical Hit\n'
                                           'React ❓ For a Third Physical or Magical Hit\n'
                                           'React :rewind: If you have Reset An Attack')
        store = store.id
        save = open("save.txt", "w")
        save.writelines([f'{str(day)}\n', str(store)])
        save.close()
        return

    if message.content.startswith('/hits') and message.author != client.user and day != 0:
        physicallist = {}
        magicallist = {}
        clown = {}
        skip = []
        total = {}
        await message.delete()
        hits = await message.channel.history().find(lambda m: m.id == store)
        react = hits.reactions

        for y in await react[0].users().flatten():
            user = str(y)
            physicallist[user] = 1
            magicallist[user] = 0
            total[user] = 1
        for y in await react[1].users().flatten():
            user = str(y)
            if user not in physicallist:
                physicallist.update({user: 1})
            else:
                count = physicallist[user]
                physicallist.update({user: count + 1})
            if user not in total:
                total.update({user: 1})
            if user not in magicallist:
                magicallist.update({user: 0})
        for y in await react[2].users().flatten():
            user = str(y)
            magicallist.update({user: 1})
            if user not in total:
                total.update({user: 1})
            if user not in physicallist:
                physicallist.update({user: 0})
        for y in await react[3].users().flatten():
            user = str(y)
            clown[user] = 1
            if user not in total:
                total.update({user: 1})
        for y in await react[4].users().flatten():
            user = str(y)
            skip.append(user)
            if user not in total:
                total.update({user: 1})
        physicallist.pop('BotBot#4939')
        magicallist.pop('BotBot#4939')
        total.pop('BotBot#4939')
        clown.pop('BotBot#4939')
        skip.pop(0)

        for y in total:
            if y in skip:
                if y in clown:
                    answer.append(f"{str(y)} = {physicallist[y]} P hits | {magicallist[y]} M hit | 1 ? hit | Skip Used")
                else:
                    answer.append(f"{str(y)} = {physicallist[y]} P hits | {magicallist[y]} M hit | Skip Used")
            else:
                if y in clown:
                    answer.append(f"{str(y)} = {physicallist[y]} P hits | {magicallist[y]} M hit | 1 ? hit")
                else:
                    answer.append(f"{str(y)} = {physicallist[y]} P hits | {magicallist[y]} M hit")
        await message.channel.send('\n'.join('{}' for _ in range(len(answer))).format(*answer))
        answer.clear()
        answer.append('Hits')
        return

    if message.content.startswith('\n'.join('{}' for _ in range(len(answer))).format(*answer)):
        await asyncio.sleep(60)
        await message.delete()
        return


asyncio.run(client.run('NTgxMjg1OTQxMDUwNzM2NjUw.XOdCuA.MR6mdDZWQ7Td4HUDdeAreayt0kI'))
