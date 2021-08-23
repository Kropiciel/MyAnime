# #!/usr/bin/env python3


import json
import requests
import bs4
import random
from typing import Optional
import pandas as pd
from collections import namedtuple

pd.set_option("display.max_rows", 999)
pd.set_option("display.max_columns", 5)
pd.set_option('display.max_colwidth', 150)
pd.set_option("expand_frame_repr", True)


class MyAnime:
    """A class to manipulate data from my anime list."""

    _STATUS_ALL = 7
    _STATUS_DICT = {'1': 'Currently Watching', '2': 'Completed', '3': 'On Hold', '4': 'Dropped', '6': 'Plan to Watch'}

    def __init__(self, nickname) -> None:
        """Initialize self.

        :param nickname: a nickname of the user to fetch the list for
        """
        self.anime_details_all = []
        self.nickname = nickname

    Anime = namedtuple('Anime', 'title, score, status')

    def get_all_scores(self) -> list[Anime]:
        """Get the user score and status map

        Makes a request to MyAnimeList to download the user list.

        :return: a list of tuples of anime title, anime score and anime status
        """
        json_request = 0
        while True:
            req = requests.get(
                f'https://myanimelist.net/animelist/{self.nickname}/'
                f'load.json?offset={json_request}&status={self._STATUS_ALL}')
            soup = bs4.BeautifulSoup(req.text, "lxml")
            select_anime_list = soup.select('p')[0]
            json_format = select_anime_list.getText()
            anime_details = json.loads(json_format)
            self.anime_details_all += anime_details

            if len(anime_details) < 300:
                break
            json_request += 300

        return [self.Anime(anime['anime_title'], anime['score'], self._STATUS_DICT[str(anime['status'])])
                for anime in self.anime_details_all]

    def get_score_for_title(self, title) -> Optional[int]:
        """Retrieve score for a given title.

        Accepts case-insensitive titles.

        :param title: title of the anime to get the score for

        :return: anime score
        """
        title_score = self.get_all_scores()

        for item_title, item_score, item_status in title_score:
            if item_title.lower() == title.lower():
                return item_score

        return None

    def random_title(self) -> str:
        """Return random anime title from the user list

        :return: anime title
        """
        titles = [title for title, score, status in self.get_all_scores()]
        return random.choice(titles)

    def compare_with(self, friend_nickname):
        """Compare user score and anime status with another user for anime title that both have in their lists.

        :param friend_nickname: a nickname of another user to fetch the list for

        :return: A table with a common anime title, both users' scores and anime status
        """
        friend = MyAnime(friend_nickname)

        my_all_scores = self.get_all_scores()
        friend_all_scores = friend.get_all_scores()

        my_all_titles_set = set([title for title, score, status in my_all_scores])
        friend_all_titles_set = set([title for title, score, status in friend_all_scores])

        mutual_anime = my_all_titles_set.intersection(friend_all_titles_set)

        my_mutual_anime_scores = {title: score for title, score, status in my_all_scores if title in mutual_anime}
        friend_mutual_anime_scores = {title: score for title, score, status in my_all_scores if title in mutual_anime}

        my_anime_status = {title: status for title, score, status in my_all_scores}
        friend_anime_status = {title: status for title, score, status in friend_all_scores}

        compared = sorted([(anime, my_mutual_anime_scores[anime], my_anime_status[anime],
                            friend_mutual_anime_scores[anime], friend_anime_status[anime]) for anime in mutual_anime])

        table = pd.DataFrame(compared, columns=['Anime Title', self.nickname, self.nickname + ' anime status',
                                                friend_nickname, friend_nickname + ' anime status'])
        table.index += 1

        return table

ja = MyAnime('Kropiciel')
print(ja.compare_with('feyaxa'))
