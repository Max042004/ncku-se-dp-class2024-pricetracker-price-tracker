"""
UDN News Scraper Module

This module provides the UDNCrawler class for fetching, parsing, and saving news articles from the UDN website.
The class extends the NewsCrawlerBase and includes functionalities to search for news articles based on a search term,
parse the details of individual articles, and save them to a database using SQLAlchemy ORM.

Classes:
    UDNCrawler: A class to scrape news from UDN.

Exceptions:
    DomainMismatchException: Raised when the URL domain does not match the expected domain for the crawler.

Usage Example:
    crawler = UDNCrawler(timeout=10)
    headlines = crawler.startup("technology")
    for headline in headlines:
        news = crawler.parse(headline.url)
        crawler.save(news, db_session)

UDNCrawler Methods:
    __init__(self, timeout: int = 5): Initializes the crawler with a default timeout for HTTP requests.
    startup(self, search_term: str) -> list[Headline]: Fetches news headlines for a given search term across multiple pages.
    get_headline(self, search_term: str, page: int | tuple[int, int]) -> list[Headline]: Fetches news headlines for specified pages.
    _fetch_news(self, page: int, search_term: str) -> list[Headline]: Helper method to fetch news headlines for a specific page.
    _create_search_params(self, page: int, search_term: str): Creates the parameters for the search request.
    _perform_request(self, params: dict): Performs the HTTP request to fetch news data.
    _parse_headlines(response): Parses the response to extract headlines.
    parse(self, url: str) -> News: Parses a news article from a given URL.
    _extract_news(soup, url: str) -> News: Extracts news details from the BeautifulSoup object.
    save(self, news: News, db: Session): Saves a news article to the database.
    _commit_changes(db: Session): Commits the changes to the database with error handling.
"""

from requests import Response
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from .crawler_base import NewsCrawlerBase, Headline, News, NewsWithSummary

from src.news.models import NewsArticle
import requests
from urllib.parse import quote


class UDNCrawler(NewsCrawlerBase):
    CHANNEL_ID = 2

    def __init__(self, timeout: int = 5) -> None:
        self.news_website_url = "https://udn.com/api/more"
        self.timeout = timeout

    def startup(self, search_term: str) -> list[Headline]:
        """
        Initializes the application by fetching news headlines for a given search term across multiple pages.
        This method is typically called at the beginning of the program when there is no data available,
        hence it fetches headlines from the first 10 pages.

        :param search_term: The term to search for in news headlines.
        :return: A list of Headline namedtuples containing the title and URL of news articles.
        :rtype: list[Headline]
        """
        return self.get_headline(search_term, page=(1, 10))

    def get_headline(
        self, search_term: str, page: int | tuple[int, int]
    ) -> list[Headline]:

        # Calculate the range of pages to fetch news from.
        # If 'page' is a tuple, unpack it and create a range representing those pages (inclusive).
        # If 'page' is an int, create a list containing only that single page number.
        # page_range = range(*page) if isinstance(page, tuple) else [page]
        all_news_data = []
        # iterate pages to get more news data, not actually get all news data
        if page == tuple:
            news = []
            for page in range(1, 10):
                news.append(self._fetch_news(page=page, search_term=search_term))

                for result in news:
                    all_news_data.append(result)
        else:
            all_news_data = self._fetch_news
        return all_news_data


    def _fetch_news(self, page: int, search_term: str) -> list[Headline]:
        response = self._perform_request(url=self.news_website_url, params=self._create_search_params(page=page, search_term=search_term))
        return self._parse_headlines(response=response)

    def _create_search_params(self, page: int, search_term: str) -> dict:
        pageinfo = {
                "page": page,
                "id": f"search:{quote(search_term)}",
                "channelId": 2,
                "type": "searchword",
        }
        return pageinfo

    def _perform_request(self, url: str | None = None, params: dict | None = None) -> Response:
        response = requests.get(url, params=params)
        return response

    @staticmethod
    def _parse_headlines(response: Response) -> list[Headline]:
        all_news_data = response.json()["lists"]
        return all_news_data

    def parse(self, url: str) -> News:
        response = self._perform_request(url=url)
        soup = BeautifulSoup(response.text, "html.parser")
        detailed_news =  self._extract_news(soup=soup, url=url)

        return detailed_news

    @staticmethod
    def _extract_news(soup: BeautifulSoup, url: str) -> News:
        title = soup.find("h1", class_="article-content__title").text
        time = soup.find("time", class_="article-content__time").text
        # 定位到包含文章內容的 <section>
        content_section = soup.find("section", class_="article-content__editor")

        paragraphs = [
            p.text
            for p in content_section.find_all("p")
            if p.text.strip() != "" and "?" not in p.text
        ]

        return News(title=title, url=url, time=time, content=content_section)

    def save(self, news: NewsWithSummary, db: Session):
        db.add(NewsArticle(
            url=news["url"],
            title=news["title"],
            time=news["time"],
            content=" ".join(news["content"]),  # 將內容list轉換為字串
            summary=news["summary"],
            reason=news["reason"],
        ))
        self._commit_changes(db)
        

    @staticmethod
    def _commit_changes(db: Session):
        db.commit()