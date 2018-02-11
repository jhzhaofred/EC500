# TweepyAPI
This library downloads pictures from a Twitter's timeline and convert them into a video and save as a *.mp4 file. 
It also returns, in the form of a dictionary, the description of the images that were downloaded before. 

## Usage
    labels = {}
    labels = get_pics(screen_name, videoname)
    // screen_name is the Twitter's account
    // videoname is the name of the output video, no need to type .mp4
    // labels is the output dictionary

In this case, the pictures are:

<img src="https://github.com/jhzhaofred/EC500/blob/master/TweepyAPI/pics/DVSM-fBX0AEWGHh.jpg" width = "300" height = "200" alt="图片名称" align=center /> <img src="https://github.com/jhzhaofred/EC500/blob/master/TweepyAPI/pics/DVSN1NPXcAAGYiV.jpg" width = "300" height = "200" alt="图片名称" align=center />

The output will be:
    labels = 
    {0: ['Manchester United F.C.'], 1: ['Liverpool F.C.']}
