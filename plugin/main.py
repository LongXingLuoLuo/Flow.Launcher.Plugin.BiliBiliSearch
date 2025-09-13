# -*- coding: utf-8 -*-
from typing import MutableMapping

from flox import Flox, ICON_SETTINGS
from plugin.bilibili_search import get_search_url, get_query_suggestions
import webbrowser
from plugin.log import logger


class BiliBiliSearchPlugin(Flox):

    def query(self, query) -> None:
        logger.debug(f"Suggest query: {query}")
        for suggestion in get_query_suggestions(query):
            self.add_item(
                title=suggestion,
                subtitle=suggestion,
                icon=ICON_SETTINGS,
                method=self.open_url,
                parameters=[suggestion],
                context=[suggestion]
            )
            logger.info(f"Suggestion add: {suggestion}")

    def context_menu(self, data):
        context = data["context"]
        self.add_item(
            title="打开链接",
            subtitle="Open in BiliBili",
            method="open_url",
            parameters=[context]
        )
        logger.info(f"Context menu add: {context}")
        return self._results

    def open_url(self, query):
        logger.debug(f"Open url: {query}")
        webbrowser.open(get_search_url(query))


if __name__ == "__main__":
    BiliBiliSearchPlugin()
