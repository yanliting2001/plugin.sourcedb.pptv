# -*- coding: utf8 -*-

import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import sqlite3
from simpleplugin import Plugin
from common import *
from pptv import PPTVClass
from util import video_database
from customdb import Customdb_Functions
from traceback import print_exc
try:
    import simplejson
except Exception:
    import json as simplejson


ADDON = xbmcaddon.Addon()
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
ADDON_VERSION = ADDON.getAddonInfo('version')
sys.path.append(xbmc.translatePath(os.path.join(ADDON_PATH, 'sourcedb')))
from movies import Movies
plugin = Plugin()
pptv = PPTVClass()
KODI = xbmc.getInfoLabel('System.BuildVersion')[:2]
KODI_DATABASE_PATH = video_database(KODI)
PPTV_DATABASE_PATH = KODI_DATABASE_PATH.replace("MyVideos78", "pptv")
PLUGIN_PPTV_DB_PATH = 'plugin://plugin.sourcedb.pptv'


def log(txt):
    message = '%s: %s' % (ADDON_NAME, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)


def get_actor_list(cursor, movie_id):
    actor_list = []
    item = Customdb_Functions(cursor).get_movie_actors(movie_id)
    if not item:
        return actor_list
    import json
    item = json.dumps(item)
    for item in json.loads(item):
        actor_list.append(item[0])
    return actor_list


def get_listitem(cursor, movie_id, cid):
    customdb = Customdb_Functions(cursor)
    movie_item = customdb.get_movie_item(movie_id)
    if not movie_item:
        return None
    actor_list = get_actor_list(cursor, movie_id)
    listitem = {'label': movie_item[2],
                'label2': "",
                'thumb': "",
                'icon': "",
                'fanart': "",
                'art': {'clearart': "", 'poster': customdb.get_movie_poster(movie_id)},
                'stream_info': {'video': {'codec': "", 'duration': movie_item[13]}},
                'info': {'video': {'genre': movie_item[16], 'year': movie_item[9], 'director': movie_item[17], 'cast': actor_list, 'plot': movie_item[3], 'rating': movie_item[7], 'sorttitle': movie_item[12]}},
                'context_menu': [('Menu Item', 'Action')],
                'url': PLUGIN_PPTV_DB_PATH + "?action=videoinfo&cid=" + cid,
                'is_playable': True,
                'is_folder': False,
                'subtitles': "",
                'mime': ""
                }
    return listitem


def get_listitem_from_json(detail):
    title = detail.get('title')
    actor_list = []
    for actor in detail.get('actors'):
        actor_list.append(actor['name'])
    return {
        "label": title,
        "label2": "",
        "thumb": "",
        "icon": "",
        "fanart": "",
        "art": {"clearart": "", "poster": detail.get('imgurl')},
        "stream_info": {"video": {"codec": "", "duration": detail.get('durationSecond')}},
        "info": {"video": {"genre": ' / '.join(detail.get('catalog').split(',')), 'year': detail.get('year'), 'director': detail.get('director'), 'cast': actor_list, 'plot': detail.get('content'), 'rating': detail.get('douBanScore'), 'sorttitle': get_sorttitle(title)}},
        "context_menu": [("Menu Item", "Action")],
        "url": PLUGIN_PPTV_DB_PATH + "?action=videoinfo&cid=" + detail.get('vid'),
        "is_playable": True,
        "is_folder": False,
        "subtitles": "",
        "mime": ""
    }


def get_related_list(cid):
    data = pptv.get_video_relate(cid)
    data = simplejson.loads(data)
    if data and "items" in data:
        result = data['items']
    else:
        result = None
    return result


def add_update_listitem(kodi_cursor, pptv_cursor, detail):
    mo = Movies(kodi_cursor, pptv_cursor, int(KODI))
    mo.add_update(item_remap(detail))


