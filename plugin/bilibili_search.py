# -*- coding: utf-8 -*-
from typing import MutableMapping

from requests import get

from plugin.log import logger

proxies: MutableMapping = {"http": None, "https": None}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
suggest_url = r"https://api.bilibili.cn/suggest"
search_url = r"https://search.bilibili.com/all"


def get_query_suggestions(query: str) -> list[str]:
    logger.debug(f"Get query suggestions for {query}")
    if query == "" or query is None:
        logger.debug("Empty query")
        return []
    resp = get(url=suggest_url, params={"term": query}, proxies=proxies, headers=headers)
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
    return f"{search_url}?keyword={query}"

if __name__ == "__main__":
    logger.info("Start bilibili search")
    logger.debug(get_query_suggestions("奶绿"))
    logger.debug(get_search_url("奶绿"))