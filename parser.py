import fetcher
import utils
import cli
import httpx
from bs4 import BeautifulSoup as bs
import asyncio
import json
import os

class Parser:
    """
    A class to parse brochures from the prospektmaschine.de website.

    Attributes:
        concurrent_requests (int): The maximum number of concurrent requests.
        num_retries (int): The number of retries for failed requests.
        timeout (float): The timeout for HTTP requests in seconds.
        retry_delay (float): The delay between retries in seconds.
        client (httpx.AsyncClient): The HTTP client for making asynchronous requests.
        semaphore (asyncio.Semaphore): A semaphore to limit concurrent requests.
    """
    def __init__(self, num_concurrent_requests: int = 5, num_retries: int = 3, timeout: float = 5.0, retry_delay: float = 1.0):
        """
        Initializes the Parser object with configuration for HTTP requests.

        Args:
            num_concurrent_requests (int): The maximum number of concurrent requests. Default is 5.
            num_retries (int): The number of retries for failed requests. Default is 3.
            timeout (float): The timeout for HTTP requests in seconds. Default is 5.0.
            retry_delay (float): The delay between retries in seconds. Default is 1.0.
        """
        self.concurrent_requests = num_concurrent_requests
        self.num_retries = num_retries
        self.timeout = timeout
        self.retry_delay = retry_delay
        self.client = httpx.AsyncClient()
        self.semaphore = asyncio.Semaphore(num_concurrent_requests)
        self.base_url = "https://www.prospektmaschine.de"

    def run(self) -> list[dict]:
        """
        Orchestrates the fetching and parsing of brochure data.

        Returns:
            list[dict]: A list of dictionaries containing parsed brochure data.
        """
        results, shops = asyncio.run(fetcher.gather_all_content(self))
        output = []
        for i, shop in enumerate(shops):
            brochures = self.parse_brochures(results[i], shop)
            output.extend(brochures)
        return output

    def parse_brochures(self, html: str, shop: str) -> list[dict]:
        """
        Parses the HTML content of a shop's page to extract brochure data.

        Args:
            html (str): The HTML content of the shop's page.
            shop (str): The name of the shop.

        Returns:
            list[dict]: A list of dictionaries containing brochure data, including title, validity, link, and thumbnail.
        """
        soup = bs(html, "lxml")
        # Locate the grid containing brochures
        grid = soup.find("div", attrs={"class": "letaky-grid"})
        brochures = grid.find_all("div", attrs={"class": "letak-description"})
        output = []

        # Extract necessary information from each brochure
        for brochure in brochures:
            validity = brochure.find("small", attrs={"class": "hidden-sm"})
            valid, brochure_dict = utils.validity_check(validity.text)
            if not valid:
                continue

            title = brochure.find("strong").text
            brochure_dict["title"] = title
            brochure_dict["shop_name"] = shop
            
            link = brochure.find("a").get("href")
            brochure_dict["link"] = self.base_url + link

            container = brochure.parent.parent

            thumbnail = container.find(utils.filter_thumbnail).get("src")
            if thumbnail is None:
                thumbnail = container.find(utils.filter_thumbnail).get("data-src")
            brochure_dict["thumbnail"] = thumbnail

            output.append(brochure_dict)

        return output

def main():
    """
    The main entry point of the script. Parses command-line arguments, initializes the Parser, and writes the output to a file.
    """
    args = cli.parse_args()

    parser = Parser(args.concurrent, args.retries, args.timeout, args.delay)
    output = parser.run()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=3)

if __name__ == "__main__":
    main()