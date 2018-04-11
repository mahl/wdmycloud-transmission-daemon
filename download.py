#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import glob
import urllib2
import re
import json
import base64


session_id = '1tdVcent76N0EWZKfzRZosbvG5WAVjDvFTstcpijTLRWPzYz'
url = 'http://wdmycloud:9092/transmission/rpc'
req_session = urllib2.Request(url, '{}')

try:
    r = urllib2.urlopen(req_session)
except urllib2.HTTPError as err:
    html = err.read()
    match = re.search('X-Transmission-Session-Id: ([a-zA-Z0-9]+)', html)
    session_id = match.group(1)

headers = {
    'X-Transmission-Session-Id': session_id,
    'Content-Type': 'json'
}

print session_id

magnetfiles = glob.glob('/shares/Public/torrents/*.txt')
for magnetfile in magnetfiles:
    magnet = ''
    with open(magnetfile) as f:
        magnet = f.readline().rstrip('\n').rstrip('\r')
    if magnet:
        print magnet
        data = '{{"method":"torrent-add","arguments":{{"paused":false,"download-dir":"/mnt/HD/HD_a2/Transmission","filename":"{}"}}}}'.format(magnet)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req).read()
        response = json.loads(response)
        if 'result' in response and response['result'] == 'success':
            print 'ok' 
            os.remove(magnetfile)
            
torrentfiles = glob.glob('/shares/Public/torrents/*.torrent')
for torrentfile in torrentfiles:
    torrent = ''
    with open(torrentfile) as f:            
        torrent = f.read()
    if torrent:
        torrent = base64.b64encode(torrent).decode('utf-8')
        data = '{{"method":"torrent-add","arguments":{{"paused":false,"download-dir":"/mnt/HD/HD_a2/Transmission","metainfo":"{}"}}}}'.format(torrent)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req).read()
        response = json.loads(response)
        if 'result' in response and response['result'] == 'success':
            print 'ok'
            os.remove(torrentfile)

            
            
