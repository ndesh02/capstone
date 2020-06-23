import json
import urllib.request, urllib.parse, urllib.error
import ssl
import sqlite3

api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'
# https://developers.google.com/maps/documentation/geocoding/intro

if api_key is False:
    api_key = 42
    serviceurl = 'https://data.nasa.gov/resource/gh4g-9sfh.json'
else :
    serviceurl = 'https://data.nasa.gov/resource/gh4g-9sfh.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = serviceurl

print('Retrieving', url)
um = urllib.request.urlopen(url, context=ctx)
data = um.read().decode()

print('Retrieved', len(data), 'characters')

try:
    js = json.loads(data)
except:
    js = None

#if not js or 'status' not in js or js['status'] != 'OK':
#    print('==== Failure to Retrieve ====')
#    print(data)
#    quit()

#Make a file
conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE Meteors')
#Creates the sqlite database
cur.execute('''CREATE TABLE IF NOT EXISTS Meteors
    (id INTEGER PRIMARY KEY, name TEXT UNIQUE, nameType TEXT, recclass TEXT, mass INTEGER,
     fall TEXT, reclat INTEGER, reclong INTEGER, year INTEGER, geolocation TEXT UNIQUE)''')

meteor = dict()
count = 0
name = None
id = None
nameType = None
recclass = None
mass = None
fall = None
reclat = None
reclong = None
year = None
geolocation = None
for item in js:
    meteor = js[count]
    try:
        name = meteor["name"]
    except:
        print("===Name was missing===")

    try:
        id = meteor["id"]
    except:
        print('===ID was missing===')

    try:
        nameType = meteor["nametype"]
    except:
        print('===NameType was missing===')

    try:
        recclass = meteor["recclass"]
    except:
        print('===Reclass was missing===')

    try:
        fall = meteor["fall"]
    except:
        print('===Fall was missing===')

    try:
        reclat = meteor["reclat"]
    except:
        print('===Reclat was missing===')

    try:
        reclong = meteor["reclong"]
    except:
        print("===Reclong was missing===")

    try:
        year = meteor["year"]
        year = year[:4]
    except:
        print('===Year was missing===')

    try:
        geolocation = meteor["geolocation"]["latitude"]+" "+meteor["geolocation"]["longitude"]
    except:
        print('===Geolocation was missing===')

    try:
        mass = meteor["mass"]
    except:
        print('===Mass was missing===')

    print(id, name, nameType, recclass, mass, fall, reclat, reclong, year, geolocation)
    cur.execute('''INSERT OR IGNORE INTO Meteors (id, name, nameType, recclass, mass, fall, reclat, reclong, year, geolocation)
        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (id, name, nameType, recclass, mass, fall, reclat, reclong, year, geolocation))
    if count%50 == 0: conn.commit()
    count = count + 1

conn.commit()
cur.close()
