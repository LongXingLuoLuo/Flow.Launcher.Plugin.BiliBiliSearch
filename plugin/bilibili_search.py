# -*- coding: utf-8 -*-
from datetime import datetime
from typing import MutableMapping

from requests import get

from plugin.log import logger

proxies: MutableMapping = {"http": None, "https": None}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
SUGGEST_URL = r"https://api.bilibili.cn/suggest"
SEARCH_URL = r"https://search.bilibili.com/all"
DYNAMIC_URL = r"https://t.bilibili.com/"
ROOM_INFO_URL = r"https://api.live.bilibili.com/room/v1/Room/get_info"
ROOM_URL = r"https://live.bilibili.com/"

class RoomInfo(object):
    roomStatus: bool # 有无房间
    liveStatus: int # 是否开播
    url: str # 直播间网页 url
    title: str # 直播间标题
    cover: str # 直播间封面 url
    roomId: int # 直播间 id
    online: int # 直播间人气
    liveTime: datetime # 开播时间

    def __init__(self):
        """
        BiliBili 直播间信息数据结构
        """
        self.roomStatus = True
        self.liveStatus = 0
        self.url = ""
        self.title = ""
        self.cover = ""
        self.roomId = 0
        self.online = 0
        self.liveTime = datetime.now()

    def __str__(self):
        return f"RoomInfo(roomStatus={self.roomStatus}, liveStatus={self.liveStatus}, url='{self.url}', title='{self.title}', cover='{self.cover}', roomId={self.roomId}, online={self.online}, liveTime={self.liveTime})"

    def __repr__(self):
        return self.__str__()

def get_query_suggestions(query: str) -> list[str]:
    logger.debug(f"Get query suggestions for {query}")
    if query == "" or query is None:
        logger.debug("Empty query")
        return []
    resp = get(url=SUGGEST_URL, params={"term": query}, proxies=proxies, headers=headers)
    if resp.status_code != 200:
        logger.error(f"Suggest resp: {resp.status_code}")
        return []
    else:
        results = []
        for suggestion in resp.json()["result"]["tag"]:
            results.append(suggestion["value"])
        logger.debug(f"Suggest results: {results}")
        return results

def get_search_url(query: str) -> str:
    logger.debug(f"Search url: {query}")
    return f"{SEARCH_URL}?keyword={query}"

def get_dynamic_url() -> str:
    logger.debug(f"Get dynamic url: {DYNAMIC_URL}")
    return DYNAMIC_URL

def get_room_info(room_id: int) -> RoomInfo:
    logger.debug(f"Get room of mid: {room_id}")
    info = RoomInfo()
    resp = get(url=ROOM_INFO_URL, proxies=proxies, headers=headers, params={"room_id": room_id})
    if resp.status_code != 200:
        logger.debug(f"Get room info resp: {resp.status_code}")
        return info
    if resp.json()["code"] != 0:
        logger.debug(f"Room is not live: {resp.json()}")
        info.roomStatus = False
        return info
    logger.info(f"Get room info resp: {resp.json()}")
    data = resp.json()["data"]
    info.liveStatus = data["live_status"]

    info.title = data["title"]
    info.cover = data["user_cover"]
    info.roomId = data["room_id"]
    info.online = data["online"]
    info.url = f"{ROOM_URL}{info.roomId}"
    if data['live_time'] == "0000-00-00 00:00:00":
        info.liveTime = datetime.now()
    return info

if __name__ == "__main__":
    logger.debug("Start bilibili search")
    logger.debug(get_query_suggestions("奶绿"))
    logger.debug(get_search_url("奶绿"))
    logger.debug(get_dynamic_url())
    logger.debug(get_room_info(898170))
    logger.debug("End bilibili search")