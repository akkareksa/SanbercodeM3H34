# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 07:05:22 2020

@author: Kevin
"""

#mencari sentimen positif atau negatif dari postingan jokowidodo

class simple_sentiment_analysis:
    import tweepy
    import sqlite3
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
    
    consumer_key = "JoPmGvLluEyLqyASsz49lE0fh"
    consumer_secret = "sOcYXKBtnWYtIkzjiYS2tw9y7OdeX2qcP3SnZk8FYe5kzLz2ME"
    access_token = "1287763964466610176-K64Z6DDuzE8zLWvH0vn5Q8Nz6d13b1"
    access_token_secret = "ZLA10vZWo27ervw0DgCGLKpWsZ35GtEcmC9ploOqMbKdM"
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    connection = sqlite3.connect('vckevin98_tugas12.db')
    cursor = connection.cursor()
    captured_data = []
    
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    
    positif = ['senang','bahagia','baik','bangga','positif','bagus']
    negatif = ['sedih','kecewa', 'buruk', 'malu', 'negatif', 'gagal']
    
        
    def __init__(self,user,jumlah_post):
        self.user = user
        self.jumlah_post = jumlah_post
        
    def get_data(self):
        self.user_timeline = self.api.user_timeline(id=self.user, count=self.jumlah_post,tweet_mode="extended")
        for item in self.user_timeline:
            self.captured_data.append(item)
            self.c=item
    
    def save_sql(self):
        #panggil fungsi insert
        for item in self.captured_data:
            self.insert_to_lastscrapping()
            self.insert_to_tweet(item)
            self.insert_to_user(item)
    
    def clean_data(self):
        pass
    
    def insert_to_lastscrapping(self):
        #get_last id 
        #next catch, id = last_id+1
        inputlist=[]
        last_id_query = '''SELECT scrapping_id 
                     FROM Lastscraping
                     ORDER BY scrapping_id DESC
                     LIMIT 1 '''
        last_id = (self.cursor.execute(last_id_query)).fetchone()
        if(last_id is None):
            last_id = 0
        else:
            last_id = last_id[0]
        
        print("LAST IDDD: ",last_id)
        if(last_id != 0):
            update_query = '''  UPDATE Lastscraping 
                            SET status = 0
                            WHERE scrapping_id= ?                            
            '''
            self.cursor.execute(update_query,[last_id])
        
        query = '''INSERT INTO Lastscraping (last_get,status)
                        VALUES(DATE(),1)'''
        self.connection.commit()
        self.x = last_id
        self.curr_scrap_id = last_id+1
        self.cursor.execute(query)
        self.connection.commit()
        
    
    def insert_to_sentiment(self,item, tweetid,sentiment):
        #benerin query
        tweetid = item.id
        #sentiment = ....
        query = '''INSERT INTO Sentiment (tweetid,sentiment)
                        VALUES(?,?)'''
        self.cursor.execute(query)
        pass
    
    def insert_to_tweet(self,item):
        #
        tweetid= item.id
        userid = item.user.id
        createdate = item.created_at
        tweet = item.full_text
        cleantweet = self.stemmer.stem(item.full_text)
        self.z = cleantweet
        #clean data 
        list_input = [tweetid,userid,createdate,tweet,cleantweet,self.curr_scrap_id]
        query = '''INSERT INTO Tweet (tweetid,userid,createddate,tweet,cleantweet,scraping_id)
                        VALUES(?,?,?,?,?,?)'''
        self.cursor.execute(query,list_input)
        self.connection.commit()
    
    
    def insert_to_user(self,item):
        userid = item.user.id
        name = item.user.name
        screenname = item.user.screen_name
        location = item.user.location
        accreate = item.user.created_at
        follower = item.user.followers_count 
        friend = item.user.friends_count
        verified = item.user.verified 
        list_input = [userid,name,screenname,location,accreate,follower,friend,verified]
        query = '''INSERT INTO User (userid,screenname,location,acccreate,follower,friend,verified)
                        VALUES(?,?,?,?,?,?,?)'''
        self.cursor.execute(query,list_input)
        self.connection.commit()
        
    
simple_analysis = simple_sentiment_analysis("jokowi",5)
simple_analysis.get_data()
simple_analysis.save_sql()
#%%


