CREATE DATABASE twitter;

CREATE TABLE IF NOT EXISTS tweets(
 id PRIMARY KEY INT NOT NULL AUTO_INCREMENT,
 created_at DATETIME,
 source VARCHAR(255),
 original_text VARCHAR(255),
 clean_text VARCHAR(255),
 sentiment INTEGER,
 polarity FLOAT,
 subjectivity FLOAT,
 lang VARCHAR(255),
 favorite_count INTEGER,
 retweet_count INTEGER,
 original_author VARCHAR(255),
 followers_count INTEGER,
 friends_count INTEGER,
 possibly_sensitive BOOLEAN,
 hashtags VARCHAR(255),
 user_mentions VARCHAR(255),
 place VARCHAR(255));
