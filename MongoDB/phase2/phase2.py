import wget
import urllib 
import os
import io
import re
import tweepy
import json
from tweepy import OAuthHandler
import requests
import subprocess
import sys
from PIL import Image
import time

# Imports the Google Cloud client library
from google.cloud import vision

from google.cloud.vision import types
from os import listdir
from pymongo import MongoClient
import pprint
import bson



#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_all_tweets(screen_name,videoname, labels_name):
    try:
        for n in range(20):
            os.remove(str(n) + ".jpg")
    except:
        pass
    try:
        os.remove(videoname)
    except:
        pass
    try:
        os.remove(labels_name)
    except:
        pass
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=20)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=20,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if(len(alltweets) > 25):
            break
        print ("...%s tweets downloaded so far" % (len(alltweets)))
    data = {}
    data['Pictures'] = []
    data['Account'] = screen_name
    media_files = set()
    for status in alltweets :
        try :
            media = status.extended_entities.get('media', [])
        except :
            media = status.entities.get('mdeia',[])
        # print (media[0])
        if(len(media) > 0):
            for i in range(len(media)):
             media_files.add(media[i]['media_url'])
    for media_file in media_files:
        print(media_file)
        wget.download(media_file)
    
    os.system("cat *.jpg | ffmpeg -f image2pipe -framerate .5 -i - -vf 'crop=in_w-1:in_h' -vcodec libx264 " + videoname)
    

   # for google vision
    client = vision.ImageAnnotatorClient()
    file = open(labels_name,"w")

    
    picNum = 0
    OBJ = [pic for pic in listdir(".") if pic.endswith('jpg') or pic.endswith('png')]
    
    idx = 0
    for i in OBJ:

        file_name = os.path.join(os.path.dirname(__file__),i)      
        new_name = str(picNum) +'.jpg'

              
        os.renames(file_name, new_name)
        nestDIC = {}
        nestDIC['Picture ' + str(idx)] = new_name  
        picNum = picNum + 1
        
        # Loads the image into memory
        with io.open(new_name, 'rb') as image_file:
             content = image_file.read()
       
        image = types.Image(content=content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations
       
        file.write('Lables for '+new_name+' :\n')
       
        
        label_list = []
        for label in labels:
           label_list.append(label.description)
           file.write(label.description+'\n')

        nestDIC['Description ' + str(idx)] =  label_list
        data['Pictures'].append(nestDIC)
        
        idx += 1
    file.close()

    print(data)
    with open('labels.json','w') as JSONObject:
        json.dump(data, JSONObject, indent = 4, sort_keys = True)
    client = MongoClient()
    db = client.picture.database
    collection = db.picture_collection

    posts = db.posts
    # Delete everything if you need
    posts.delete_many({})
    posts.insert_one(data)

    print("This is the data stored in MongoDB: \n")
    pprint.pprint(posts.find_one({'Account':screen_name}))
    # print out everything you have if needed
    # for doc in posts.find({}):
    #     print(doc)
    
if __name__ == '__main__':
    get_all_tweets("@realDonaldTrump",'OutputVideo.mp4',"label.txt")
