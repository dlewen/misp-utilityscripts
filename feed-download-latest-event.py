#!/usr/bin/env python3
import requests
import pprint
import time
import configparser
import argparse
import sys

"""
Used to download todays misp event from misp feeds that publish once a day
instead of downloading all events in the feed.
The threatfox.abuse.ch misp feed being my usecase.
You'll have to check your misp server feedlist what the feed-id
is on the feed you want to download.
"""

parser = argparse.ArgumentParser()
parser.add_argument('--feedid',help='Feed ID of the feed you want to download todays event from',default=None)

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()


config = configparser.ConfigParser()
config.read("config.ini")

feedId = args.feedid
mispapikey = config['misp']['apikey']
mispurl = config['misp']['url']

pp = pprint.PrettyPrinter(indent=4)

session = requests.Session()
session.headers.update({'Accept': 'application/json'})
session.headers.update({'Content-Type': 'application/json'})
session.headers.update({'Authorization': mispapikey})
url = f'{mispurl}/feeds/previewIndex/{feedId}/sort:date/direction:desc.json'
res = session.get(url)
events = res.json()

fetchurl = f'{mispurl}/feeds/getEvent/{feedId}/'

now = int( time.time() )
# 23h 30min ago
ago = now-84600

for event in events:
    if events[event]['timestamp'] > ago:
        res2 = session.get(fetchurl+event)
