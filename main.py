import tweepy
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import json

analyzer = SentimentIntensityAnalyzer()


def check_twitter(tag, num, key_tweets):

    consumer_key = "4R8I2k3qdIBrMGVXB21DGkmLn"
    consumer_secret = "GBRX9vQkLQXaa9bpFJrxjCW9kavilxSNhbAOQZQ3cCvlt22Ktn"
    access_token = "1425668954958163971-ExEhBMRLeZXAKoYywohfRoDowANQjG"
    access_token_secret = "7cxCBGdjEidJkGdwBkOQAKe7EHoCuV4JWn6cyN0QOKEre"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    searched_tweets = tweepy.Cursor(api.search, tweet_mode='extended', q=tag, since=datetime.today().strftime('%Y-%m-%d'), count=num).items(num)

    compound = []
    neg_max = 0
    pos_max = 0

    for tweet in searched_tweets:

        if tweet.lang != "en":
            continue

        try:
            sentence = tweet.retweeted_status.full_text
            vs = analyzer.polarity_scores(sentence)
            compound.append(vs['compound'])
            if vs['compound'] > pos_max:
                pos_max = vs['compound']
                key_tweets[tag + " Positive"] = sentence
                key_tweets[tag + " Positive" + " Author"] = tweet.author.screen_name

            if vs['compound'] < neg_max:
                neg_max = vs['compound']
                key_tweets[tag + " Negative"] = sentence
                key_tweets[tag + " Negative" + " Author"] = tweet.author.screen_name

        except AttributeError:
            sentence = tweet.full_text
            vs = analyzer.polarity_scores(sentence)
            compound.append(vs['compound'])
            if vs['compound'] > pos_max:
                pos_max = vs['compound']
                key_tweets[tag + " Positive"] = sentence
                key_tweets[tag + " Positive" + " Author"] = tweet.author.screen_name

            if vs['compound'] < neg_max:
                neg_max = vs['compound']
                key_tweets[tag + " Negative"] = sentence
                key_tweets[tag + " Negative" + " Author"] = tweet.author.screen_name

    if len(compound) > 0:
        mean_c = sum(compound)/len(compound)
    else:
        mean_c = 0.0

    mean_c = round(mean_c, 2)
    print("Analysed search tag", tag,  "at time", datetime.now(), "and calculated", str(mean_c))

    return key_tweets, mean_c


def check_popular_tweets(tag, num, key_tweets):

    consumer_key = "4R8I2k3qdIBrMGVXB21DGkmLn"
    consumer_secret = "GBRX9vQkLQXaa9bpFJrxjCW9kavilxSNhbAOQZQ3cCvlt22Ktn"
    access_token = "1425668954958163971-ExEhBMRLeZXAKoYywohfRoDowANQjG"
    access_token_secret = "7cxCBGdjEidJkGdwBkOQAKe7EHoCuV4JWn6cyN0QOKEre"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    popular_tweets = tweepy.Cursor(api.search, tweet_mode='extended', since=datetime.today().strftime('%Y-%m-%d'),
                                   count=num, q=tag, result_type='popular').items(num)

    pop_max = 0

    for tweet in popular_tweets:

        if tweet.lang != "en":
            continue

        if tweet.favorite_count > pop_max:
            pop_max = tweet.favorite_count
            try:
                sentence = tweet.retweeted_status.full_text
                key_tweets[tag + " Popular"] = sentence
                key_tweets[tag + " Popular" + " Author"] = tweet.author.screen_name
                key_tweets[tag + " Popular" + " Count"] = pop_max
            except AttributeError:
                sentence = tweet.full_text
                key_tweets[tag + " Popular"] = sentence
                key_tweets[tag + " Popular" + " Author"] = tweet.author.screen_name
                key_tweets[tag + " Popular" + " Count"] = pop_max

    print("Analysed search tag", tag,  "at time", datetime.now(), "and calculated", pop_max)

    return key_tweets


while True:

    key_tweet_data = {}
    count = 100

    key_tweet_data = check_popular_tweets("Australia Covid", count, key_tweet_data)

    key_tweet_data, mean_nsw = check_twitter("NSW Covid", count, key_tweet_data)
    key_tweet_data, mean_wa = check_twitter("WA Covid", count, key_tweet_data)
    key_tweet_data, mean_act = check_twitter("ACT Covid", count, key_tweet_data)
    key_tweet_data, mean_sa = check_twitter("SA Covid", count, key_tweet_data)
    key_tweet_data, mean_qld = check_twitter("QLD Covid", count, key_tweet_data)
    key_tweet_data, mean_nt = check_twitter("NT Covid", count, key_tweet_data)
    key_tweet_data, mean_tas = check_twitter("TAS Covid", count, key_tweet_data)
    key_tweet_data, mean_vic = check_twitter("VIC Covid", count, key_tweet_data)

    key_tweet_data, mean_aus = check_twitter("Australia Covid", count, key_tweet_data)

    key_tweet_data, mean_scomo = check_twitter("Scott Morrison", count, key_tweet_data)
    key_tweet_data, mean_gladys = check_twitter("Gladys Berejiklian", count, key_tweet_data)
    key_tweet_data, mean_dan = check_twitter("Daniel Andrews", count, key_tweet_data)

    key_tweet_data, mean_vaxx = check_twitter("Australia Vaccinations", count, key_tweet_data)

    file_object = open('data.csv', 'a')
    file_object.write(str(datetime.now()) + "," +
                      str(mean_nsw) + "," +
                      str(mean_wa) + "," +
                      str(mean_act) + "," +
                      str(mean_sa) + "," +
                      str(mean_qld) + "," +
                      str(mean_nt) + "," +
                      str(mean_tas) + "," +
                      str(mean_vic) + "," +
                      str(mean_aus) + "," +
                      str(mean_scomo) + "," +
                      str(mean_gladys) + "," +
                      str(mean_dan) + "," +
                      str(mean_vaxx) + "\n")
    file_object.close()

    json_file = open('key_tweets.json', 'w')
    json.dump(key_tweet_data, json_file)
    json_file.close()

    time.sleep(60*15)
