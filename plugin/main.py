# -*- coding: utf-8 -*-

import webbrowser
from functools import cached_property

from flox import Flox

from plugin.bilibili_search import get_search_url, get_query_suggestions, get_dynamic_url, get_room_info
from plugin.log import logger

ROOM_ID_LIST_SPILT = ','


class BiliBiliSearchPlugin(Flox):

    @cached_property
    def app_icon(self):
        return self.plugindir + "/Images/app.png"

    @property
    def room_id_list(self) -> list[int]:
        room_id_list = self.settings.get("room_id_list", '')
        if room_id_list != '':
            return [int(rid) for rid in room_id_list.split(ROOM_ID_LIST_SPILT) if rid.isdigit()]
        return []

    def query(self, query) -> None:
        logger.debug(f"Suggest query: {query}")
        if query is None or query == "":
            self.add_item(
                title="动态",
                subtitle="动态页面",
                icon=self.app_icon,
                method=self.open_url,
                parameters=[get_dynamic_url()]
            )
            for room_id in self.room_id_list:
                info = get_room_info(room_id)
                if not info.roomStatus:
                    subtitle = "不存在该直播间"
                    self.add_item(
                        title=f"直播: {info.title}",
                        subtitle=subtitle,
                        icon=self.app_icon,
                        context=[room_id]
                    )
                    return
                if info.liveStatus != 1:
                    subtitle = "未开播"
                else:
                    subtitle = f"直播中，观看人数: {str(info.online)}，开播时间: {info.liveTime.strftime('%Y-%m-%d %H:%M:%S')}"
                self.add_item(
                    title=f"直播: {info.title}",
                    subtitle=subtitle,
                    icon=self.app_icon,
                    method=self.open_url,
                    parameters=[info.url],
                    context=[room_id]
                )
            return
        if query.isdigit():
            rid = int(query)
            info = get_room_info(rid)
            if not info.roomStatus or info.liveStatus != 1:
                subtitle = "未开播"
            else:
                subtitle = f"直播中，观看人数: {str(info.online)}，开播时间: {info.liveTime.strftime('%Y-%m-%d %H:%M:%S')}"
            if info.roomStatus:
                self.add_item(
                    title=f"直播: {info.title}",
                    subtitle=subtitle,
                    icon=self.app_icon,
                    method=self.open_url,
                    parameters=[info.url],
                    context=[rid]
                )
        for suggestion in get_query_suggestions(query):
            self.add_item(
                title=suggestion,
                subtitle=suggestion,
                icon=self.plugindir + "/Images/app.png",
                method=self.open_search_url,
                parameters=[suggestion],
            )
            logger.info(f"Suggestion add: {suggestion}")

    def context_menu(self, data):
        rid = data[0]
        self.add_item(
            title=f"添加直播间 {rid}",
            subtitle=f"将该直播间添加到关注列表",
            method=self.add_room_id,
            parameters=[rid]
        )
        self.add_item(
            title=f"移除直播间 {rid}",
            subtitle="从关注列表移除该直播间",
            method=self.remove_room_id,
            parameters=[rid]
        )
        logger.info(f"Context menu add: {data}")

    def open_search_url(self, query: str):
        url = get_search_url(query)
        logger.debug(f"Open search url: {url}")
        self.open_url(url)

    def open_url(self, url: str):
        logger.debug(f"Open url: {url}")
        webbrowser.open(url)

    def add_room_id(self, room_id: int):
        room_id_list = self.room_id_list
        if room_id not in room_id_list:
            room_id_list.append(room_id)
            self.settings["room_id_list"] = ROOM_ID_LIST_SPILT.join([str(rid) for rid in room_id_list])
            logger.debug(f"Room id: {room_id} added to room id: {self.room_id_list}")

    def remove_room_id(self, room_id: int):
        room_id_list = self.room_id_list
        if room_id in room_id_list:
            room_id_list.remove(room_id)
            self.settings["room_id_list"] = ROOM_ID_LIST_SPILT.join([str(rid) for rid in room_id_list])
            logger.debug(f"Room id: {room_id} not in room id: {self.room_id_list}")


if __name__ == "__main__":
    BiliBiliSearchPlugin()
