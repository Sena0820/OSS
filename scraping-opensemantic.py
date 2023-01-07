import requests
from bs4 import BeautifulSoup


def return_semantic_rank(query):
    global site_title
    search = query
    target = 'c92af410-45e1-42f9-868b-bc14bd375d32.json'
    print(f'【検索ワード】{search}')
    point_page = [1, 11, 21, 31, 41]
    for s in point_page:
        url = f'http://yoda.cla.kobe-u.ac.jp:8080/search/?&s={s}view=list&zoom=years&q={search}'
        request = requests.get(url)
        soup = BeautifulSoup(request.text, "html.parser")
        search_site_list = soup.find_all('a', class_='title')
        query_rank = 50
        for rank, site in zip(range(1, 10), search_site_list):
            try:
                site_title = site.text
            except IndexError:
                site_url = site['href'].replace('/url?q=', '')
            # 結果を出力する
            if site_title == target:
                query_rank = rank
                # print(query_rank)
                if s == 11:
                    query_rank += 10
                if s == 21:
                    query_rank += 20
                if s == 31:
                    query_rank += 30
                if s == 41:
                    query_rank += 40
                return query_rank
    return query_rank


print(return_semantic_rank('look'))
