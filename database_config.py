import sqlite3
conn = sqlite3.connect('database1.db')

c = conn.cursor()

create_1_query = '''
        CREATE TABLE IF NOT EXISTS spotifon
        (user_id text, song_id text, listens integer)
'''
print(create_1_query)
c.execute(create_1_query)

create_2_query = '''
        CREATE TABLE IF NOT EXISTS song_urls
        (song text, url text)
'''
print(create_2_query)
c.execute(create_2_query)

total_songs, total_users, total_listens = 0, 0, 0
songs_dict = {}
users_dict = {}

gender_songs_dict = {
    "pop": [["eletronica", "rap"], [
        ("Michael Jackson - Billie Jean", "https://www.youtube.com/watch?v=Zi_XLOBDo_Y"),
        ("Britney Spears - Criminal", "https://www.youtube.com/watch?v=s6b33PTbGxk"),
        ("Katy Perry - Dark Horse", "https://www.youtube.com/watch?v=0KSOMA3QBU0"),
        ("One Direction - What Makes You Beautiful", "https://www.youtube.com/watch?v=QJO3ROT-A4E"),
        ("Beyoncé - Single Ladies", "https://www.youtube.com/watch?v=4m1EFMoRFvY")
    ]],
    "bossa nova": [["samba", "musica classica"], [
        ("Tom Jobim - Garota de Ipanema", "https://www.youtube.com/watch?v=KOQShDfOwuI"),
        ("João Gilberto - Chega de Saudade", "https://www.youtube.com/watch?v=yUuJrpP0Mak"),
        ("Vinícius de Moraes - Samba da Bênção", "https://www.youtube.com/watch?v=KEAxP_B2wcM"),
        ("Elis Regina - Como Nossos Pais", "https://www.youtube.com/watch?v=2qqN4cEpPCw"),
        ("Toquinho - Onde Anda Você", "https://www.youtube.com/watch?v=Gb5sbORA62w")
    ]],
    "pagode": [["samba", "funk"], [
        ("Grupo Revelação - Deixa Acontecer", "https://www.youtube.com/watch?v=tKChV_aBLcc"),
        ("Turma do Pagode - Deixa em Off", "https://www.youtube.com/watch?v=x_uuWhEtm4k"),
        ("Péricles - Se eu Largar o Freio", "https://www.youtube.com/watch?v=lTeb3xT0pG4"),
        ("Sorriso Maroto - O Impossível", "https://www.youtube.com/watch?v=qmKpwRr5Lj0"),
        ("Thiaguinho - Vamo Que Vamo", "https://www.youtube.com/watch?v=wPA9a2KOZBI")
    ]],
    "metal": [["rock"], [
        ("Metallica - Enter Sandman", "https://www.youtube.com/watch?v=CD-E-LDc384"),
        ("System Of A Down - Chop Suey!", "https://www.youtube.com/watch?v=CSvFpBOe8eY"),
        ("Iron Maiden - The Trooper", "https://www.youtube.com/watch?v=y98-ksHnjE4"),
        ("Sepultura - Roots Bloody Roots", "https://www.youtube.com/watch?v=F_6IjeprfEs"),
        ("Slipknot - Before I Forget", "https://www.youtube.com/watch?v=qw2LU1yS7aw")
    ]],
    "rap": [["pop", "funk"], [
        ("Drake - God's Plan", "https://www.youtube.com/watch?v=xpVfcZ0ZcFM"),
        ("Sabotage - Um Bom Lugar", "https://www.youtube.com/watch?v=GA7LcSX8tYE"),
        ("Eminem - Rap God", "https://www.youtube.com/watch?v=XbGs_qK2PQA"),
        ("Snoop Dogg - Smoke Weed Everyday", "https://www.youtube.com/watch?v=KlujizeNNQM"),
        ("Emicida - Hoje Cedo", "https://www.youtube.com/watch?v=PNl9Z587r8o")
    ]],
    "samba": [["bossa nova", "pagode"], [
        ("Alcione - Não Deixe o Samba Morrer", "https://www.youtube.com/watch?v=QZ5hS7KzXX0"),
        ("Zeca Pagodinho - Deixa a Vida Me Levar", "https://www.youtube.com/watch?v=HJzKCFxFlBY"),
        ("Martinho da Vila - Mulheres", "https://www.youtube.com/watch?v=Dy66LbNvDiM"),
        ("Paulinho da Viola - Timoneiro", "https://www.youtube.com/watch?v=EflJ67AAZFc"),
        ("Cartola - Preciso Me Encontrar", "https://www.youtube.com/watch?v=fUjOfsoBhMY")
    ]],
    "rock": [["metal", "musica classica"], [
        ("The Rolling Stones - (I Can't Get No) Satisfaction", "https://www.youtube.com/watch?v=nrIPxlFzDi0"),
        ("The Beatles - Hey Jude", "https://www.youtube.com/watch?v=A_MjCqQoLLA"),
        ("Led Zeppelin - Stairway to Heaven", "https://www.youtube.com/watch?v=xbhCPt6PZIU"),
        ("Legião Urbana - Tempo Perdido", "https://www.youtube.com/watch?v=SAlOfCg1F_E"),
        ("Queen - Bohemian Rhapsody", "https://www.youtube.com/watch?v=fJ9rUzIMcZQ")
    ]],
    "funk": [["rap", "pagode"], [
        ("Claudinho e Buchecha - Quero Te Encontrar", "https://www.youtube.com/watch?v=502h2lATML4"),
        ("Anitta - Vai Malandra", "https://www.youtube.com/watch?v=kDhptBT_-VI"),
        ("DennisDJ - Professor da Malandragem", "https://www.youtube.com/watch?v=-LZyE8XpVzU"),
        ("MC Livinho - Fazer Falta", "https://www.youtube.com/watch?v=b9jo4mk0VQU"),
        ("Os Hawaianos - É o pente", "https://www.youtube.com/watch?v=dEh3dJORNU4")
    ]],
    "musica classica": [["rock", "bossa nova"], [
        ("Beethoven - Symphony No. 9", "https://www.youtube.com/watch?v=t3217H8JppI"),
        ("Bach - Toccata and Fugue in D Minor", "https://www.youtube.com/watch?v=ho9rZjlsyYY"),
        ("Mozart - Symphony No. 40 in G minor", "https://www.youtube.com/watch?v=JTc1mDieQI8"),
        ("Franz Joseph Haydn - Surprise (Symphony no. 94)", "https://www.youtube.com/watch?v=tF5kr251BRs"),
        ("Lobo de Mesquita - Beata Mater - Antífona do Magnificat", "https://www.youtube.com/watch?v=WRkZD6jVWi0")
    ]],
    "eletronica": [["pop"], [
        ("Skrillex - First Of The Year", "https://www.youtube.com/watch?v=2cXDgFwE13g"),
        ("Steve Aoki - Waste It On Me", "https://www.youtube.com/watch?v=bIv16itYi_0"),
        ("Martin Garrix - Tremor", "https://www.youtube.com/watch?v=9vMh9f41pqE"),
        ("David Guetta - Titanium", "https://www.youtube.com/watch?v=JRfuAukYTKg"),
        ("Calvin Harris - Summer", "https://www.youtube.com/watch?v=ebXbLfLACGM")
    ]]
}

