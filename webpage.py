from bottle import route, run, template, redirect, request
from req import s, News, get_news
import requests
from classifier import Model
from operator import itemgetter


naive = Model()
naive.load('freq.pkl')


@route('/add_label/')
def add_label():
    label = request.GET.get('label')
    piece_id = request.GET.get('id')
    row = s.query(News).filter(News.id == piece_id).all()
    row[0].label = label
    s.add(row[0])
    s.commit()
    redirect('/news')


@route('/update_news')
def update_news():
    r = requests.get("https://news.ycombinator.com/newest")
    news_l = get_news(r.text)
    for piece in news_l:
        title = piece['title']
        author = piece['author']
        result = s.query(News).filter(News.title == title)
        result = result.filter(News.author == author).all()
        if len(result) == 0:
            piece = News(title=piece['title'],
                         author=piece['author'],
                         url=piece['url'],
                         comments=piece['comments'],
                         points=piece['points'])
            try:
                print(piece.title)
            except:
                pass
            print(naive.predict(piece))
            s.add(piece)
    s.commit()
    redirect('/news')


@route('/')
@route('/news')
def news_list():
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route('/recommend')
def news_predicted():
    count = request.GET.get('count')
    colors = {'never': '#FF0000', 'maybe': '#FFFF00', 'good': '#00FF00'}
    if count == 'all':
        rows = s.query(News).filter(News.label == None).all()
    else:
        count = int(count)
        rows = s.query(News).filter(News.label == None).all()[-count:]
    rows = [(row, naive.classify(row)) for row in rows]
    rows.sort(key=itemgetter(1))
    rows = [(row[0], colors[row[1]]) for row in rows]
    return template('news_auto', rows=rows)


run(host='localhost', port=8080)
