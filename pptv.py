#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
import util


class PPTVClass():
    DETAILHOST = 'epg.api.cp61.ott.cibntv.net'
    RELATEHOST = 'recommend.cp61.ott.cibntv.net'
    DETAILAPI = 'http://' + DETAILHOST + '/'
    RELATEAPI = 'http://' + RELATEHOST + '/'
    PPI = 'AgACAAAAAgAATksAAAACAAAAAFhhPoA6c6A7DfvkYyt22APc1w5-U9eq5FEUyr9iLBpUpnnnNllkZwqRN9RI3cu6j9lIVJKHmXQgCh4K15mHQ1Cd8drT'

    def __init__(self):
        pass

    def get_video_detail(self, cid):
        url = self.DETAILAPI + 'detail.api?auth={auth}&virtual={virtual}&ppi={ppi}&token={token}&appplt={appplt}&appid={appid}&appver={appver}&username={username}&type={type}&platform={platform}&vid={vid}&ver={ver}&lang={lang}&vvid={vvid}&gslbversion={gslbversion}&userLevel={userLevel}&coverPre={coverPre}&format=json'
        url = url.format(
            auth="1",
            virtual="0",
            ppi=self.PPI,
            token="",
            appplt="launcher",
            appid="com.pptv.launcher",
            appver="4.0.3",
            username="",
            type="ppbox.launcher",
            platform="launcher",
            vid=cid,
            ver="3",
            lang="zh_CN",
            vvid="90f1d8a5-106c-48d4-b806-fec3e5fa58fe",
            gslbversion="2",
            userLevel="0",
            coverPre="sp423")
        return util.GetHttpData(url)

    def get_video_relate(self, cid):
        url = self.RELATEAPI + 'recommend?appplt={appplt}&appid={appid}&appver={appver}&src={src}&video={video}&uid={uid}&num={num}&ppi={ppi}&extraFields={extraFields}&userLevel={userLevel}&vipUser={vipUser}&format=json'
        url = url.format(
            appplt="launcher",
            appid="pptvLauncher",
            appver="4.0.4",
            src="34",
            video=cid,
            uid="pptv",
            num=7,
            ppi=self.PPI,
            extraFields="douBanScore,isPay,vt,vipPrice,coverPic,isVip,score,epgCatas",
            userLevel="1",
            vipUser="0")
        return util.GetHttpData(url)

    def get_playinfo(self, vid):
        if not xbmc.getCondVisibility('system.platform.Android'):
            return '[{"url":"C:/Download/20160810-111059351.mkv","ft":0}]'
        return util.GetHttpData('http://127.0.0.1:6666/pivos/getVideoURL?vid={vid}'.format(vid=vid))

    def get_userinfo(self):
        if not xbmc.getCondVisibility('system.platform.Android'):
            return '{"token": "baioHxWw7aoKgFgkQLKuZft9YzUwONazKPnAG8ZATRCr1lEKBsc5MJsA0Yi4Nu9KBPlGYNNxCxlv\nCoXFfLaS7QNBE8x7sEZz9vjlXW7UjtttKPloeqUJ6yxzaElK_vzhkHMUHq9Rpq9K5CQNMLPv9q6Q\nRjF6xmzFiZeZRXoIuXs\n", "username": "13868191875", "vipgrade": 0, "face": ""}'
        return util.GetHttpData('http://127.0.0.1:6667/pivos/getUserInfo?vid=1234')