for gender in list(gender_songs_dict.keys()):
    data = gender_songs_dict[gender]
    user_songs = data[1][1:]
    for sub_gender in data[0]:
        sub_data = gender_songs_dict[sub_gender]
        user_songs += sub_data[1][:2]
    user_id = gender + '_user'
    count = 0
    for song in user_songs:
        count += 1
        if count <= 4:
            song_query = 'insert into spotifon (user_id, song_id, listens) values ("{}", "{}", 10)'.format(user_id, song[0])
            print(song_query)
            c.execute(song_query)
        else:
            song_query = 'insert into spotifon (user_id, song_id, listens) values ("{}", "{}", 8)'.format(user_id, song[0])
            print(song_query)
            c.execute(song_query)
        url_query = 'insert into song_urls (song, url) values ("{}", "{}")'.format(song[0], song[1])
        c.execute(url_query)

c.execute("""
    insert into spotifon (user_id, song_id, listens) values
    ('{0}', "Led Zeppelin - Stairway to Heaven", 10),
    ('{0}', "Beethoven - Symphony No. 9", 10),
    ('{0}', "Emicida - Hoje Cedo", 10),
    ('{0}', "Michael Jackson - Billie Jean", 10),
    ('{0}', "Queen - Bohemian Rhapsody", 10)
""".format('Giovanni'))

conn.commit()

conn.close()
