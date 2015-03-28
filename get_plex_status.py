import xml.etree.ElementTree as ET
import wget
import urllib2
import xmltodict

f = open("temp.xml","wr")
response = urllib2.urlopen('http://192.168.1.24:32400/status/sessions/')
xml = response.read()
f.write(xml)

obj = xmltodict.parse(xml)

num_playing = int(obj['MediaContainer']['@size'])
if num_playing > 1:
    print num_playing
    for i in range(num_playing - 1):
        media_type = str(obj['MediaContainer']['Video']['@type'])
        if media_type == "movie":
            username = str(obj['MediaContainer']['Video'][i]['User']['@title'])
            playing = str(obj['MediaContainer']['Video'][i]['@title'])
            duration = int(obj['MediaContainer']['Video'][i]['@duration'])
            current = int(obj['MediaContainer']['Video'][i]['@viewOffset'])
        else:
            username = str(obj['MediaContainer']['Video'][i]['User']['@title'])
            playing = str(obj['MediaContainer']['Video'][i]['@grandparentTitle'])
            duration = int(obj['MediaContainer']['Video'][i]['@duration'])
            current = int(obj['MediaContainer']['Video'][i]['@viewOffset'])
        progress = int((current/duration)*100)
        print username + " is Playing \"" + playing  + "\" on Plex and is at " + str(progress) + " percent done"
elif num_playing == 1 :
    media_type = str(obj['MediaContainer']['Video']['@type'])
    if media_type == "movie":
        username = str(obj['MediaContainer']['Video']['User']['@title'])
        playing = str(obj['MediaContainer']['Video']['@title'])
        duration = float(obj['MediaContainer']['Video']['@duration'])
        current = float(obj['MediaContainer']['Video']['@viewOffset'])
        print duration,current        
    else:
        username = str(obj['MediaContainer']['Video']['User']['@title'])
        playing = str(obj['MediaContainer']['Video']['@grandparentTitle'])
        duration = float(obj['MediaContainer']['Video']['@duration'])
        current = float(obj['MediaContainer']['Video']['@viewOffset'])
    progress = float((current/duration)*100)
    print username + " is Playing \"" + playing  + "\" on Plex and is at " + str(progress) + " percent done"
else:
    print "No one is watching anything"





