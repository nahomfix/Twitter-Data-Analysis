import json

import pandas as pd
import spacy
from textblob import TextBlob

nlp = spacy.load('en_core_web_sm')


def read_json(json_file: str) -> list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file

    Returns
    -------
    length of the json file and a list of json
    """

    tweets_data = []
    for tweets in open(json_file, 'r'):
        tweets_data.append(json.loads(tweets))

    return len(tweets_data), tweets_data


class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe

    Return
    ------
    dataframe
    """

    def __init__(self, tweets_list):

        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self) -> list:
        status_count = []
        for x in self.tweets_list:
            try:
                status_count.append(x['user']['status_count'])
            except KeyError:
                status_count.append(None)

        return status_count

    def find_full_text(self) -> list:
        text = [x['text'] for x in self.tweets_list]

        return text

    def find_sentiments(self, text) -> list:
        polarity, subjectivity = [], []
        for single_text in text:
            blob = TextBlob(single_text)
            single_polarity, single_subjectivity = blob.sentiment
            polarity.append(single_polarity)
            subjectivity.append(single_subjectivity)
        # for sentence in blob:
        return polarity, subjectivity

    def find_created_time(self) -> list:
        created_at = [x['created_at'] for x in self.tweets_list]

        return created_at

    def find_source(self) -> list:
        source = [x['source'] for x in self.tweets_list]

        return source

    def find_screen_name(self) -> list:
        screen_name = [x['user']['screen_name'] for x in self.tweets_list]
        
        return screen_name

    def find_followers_count(self) -> list:
        followers_count = [x['user']['followers_count'] for x in self.tweets_list]
        
        return followers_count

    def find_friends_count(self) -> list:
        friends_count = [x['user']['friends_count'] for x in self.tweets_list]
        
        return friends_count

    def is_sensitive(self) -> list:
        is_sensitive = []
        for x in self.tweets_list:
            try:
                is_sensitive.append(x['retweeted_status']['possibly_sensitive'])
            except KeyError:
                is_sensitive.append(None)

        return is_sensitive

    def find_favourite_count(self) -> list:
        favorite_count = []
        for x in self.tweets_list:
            try:
                favorite_count.append(x['retweeted_status']['favorite_count'])
            except KeyError:
                favorite_count.append(0)

        return favorite_count

    def find_retweet_count(self) -> list:
        retweet_count = []
        for x in self.tweets_list:
            try:
                retweet_count.append(x['retweeted_status']['retweet_count'])
            except KeyError:
                retweet_count.append(0)

        return retweet_count

    def find_hashtags(self) -> list:
        hashtags = []
        for x in self.tweets_list:
            try:
                hashtags.append(', '.join(y["text"] for y in x["entities"]["hashtags"]))
            except KeyError:
                hashtags.append('')

        return hashtags

    def find_mentions(self) -> list:
        mentions = []
        for x in self.tweets_list:
            try:
                mentions.append(', '.join(y["screen_name"] for y in x["entities"]["user_mentions"]))
            except KeyError:
                mentions.append('')

        return mentions

    def find_location(self) -> list:
        try:
            # location = self.tweets_list['user']['location']
            location = [x['user']['location'] for x in self.tweets_list]
        except KeyError:
            location = []

        return location

    def find_lang(self) -> list:
        lang = [x['lang'] for x in self.tweets_list]

        return lang

    def clean_text(self) -> list:
        clean_text = []

        for x in self.tweets_list:
            doc = nlp(x["text"])
            lemmas = [token.lemma_ for token in doc]
            a_lemmas = [lemma for lemma in lemmas if lemma.isalpha() 
                 or lemma == '-PRON-']
            clean_text.append(' '.join(a_lemmas))
        
        return clean_text

    def find_sentiment(self, text) -> list:
        sentiment = []
        for single_text in text:
            blob = TextBlob(single_text)
            polarity, sensivity = blob.sentiment
            sentiment.append((polarity, sensivity))
        # for sentence in blob:
        return sentiment

    def find_coordinates(self) -> list:
        coordinates = []
        for x in self.tweets_list:
            if "place" in x and x["place"] != None and "bounding_box" in x["place"]:
                coordinates.append(x["place"]["bounding_box"]["coordinates"])
            else:
                coordinates.append(None)
        # for sentence in blob:
        return coordinates

    def get_tweet_df(self, save=False) -> pd.DataFrame:
        """required column to be generated you should be creative and add more features"""

        columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count',
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']

        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        sentiment = self.find_sentiment(text)
        boundaries = self.find_coordinates()
        clean_text = self.clean_text()

        data = zip(created_at, source, text, clean_text, sentiment, polarity, subjectivity, lang, fav_count, retweet_count, screen_name,
                follower_count, friends_count, sensitivity, hashtags, mentions, location, boundaries)

        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('./processed_tweet_data.csv', index=False)
            print('File Successfully Saved!!!')

        return df


if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count',
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']

    _, tweet_list = read_json("./data/Economic_Twitter_Data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df(save=True)

    # use all defined functions to generate a dataframe with the specified columns above
