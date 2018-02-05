import tweepy
from tweepy import OAuthHandler
from google.cloud import vision
import io, os
import json
import wget
import glob

consumer_key = 
consumer_secret = 
access_token = 
access_secret = 


@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

def get_pics(screen_name, videoname):
    # Status() is the data model for a tweet
    tweepy.models.Status.first_parse = tweepy.models.Status.parse
    tweepy.models.Status.parse = parse
    # User() is the data model for a user profil
    tweepy.models.User.first_parse = tweepy.models.User.parse
    tweepy.models.User.parse = parse
    # You need to do it for all the models you need

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name=screen_name,
                               count=200, include_rts=False,
                               exclude_replies=True)

    last_id = tweets[-1].id

    media_files = set()
    for status in tweets:
        media = status.entities.get('media', [])
        if(len(media) > 0):
            media_files.add(media[0]['media_url'])

    for media_file in media_files:
        wget.download(media_file)

    # Convert images to *.mp4
    os.system('cat *.jpg | ffmpeg -f image2pipe -framerate .5 -i - ' + videoname)

    #Google Cloud Vision
    # To use, need export Google Vision AnnotatorClient .json file
    labels_dict = {}
    path = glob.glob('*.jpg')
    client = vision.ImageAnnotatorClient()
    idx = 0

    for img in path:
        with io.open(img, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)
        # Print labels or logos
        response = client.label_detection(image=image)
        labels = response.label_annotations
        # response = client.logo_detection(image=image)
        # labels = response.logo_annotations
        labels_dict[idx] = []

        for label in labels:
            labels_dict[count].append(label.description)
        idx += 1

    print(labels_dict)


def main():
    # input is ID and the filename of the video
    # For example: Ibra_official
    get_pics('Ibra_official', 'outputvideo.mp4')

if __name__== "__main__":
  main()