import urllib2
import xmltodict
from pushbullet import Pushbullet

def start_html(html):
    html.write("<html><head><title>[UARNIUM] Plex Status</title></head><body>")
    
def finish_html(html):
    html.write("</body></html>")

def write_html_entry(html,title,message):
    html.write("<h2>")
    html.write(title)
    html.write("</h2><p>")
    html.write(message)
    html.write("</p>")


# read my push bullet key from a file, so we can commit this.
f = open("/home/bsmith/repos/plex_status/pb_key.txt","r")
x = f.readline()
y = x.strip('\n')
PB_KEY = y
f.close()

db_file = open("/home/bsmith/Dropbox/Public/plex_status/status.txt","w")
html = open("/home/bsmith/Dropbox/Public/plex_status/plex_status.html","w")
start_html(html)

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
            duration = float(obj['MediaContainer']['Video'][i]['@duration'])
            current = float(obj['MediaContainer']['Video'][i]['@viewOffset'])
        else:
            username = str(obj['MediaContainer']['Video'][i]['User']['@title'])
            playing = str(obj['MediaContainer']['Video'][i]['@grandparentTitle'])
            duration = float(obj['MediaContainer']['Video'][i]['@duration'])
            current = float(obj['MediaContainer']['Video'][i]['@viewOffset'])
        progress = float((current/duration)*100)
        progress = round(progress,2)
        message = username + " is Playing \"" + playing  + "\" on Plex and is at " + str(progress) + " percent done"
        title = "[PLEX] " + username + " is Watching"
        print message
        pb = Pushbullet(PB_KEY)
        push = pb.push_note(title,message)
        db_file.write(title)
        db_file.write(message)
        write_html_entry(html,title,message)
elif num_playing == 1 :
    media_type = str(obj['MediaContainer']['Video']['@type'])
    if media_type == "movie":
        username = str(obj['MediaContainer']['Video']['User']['@title'])
        playing = str(obj['MediaContainer']['Video']['@title'])
        duration = float(obj['MediaContainer']['Video']['@duration'])
        current = float(obj['MediaContainer']['Video']['@viewOffset'])
    else:
        username = str(obj['MediaContainer']['Video']['User']['@title'])
        playing = str(obj['MediaContainer']['Video']['@grandparentTitle'])
        duration = float(obj['MediaContainer']['Video']['@duration'])
        current = float(obj['MediaContainer']['Video']['@viewOffset'])
    progress = float((current/duration)*100)
    progress = round(progress,2)
    message = username + " is Playing \"" + playing  + "\" on Plex and is at " + str(progress) + " percent done"
    title = "[PLEX] " + username + " is Watching"
    print message
    pb = Pushbullet(PB_KEY)
    push = pb.push_note(title,message)
    db_file.write(title)
    db_file.write(message)
    write_html_entry(html,title,message)
else:
    print "No one is watching anything"
    db_file.write("No one is watching anything")
    write_html_entry(html,"No Activity","Sad Plex, no activity right now")

f.close()
db_file.close()    
finish_html(html)
html.close()