def item_remap(detail):
    pptv_id = int(detail.get('vid'))
    return {
        "title": detail.get('title'),
        "dateadded": detail.get('onlinetime'),
        "writer": '',
        "director": ' / '.join(detail.get('director').split(',')),
        "actors": detail.get('act').split(','),
        "genres": detail.get('catalog').split(','),
        "genre": ' / '.join(detail.get('catalog').split(',')),
        "tags": [],
        "plot": detail.get('content'),
        "tagline": "",
        "rating": detail.get('douBanScore'),
        "year": detail.get('year'),
        "runtime": detail.get('durationSecond'),
        "country": detail.get('area'),
        "studio": "",
        "sorttitle": get_sorttitle(detail.get('title')),
        "shortplot": detail.get('subtitle'),
        "trailer": "",
        "mpaa": "",
        "source_type": "pptv",
        "source_id": pptv_id,
        "id": pptv_id,
        "playurl": PLUGIN_PPTV_DB_PATH + "?action=videoinfo&cid=" + str(pptv_id),
        "path": PLUGIN_PPTV_DB_PATH + "/",
        "artwork": {
            "poster": detail.get('imgurl'),
            "landscape": detail.get('landscape')
        }
    }


@plugin.action()
def videoinfo(params):
    xbmc.executebuiltin("ActivateWindow(movieinformation)")
    xbmcgui.Window(12003).setProperty("cid", params.cid)


@plugin.action()
def getvideoinfo(params):
    listitem = []
    with sqlite3.connect(KODI_DATABASE_PATH, 120) as kodi_conn,\
            sqlite3.connect(PPTV_DATABASE_PATH, 120) as pptv_conn:
        kodi_cursor = kodi_conn.cursor()
        pptv_cursor = pptv_conn.cursor()
        kodi_id = Customdb_Functions(pptv_cursor).get_movie_id(params.cid)
        if not kodi_id:
            log("kodi id is none")
            return
        item = get_listitem(kodi_cursor, kodi_id, params.cid)
        listitem.append(item)
    return listitem


@plugin.action()
def getrelatedlist(params):
    listitems = []
    related_list = get_related_list(params.cid)
    if not related_list:
        return listitems
    with sqlite3.connect(KODI_DATABASE_PATH, 120) as kodi_conn,\
            sqlite3.connect(PPTV_DATABASE_PATH, 120) as pptv_conn:
        kodi_cursor = kodi_conn.cursor()
        pptv_cursor = pptv_conn.cursor()
        try:
            for item in related_list:
                cid = item['id']
                movie_id = Customdb_Functions(pptv_cursor).get_movie_id(cid)
                if not movie_id:
                    log(str(cid) + " : kodi id is none Now update it")
                    data = simplejson.loads(pptv.get_video_detail(cid))
                    detail = data['v']
                    listitems.append(get_listitem_from_json(detail))
                    add_update_listitem(kodi_cursor, pptv_cursor, detail)
                else:
                    listitems.append(get_listitem(kodi_cursor, movie_id, str(cid)))
        except Exception:
            print_exc()
        pptv_conn.commit()
        kodi_conn.commit()
    return listitems


@plugin.action()
def play(params):
    if not xbmc.getCondVisibility('system.platform.Android'):
        xbmc.Player().play("C:/Download/20160810-111059351.mkv", windowed=True)
        xbmc.executebuiltin("ActivateWindow(fullscreenvideo)")
        return
    cid = params.cid
    data = pptv.get_video_detail(cid)
    data = simplejson.loads(data)
    total_num = data['video_list_count']
    if data and "video_list" in data:
        video_list = data['video_list']['playlink2']
        if total_num == "1":
            vid = video_list['_attributes']['id']
        else:
            vid = video_list[0]['_attributes']['id']
    json = {"cmp": {"pkg": "com.pptv.ott.sdk", "class": "com.pptv.ott.sdk.PlayerActivity"},
            "extra": {"PLAY_TYPE": 0, "PLAY_CID": vid, "PLAY_VID": cid, "USERNAME": "", "TOKEN": ""}}
    xbmc.executebuiltin('XBMC.StartAndroidActivityByJsonIntent("{json}")'.format(json=simplejson.dumps(json)))


log('script version %s started' % ADDON_VERSION)
plugin.run()
log('script version %s stopped' % ADDON_VERSION)
