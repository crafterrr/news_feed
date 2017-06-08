import requests
from bs4 import BeautifulSoup
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


engine = create_engine("sqlite:///news.db")
Base.metadata.create_all(bind=engine)

session = sessionmaker(bind=engine)
s = session()


def get_news(page):
    answer_dict = []
    page = BeautifulSoup(page, 'html5lib')
    tables_list = page.table.findAll('table')
    news_table = tables_list[1]
    tr_list = news_table.tbody.findAll('tr')
    for i in range(0, len(tr_list) - 2, 3):
        piece = tr_list[i:i + 2]
        part = piece[1].findAll('td')[1]
        author = part.a.text
        comments = part.findAll('a')[-1].text.split('\xa0')
        if len(comments) == 2 and comments[1] == 'comments':
            comments = comments[0]
        else:
            comments = '0'
        points = part.span.text.split(' ')[0]
        part = piece[0].findAll('td')[2]
        title = part.a.text
        url = part.a.attrs['href']
        if url[0:4] == 'item':
            url = 'https://news.ycombinator.com/'
        url = url.split('/')
        url = url[0] + '//' + url[2] + '/'
        answer_dict.append({'author': author,
                            'comments': comments,
                            'points': points,
                            'title': title,
                            'url': url})

    return answer_dict


if __name__ == '__main__':
    r = requests.get("https://news.ycombinator.com/newest")
    news_list = get_news(r.text)

    for pc in news_list:
        s.add(News(**pc))
    s.commit()
