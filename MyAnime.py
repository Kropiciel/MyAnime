import re
import requests
import bs4
from random import randrange


class MyAnime:

    def __init__(self, nickname):
        self.nickname = nickname


    def title_score(self, title=''):
        req = requests.get(f'https://myanimelist.net/animelist/{self.nickname}?status=7')
        soup = bs4.BeautifulSoup(req.text, "lxml")
        soup_string = str(soup.select('.list-table')[0])

        pattern_title = 'title":.*?anime'
        anime_title = re.findall(pattern_title, soup_string)

        for item in range(len(anime_title)):
            anime_title[item] = anime_title[item].replace('title":"', '').replace('","anime', '')

        pattern_score = 'score":.*?tags'
        anime_score = re.findall(pattern_score, soup_string)

        for item in range(len(anime_score)):
            anime_score[item] = anime_score[item].replace('score":', '').replace(',"tags', '')

        title_score = {}
        for index in range(len(anime_title)):
            title_score[anime_title[index]] = anime_score[index]

        if title == '':
            return title_score
        else:
            lowercased_anime = dict((title.lower(), score) for title, score in title_score.items())
            return title, lowercased_anime[title]


    def random_title(self, titles):
        listed = list(titles.keys())
        return listed[randrange(len(listed))]


# class MyRandomAnime:

#    def __init__(self, nickname):
#       self.nickname = nickname
#
#    req = requests.get(f'https://myanimelist.net/animelist/{nickname}?status=7')
#    soup = bs4.BeautifulSoup(req.text,"lxml")
#    soup_string = str(soup.select('.list-table')[0])
#
#
#    def random(self):
#        pattern = 'title":.*?anime'
#        anime_title = re.findall(pattern,soup_string)

#       for item in range(len(anime_title)):
#           anime_title[item] = anime_title[item].replace('title":"','').replace('","anime','')
#
#       return anime_title[randrange(len(anime_title))]
#
#
#   def title_score(self):
#       pattern = 'score":.*?tags'
#       anime_score = re.findall(pattern,soup_string)
#
##       for item in range(len(anime_score)):
#          anime_score[item] = anime_score[item].replace('score":','').replace(',"tags','')
#
#       return anime_score
		
		


        
