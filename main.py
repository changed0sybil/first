import telebot, json, time, logging
from methods_fork1 import bot

if __name__ == "__main__":
    logging.basicConfig(filename='main_errors.log', level=logging.ERROR)
    with open('brave1_headers.json', 'r') as file:
        twitter_headers = json.load(file)
    with open('twitter_ids_slow.json', 'r') as file:
        twitter_ids_slow = json.load(file)
    objects = []
    for item in twitter_ids_slow:
        key = next(iter(item))
        value = item[key]
        new_object = bot(key, value,twitter_headers)
        objects.append(new_object)
    tg_bot = telebot.TeleBot('1088541375:AAHRmfMk6Mmba33DmTrkFttCuBjKG60iaxQ')
    ds_cookie = "__dcfduid=529061c0c1c711ed8511dd25b8b4486a; __sdcfduid=529061c1c1c711ed8511dd25b8b4486ae63486d605c700019a6dd564d8427dc9a50318a274f2c70f7fa70b4587204192; __cfruid=461d968e3a021702e44b248dc3c3e63a7d6b30ff-1685620150; __cf_bm=lOAy7iLFBomdXEfMgvMmRaOvcn.YUFjcySi6jptvjmE-1685620153-0-AbA7Li9QCsUAB67U/6x7KabXRL7vGdkQtG3EMsY3hCK8E8qaYnsPeu/Sn6aqzDAQ3tg/43QWebZyHL7adqMPcBb6XTgKybH3tGg2oIzEfGQw"
    first_launch = True
    try:
        while(True):
            while(first_launch):
                first_launch = False
                for link in objects:
                    try:
                        with open(f'tweets_ids_backup/{link.name}.txt', 'r') as file:
                            data = json.load(file)
                            #print(data)
                            link.old_tweets = data
                    except FileNotFoundError:
                        link.get_last_tweets()
                        link.update_backup()
                for link in objects:
                    new_tweets_data = link.get_last_tweets()
                    link.new_tweets = (new_tweets_data["array1"])
                    link.tweets_text = (new_tweets_data["array2"])
                    print(new_tweets_data["array1"])
                    print(new_tweets_data["array2"])
                    new_elements = []
                    for index, value in enumerate(link.new_tweets):
                        if value not in link.old_tweets:
                            tg_bot.send_message(chat_id='312773389', text=link.tweets_text[index])
                            print(f"new element:{link.tweets_text[index]}")
                    link.old_tweets = link.new_tweets
                time.sleep(5)
            for link in objects:
                new_tweets_data = link.get_last_tweets()
                link.new_tweets = (new_tweets_data["array1"])
                link.tweets_text = (new_tweets_data["array2"])
                print(new_tweets_data["array1"])
                print(new_tweets_data["array2"])
                new_elements = []
                for tweet in link.new_tweets:
                    if tweet not in link.old_tweets:
                        new_elements.append(tweet)
                        print("Новые элементы:")
                        for element in new_elements:
                            tg_bot.send_message(chat_id='312773389', text=link.tweets_text[0])
                            print(element)
                            break
                        break
                link.old_tweets = link.new_tweets
                link.update_backup()
            time.sleep(3)
    except Exception as e:
        logging.error('Произошла ошибка: %s', str(e))