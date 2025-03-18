# Author: Ivan Rachler
from parser import Parser
import httpx
import asyncio
from typing import Optional
from bs4 import BeautifulSoup as bs

async def get_page_content(parser: Parser, url: str) -> Optional[str]:
    """
    Fetches the html content of a page asynchronously.
    Attempts to retry based on parser configuration in case of failure.

    Args:
        parser (Parser): The Parser object containing configuration.
        url (str): The URL of the page to fetch.
    
    Returns:
        Optional[str]: The html content of the page if successful, None otherwise.
    """
    async with parser.semaphore:
        for _ in range(parser.num_retries):
            try:
                response = await parser.client.get(url, timeout=parser.timeout)
                response.raise_for_status()
            except httpx.HTTPError as e:
                print(f"url: {url}, error: {str(e)}")
                await asyncio.sleep(parser.retry_delay)
            else:
                return response.content
        return None

async def gather_all_content(parser: Parser) -> tuple[list[Optional[str]], list[str]]:
    """
    Fetches the html content of all hypermarkets asynchronously.
    
    Args:
        parser (Parser): The Parser object containing configuration.

    Returns:
        tuple[list[Optional[str]], list[str]]: A tuple containing a list of html content and a list of shop names.
    """
    response = httpx.get(parser.base_url+"/hypermarkte/")
    soup = bs(response.content, "lxml")
    sidebar = soup.find(attrs={"id": "left-category-shops"})
    shops = sidebar.find_all("a")
    shop_urls = [parser.base_url + shop.get("href") for shop in shops]

    async with parser.client:
        tasks = [get_page_content(parser, url) for url in shop_urls]
        results = await asyncio.gather(*tasks)

    return results, [shop.text for shop in shops]