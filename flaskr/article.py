from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import os
from bson.objectid import ObjectId
from flaskr.db import Connection

bp = Blueprint('article', __name__)
db = Connection('web-scraping')

@bp.route('/')
def index():
    articles=db.articles.find({}).sort('release', -1)
    data = []
    for article in articles:
        id = article['_id']
        title = article['title']
        link = article['link']
        release = article['release']
        dataDict = {
            'id': str(id),
            'title': title,
            'link': link,
            'release': release,
        }
        data.append(dataDict)

    return render_template('article/index.html', articles=data)

@bp.route('/export', methods=('POST',))
def export(path="output", file_name="data.csv"):
    articles=db.articles.find({})

    df = pd.DataFrame(articles)
    os.makedirs(path, exist_ok=True)  
    df.to_csv(os.path.join(path, file_name), index=False)

    return redirect(url_for('article.index'))

@bp.route('/create', methods=('POST',))
def create():
    url = 'https://www.detik.com/terpopuler/news'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        for article in soup.find_all('article' ,{ 'class': 'list-content__item'}):
            title = article.find('h3' ,{'class' : 'media__title'}).text
            link = article.find('a',{'class':'media__link'}).get('href')
            date_element = article.find('span', {'title': True})
            release = date_element['title']
            
            error = None

            if not title:
                error = 'Title is required.'

            row=db.articles.find_one({"link": link})
            if row:
                continue

            if error is not None:
                flash(error)
            else:
                db.articles.insert_one({
                    "title": title,
                    "link": link,
                    "release": release
                })
    
    return redirect(url_for('article.index'))

@bp.route('/<string:id>/delete', methods=('POST',))
def delete(id):
    db.articles.delete_one({'_id': ObjectId(id)})

    return redirect(url_for('article.index'))