#!/usr/bin/env python
# coding=utf8

import urllib2
import re
import StringIO
import gzip
import traceback
import xbmc


def GetHttpData(url, data=None, cookie=None):
    print url
    for i in range(0, 2):
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) {0}{1}'.
                           format('AppleWebKit/537.36 (KHTML, like Gecko) ',
                                  'Chrome/28.0.1500.71 Safari/537.36'))
            req.add_header('Accept-encoding', 'gzip')
            if cookie is not None:
                req.add_header('Cookie', cookie)
            if data:
                response = urllib2.urlopen(req, data, timeout=3)
            else:
                response = urllib2.urlopen(req, timeout=3)
            httpdata = response.read()
            if response.headers.get('content-encoding', None) == 'gzip':
                httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
            response.close()
            match = re.compile('encoding=(.+?)"').findall(httpdata)
            if not match:
                match = re.compile('meta charset="(.+?)"').findall(httpdata)
            if match:
                charset = match[0].lower()
                if (charset != 'utf-8') and (charset != 'utf8'):
                    httpdata = unicode(httpdata, charset).encode('utf8')
            break
        except Exception:
            traceback.print_exc()
            httpdata = '{"status": "Fail"}'
    return httpdata


def video_database(kodi):
    db_version = {
        '13': 78,   # Gotham
        '14': 90,   # Helix
        '15': 93,   # Isengard
        '16': 99,   # Jarvis
        '17': 107,  # Krypton
        '18': 108   # Leia
    }
    return xbmc.translatePath("special://database/MyVideos%s.db"
                              % db_version.get(kodi, "")).decode('utf-8')
