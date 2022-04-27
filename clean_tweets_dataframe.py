import pandas as pd


class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        print("Automation in Action...!!!")

    def drop_unwanted_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.
        """
        unwanted_rows = df[df["retweet_count"] == "retweet_count"].index
        df.drop(unwanted_rows, inplace=True)
        df = df[df["polarity"] != "polarity"]
        df.reset_index(drop=True, inplace=True)

        return df

    def drop_duplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        drop duplicate rows
        """

        df = df.drop_duplicates(subset="original_text")
        df.reset_index(drop=True, inplace=True)

        return df

    def convert_to_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert column to datetime
        """
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

        return df

    def convert_to_numbers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df["polarity"] = pd.to_numeric(df["polarity"], errors="coerce")
        df["subjectivity"] = pd.to_numeric(df["subjectivity"], errors="coerce")
        df["favorite_count"] = pd.to_numeric(
            df["favorite_count"], errors="coerce"
        )
        df["retweet_count"] = pd.to_numeric(
            df["retweet_count"], errors="coerce"
        )
        df["followers_count"] = pd.to_numeric(
            df["followers_count"], errors="coerce"
        )
        df["friends_count"] = pd.to_numeric(
            df["friends_count"], errors="coerce"
        )

        return df

    def remove_non_english_tweets(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove non english tweets from lang
        """

        df = df.loc[df["lang"] == "en"]
        df.reset_index(drop=True, inplace=True)

        return df

    def drop_null_values(self, df: pd.DataFrame) -> pd.DataFrame:
        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        return df


if __name__ == "__main__":
    data = pd.read_csv("./processed_tweet_data.csv")
    cleaner = Clean_Tweets(data)
    clean_df = cleaner.drop_duplicate(data)
    clean_df = cleaner.remove_non_english_tweets(clean_df)
    clean_df = cleaner.convert_to_numbers(clean_df)
    clean_df = cleaner.convert_to_datetime(clean_df)
    clean_df = cleaner.drop_unwanted_column(clean_df)
    # clean_df = cleaner.drop_null_values(clean_df)
    clean_df.to_csv("./clean_tweet_data.csv", index=False)
