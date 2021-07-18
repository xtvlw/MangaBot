from requests import get
from random import randrange


def remover(name):
    args = '''"'!@#$¨&*()_+=´`[{~^]}<>:?/;.,\|'''
    for i in args:
        name = name.replace(i, '')
    name = name.replace(' ', '-')
    return name


def try_request(name, cap):
    try:
        name = remover(name)
        cap = cap.replace('capitulo ', '')
        link = f'https://www.supermangas.site/manga/{name}/{cap}'
        page = get(link)
        if page.raise_for_status() is None:
            return True
        else:
            return False
    except:
        return None

def get_manga_info(manga='kimi no na wa'):
    manga_name = remover(manga)
    page = get(f'https://www.supermangas.site/manga/{manga_name}').text
    final_data, html = {}, ''

    points = ["Capitulos Originais:</strong> <span>", "Volumes:</strong> ", "Conteúdo:</strong> ", 'Ano:</strong> <span itemprop="copyrightYear">', "Cor:</strong> ", "Censura:</strong> ", "Classificação:</strong> "]
    point_args = ['Capitulos originais: ', 'Volume: ','Conteúdo: ', 'Ano de lançamento: ', 'Cor: ', 'Censura: ', 'Classificação: ']
    final_args = ['OriginalCapters', 'volume', 'content', 'year', 'color', 'censure', 'classification']
    genders = "Genero: "

    for i in page:
        html += i
    del(page)

    start_image_point = 'class="animeCapa"'
    html = html[html.find(start_image_point):]
    html = html[html.find('<img src="')+len('<img src="'):]
    final_data["image"] = html[:html.find('"')]


    start_gender_point = 'https://www.supermangas.site/genero/'
    html = html[html.find('<li class="sizeFull"'):html.find('</li><li')]
    while start_gender_point in html:
        html = html[html.find(start_gender_point)+len(start_gender_point):]
        genders += f"""{html[:html.find('"')]}, """
    final_data["gender"] = genders[:-2]


    author_point = 'https://www.supermangas.site/autor/'
    html = html[html.find(author_point)+len(author_point):]
    final_data["author"] = html[:html.find('"')]
    art_point = 'https://www.supermangas.site/arte/'
    html = html[html.find(art_point)+len(art_point):]
    final_data["art"] = html[:html.find('"')]

    for i in range(len(final_args)):
        start_point = points[i]
        html = html[html.find(points[i])+len(points[i]):]
        final_data[f"{final_args[i]}"] = f"{point_args[i]}{html[:html.find('<')]}"

    return final_data


def get_manga_images(link, name, capter):
    main_page = get(link).text
    html = ''
    for i in main_page:
        html += i
    del(main_page)
    image_links = []
    start_limit = 'class="capituloViewBox"'
    end_limit = '<div class="boxBarraInfo">Informações</div>'
    html = html[html.find(start_limit):html.find(end_limit)]
    while start_limit in html:
        html = html[html.find('data-src="')+len('data-src="'):]
        image_links += [html[:html.find('"')]]
        html = html[html.find(start_limit):]
    arquive = f"/home/nf/Documents/python/MangaBot/mangas/{name}Capitulo{capter}_{randrange(0, 100)}.html"
    arc = open(arquive, 'w')
    for link in image_links:
        arc.write(f'<center><img src={link}></img></center>\n')
    arc.write('<style>body{ background-color: black}</style>')
    arc.close()
    return arquive
