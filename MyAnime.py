# #!/usr/bin/env python3


import json
import requests
import bs4
import random
from typing import Optional


class MyAnime:
    """A class to manipulate data from my anime list."""

    _STATUS_ALL = 7

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
        json_request = 0
        all_titles_scores = {}
        while True:
            req = requests.get(
                f'https://myanimelist.net/animelist/{self.nickname}/load.json?offset={json_request}&status={self._STATUS_ALL}')
            soup = bs4.BeautifulSoup(req.text, "lxml")
            select_anime_list = soup.select('p')[0]
            json_format = select_anime_list.getText()
            anime_details = json.loads(json_format)
            anime_score = {anime['anime_title']: anime['score'] for anime in anime_details}
            all_titles_scores = {**all_titles_scores, **anime_score}

            if len(anime_details) < 100:
                break
            json_request += 300

        return all_titles_scores

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
