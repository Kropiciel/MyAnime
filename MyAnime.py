# #!/usr/bin/env python3

import re
import requests
import bs4
import random
from typing import Optional


class MyAnime:
    """A class to manipulate data from my anime list."""

    _STATUS_ALL = 7
    _PATTERN_TITLE = 'title":.*?anime'
    _PATTERN_SCORE = 'score":.*?tags'

    def __init__(self, nickname) -> None:
        """Initialize self.

        :param nickname: a nickname of the user to fetch the list for
        """
        self.nickname = nickname

    def get_all_scores(self) -> dict[str, int]:
        """Get the user score map

        Makes a request to MyAnimeList to download the user list.

        :return: a dictionary of anime title to anime score
        """
        req = requests.get(
            f'https://myanimelist.net/animelist/{self.nickname}?status={self._STATUS_ALL}')
        soup = bs4.BeautifulSoup(req.text, "lxml")
        soup_string = str(soup.select('.list-table')[0])

        anime_title: list[str] = [
            title.replace('title":"', '').replace('","anime', '')
            for title in re.findall(self._PATTERN_TITLE, soup_string)
        ]

        anime_score: list[int] = [
            score.replace('score":', '').replace(',"tags', '')
            for score in re.findall(self._PATTERN_SCORE, soup_string)
        ]

        return dict(zip(anime_title, anime_score))

    def get_score_for_title(self, title) -> Optional[int]:
        """Retrieve score for a given title.

        Accepts case-insensitive titles.

        :param title: title of the anime to get the score for

        :return: anime score
        """
        title_score = self.get_all_scores()

        for item_title, item_score in title_score.items():
            if item_title.lower() == title.lower():
                return item_score

        return None

    def random_title(self) -> str:
        """Return random anime title from the user list

        :return: anime title
        """
        titles = list(self.get_all_scores().keys())
        return random.choice(titles)
