import sqlite3
import webbrowser
import csv
conn = sqlite3.connect('database1.db')

c = conn.cursor()

my_user = 'Giovanni'

users_list = [row[0] for row in c.execute("select user_id from spotifon group by user_id")]
items_list = [row[0] for row in c.execute("select song_id from spotifon group by song_id")]


def correlation(x, y):
    if len(x) == len(y):
        n = len(x)
        numerator, denominator1, denominator2 = 0, 0, 0
        mean_x = sum(x)/n
        mean_y = sum(y)/n
        for i in range(n):
            numerator += (x[i]-mean_x)*(y[i]-mean_y)
            denominator1 += (x[i] - mean_x)**2
            denominator2 += (y[i] - mean_y)**2
        if denominator1*denominator2 != 0:
            return numerator/(denominator1*denominator2)**0.5
        elif denominator1 == 0 and denominator2 == 0:
            return 1
        elif denominator1 == 0:
            return 1/denominator2**0.5
        else:
            return 1/denominator1**0.5
    else:
        return 'The arguments must have the same length!'


def get_user_vector(user_id, items):
    dic = {}
    query = "select song_id, listens from spotifon where user_id = '{}'".format(user_id)
    for item in items:
        dic[item] = [item, 0]
    for row in c.execute(query):
        dic[row[0]] = [row[0], row[1]]
    listens_by_song = list(dic.values())
    listens_by_song.sort(key=lambda i: i[0])
    vector = [i[1] for i in listens_by_song]
    return vector


items_for_user = {}

number_of_users = 0  # for control
for user in users_list:
    number_of_users += 1
    if user != my_user:
        x = get_user_vector(my_user, items_list)
        y = get_user_vector(user, items_list)
        corr = correlation(x, y)
        get_user_query = "select song_id, listens from spotifon where user_id = '{}'".format(user)
        print(get_user_query)
        for row in c.execute(get_user_query):
            song = row[0]
            count = row[1]*corr
            if items_for_user.get(song):
                items_for_user[song] += count
            else:
                items_for_user[song] = count
    print(number_of_users)

songs_final_list = [(song, items_for_user[song]) for song in list(items_for_user.keys())]
songs_final_list.sort(key=lambda y: items_for_user[y[0]], reverse=True)
my_user_start_list = [row[0]for row in c.execute("select song_id from spotifon where user_id = '{}'".format(my_user))]
my_user_final_list = [song for song in songs_final_list if song[0] not in my_user_start_list]

url_query = 'select url from song_urls where song = "{}"'.format(my_user_final_list[:1][0][0])
recommended_url = [row[0] for row in c.execute(url_query)][0]
print(recommended_url)

webbrowser.open(recommended_url)
