import urllib2
import xmltodict
from pushbullet import Pushbullet

# read my push bullet key from a file, so we can commit this.
f = open("/home/bsmith/repos/plex_status/pb_key.txt","r")
x = f.readline()
y = x.strip('\n')
PB_KEY = y
f.close()

# open a temp file to store the xml.
f = open("/home/bsmith/repos/plex_status/temp.xml","wr")
response = urllib2.urlopen('http://192.168.1.24:32400/status/sessions/')
xml = response.read()
f.write(xml)

# Parse out the XML
obj = xmltodict.parse(xml)

# get the number of items currently playing.
num_playing = int(obj['MediaContainer']['@size'])

# if there is more than one, we have to index the video key. 
# so we if on these 2 cases.
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
        string = username + " is Playing \"" + playing  + "\" on Plex and is at " + str(progress) + " percent done"
        print string
        pb = Pushbullet(PB_KEY)
        push = pb.push_note("[PLEX]",string)
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
    string = username + " is Playing \"" + playing  + "\" on Plex and is at " + str(progress) + " percent done"
    print string
    pb = Pushbullet(PB_KEY)
    push = pb.push_note("[PLEX]",string)
else:
    print "No one is watching anything"

