import discord
from GetData import *
from DataBase import *
from os import remove

token = "ODU5MTQ3ODAxNjE0MzUyMzk0.YNodvg.JF6teJurHo5WorOGe60o8LjXYhA"

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="!commands"))
    print("ON!")


@client.event
async def on_message(message):
    if not message.author.bot:
        if message.content.startswith("!commands"):
            style = discord.Embed(title="Ohayo!, essa é a menssagem pricipal", colour=discord.Colour.random(),
            description="""!get <nome do manga> para ver se esta disponível.\n!get <manga> capitulo <N capitulo> para um capitulo expecifico.\n!my favs para favoritos\n!my lidos para os lidos\n!my ler depois para a lista de não lidos\n\nsó um recadinho, estou em Beta, não recomendo escolher mangas com mais de 50 capitulos!""")
            await message.channel.send(embed=style)


        if message.content.startswith('!get ') and not 'capitulo' in message.content:
            manga_name = message.content[5:]
            reactions = ['❤️', '📌', '✅','🕑']
            manga_info = get_manga_info(manga_name)
            if manga_info["author"] == '':
                style = discord.Embed(title=':( Infelizmente não tenho esse manga, verifique o nome e tente novamente :)', colour=discord.Colour.random())
                await message.channel.send(embed=style)
            else:
                style = discord.Embed(title=manga_name, colour=discord.Colour.random(), description=f"""Informações do manga;\nAutor: {manga_info["author"]}\nArt: {manga_info["art"]}\n{manga_info["gender"]}\n{manga_info["OriginalCapters"]}\n{manga_info["content"]}\n{manga_info["volume"]}\n{manga_info["color"]}\n {manga_info["censure"]}\n{manga_info["year"]}\n{manga_info["classification"]}""")
                style.set_image(url=manga_info['image'])
                style.set_footer(text="❤️ para adicionar/remover dos favoritos\n📌 para ler agora\n✅ marcar como lido\n🕑 ler mais tarde")
                bot_msg = await message.channel.send(f'<@{message.author.id}> {manga_name}', embed=style)
                for emoji in reactions:
                    await bot_msg.add_reaction(emoji)


        if message.content.startswith("!get ") and "capitulo" in message.content:
            reactions = ["❤️", "📌", "✅", "🕑"]
            msg = message.content.lower()
            manga_name = msg[len('!get '):msg.find(' capitulo')]
            user_capter = msg[msg.find('capitulo'):]
            confirm = try_request(manga_name, user_capter)
            if confirm is True:
                style = discord.Embed(title=f'{manga_name} {user_capter}', description='❤️ para adicionar/remover dos favoritos\n📌 para ler agora\n✅ marcar como lido\n🕑 ler mais tarde', colour=discord.Colour.random())
            elif confirm is False:
                style = discord.Embed(title='Infelizmente não tenho esse ai :(', colour=discord.Colour.random())
            else:
                style = discord.Embed(title='desculpa :( ocorreu um erro no meu banco de dados :(, tente mais tarde.)')
            bot_msg = await message.channel.send(f'<@{message.author.id}> {manga_name} {user_capter}', embed=style)
            for emoji in reactions:
                await bot_msg.add_reaction(emoji)


        if message.content.startswith("!my "):
            option = message.content.lower()[4:]
            options_pt = ['favs', 'lidos', 'ler depois']
            tables = ['favorites', 'readed', 'read_later']
            for op in range(len(options_pt)):
                if options_pt[op] in option:
                    msg = ''
                    row = get_from_data(f'{tables[op]}_{message.author.id}')
                    try:
                        for i in row:
                            msg += f'-{i}\n'
                        break
                    except:
                        msg = 'Vazio'
                        break
            style = discord.Embed(title=options_pt[op], description=msg, colour=discord.Colour.random())
            await message.channel.send(embed=style)

@client.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        reactions = ["❤️", "✅", "🕑"]
        tables = ['favorites', 'readed', 'read_later']
        msg = reaction.message.content.lower()
        if str(reaction) in reactions:
            main_data(f'{tables[reactions.index(str(reaction))]}', user.id, msg[msg.find('>')+len('> '):])

        if str(reaction) == "📌":
            msg = reaction.message.content.lower()
            name = msg[msg.find('> ')+len('> '):]
            name = remover(name)
            if "capitulo" in msg:
                capter = msg[msg.find('capitulo ')+len('capitulo '):]
                manga_capter = get_manga_images(f'https://www.supermangas.site/manga/{name}/{capter}', name, capter)
            else:
                manga_capter = get_manga_images(f'https://www.supermangas.site/manga/{name}/1', name, '1')
            await reaction.message.channel.send(f'Aqui está <@{user.id}>', files=[discord.File(manga_capter)])
            remove(manga_capter)


client.run(token)
