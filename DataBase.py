from sqlite3 import connect

client = connect("/home/nf/Documents/python/MangaBot/database.db")
cursor = client.cursor()


def main_data(table_name, id, manga_name):
    if 'capitulo' in manga_name:
        manga_name = manga_name[:manga_name.find(' capitulo')]
    table = f'{table_name}_{id}'
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (manga_name text)")
    client.commit()
    rows = cursor.execute(f"SELECT * FROM {table}")
    names = []
    for row in rows:
        names += [str(row)]
    if manga_name in str(names):
        cursor.execute(f"DELETE FROM {table} WHERE manga_name='{manga_name}'")
    else:
        if "readed" in table_name:
            try:
                cursor.execute(f"DELETE FROM read_later_{id} WHERE manga_name='{manga_name}'")
            except:
                pass
        cursor.execute(f"INSERT INTO {table} VALUES ('{manga_name}')")
    client.commit()


def get_from_data(table):
    final_data = []
    try:
        mangas = cursor.execute(f"SELECT * FROM '{table}'")
        for manga in mangas:
            final_data += [manga[0]]
    except:
        final_data = None
    return final_data
