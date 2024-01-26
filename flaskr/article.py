from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import os
from werkzeug.exceptions import abort

from flaskr.db import get_db

bp = Blueprint('article', __name__)

@bp.route('/')
def index():
    db = get_db()
    articles = db.execute(
        'SELECT p.id, title, link, release, created'
        ' FROM article p'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('article/index.html', articles=articles)

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

            db = get_db()
            row = db.execute('SELECT * FROM article WHERE link = ?', (link,)).fetchone()
            if row:
                continue

            if error is not None:
                flash(error)
            else:
                db.execute(
                    'INSERT INTO article (title, link, release)'
                    ' VALUES (?, ?, ?)',
                    (title, link, release)
                )
                db.commit()
    
    return redirect(url_for('article.index'))
    
def get_article(id):
    articles = get_db().execute(
        'SELECT p.id, title, link, release, created'
        ' FROM article p'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if articles is None:
        abort(404, f"Articles id {id} doesn't exist.")

    return articles

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_article(id)
    db = get_db()
    db.execute('DELETE FROM article WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('article.index'))