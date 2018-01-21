# coding=utf-8

import json
import logging
import os

import requests
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


def read_and_parse_cookies(cookie_file):
    with open(cookie_file, 'r') as f:
        cookies_str = f.readline()
    cookies_dict = {}
    for item in cookies_str.split(";"):
        k, v = item.split("=", 1)
        cookies_dict[k.strip()] = v.strip()
    return cookies_dict


def to_md_files(username, total_pages, cookie_file, start=1, stop=None, jekyll=True, md_dir='.'):
    if stop is None:
        stop = total_pages
    if not os.path.exists(md_dir):
        os.makedirs(md_dir)

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
    }
    cookies = read_and_parse_cookies(cookie_file)

    for p in range(start, stop + 1):
        logging.info('Page {}'.format(p))

        # get blog in this page
        articles = requests.get(
            'http://blog.csdn.net/jiajiezhuo/article/list/' + str(p), cookies=cookies).text
        soup = BeautifulSoup(articles, 'lxml')
        for article in soup.find_all('li', href=False, class_=True):
            article_class = article['class'][0]
            if 'blog-unit' != article_class:
                continue

            article_a = article.find('a')
            article_id = article_a['href'].split('/')[-1]
            base_url = 'http://write.blog.csdn.net/mdeditor/getArticle'
            params = {
                'id': article_id,
                'username': username
            }

            # get markdown file data via id
            r = requests.get(base_url, params=params, cookies=cookies)
            try:
                data = json.loads(r.text, strict=False)
            except Exception as e:
                logging.error('Something wrong happend. {}'.format(e))

            title = data['data']['title'].strip()
            date = data['data']['create']
            date_without_time = date.split(" ")[0]
            categories = data['data']['categories']

            content = data['data']['markdowncontent']
            if content is None:
                base_url = 'http://mp.blog.csdn.net/postedit/' + article_id
                
                # get html file data via id
                r = requests.get(base_url, params=params, cookies=cookies)
                soup_article_editor = BeautifulSoup(r.text, 'lxml')
                # categories_article = soup_article_editor.find_all('span', class_='name')
                # categories = categories_article.string
                text_area = soup_article_editor.find('textarea', id='editor')
                content = text_area.string

            logging.info('Exporting {} ...'.format(title))

            jekyll_str = ''
            if jekyll:
                jekyll_str = '---\nlayout: post\ntitle: {title}\ndate: {date}\ncategories: {categories}\n---\n\n'.format(title=title, date=date, categories=categories)
            
            # forbidden characters
            forbidden = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
            
            # use id as md file name if there are forbidden characters
            file_name = date_without_time + '-' + title + '.md'
            if any([c in repr(title) for c in forbidden]):
                with open(os.path.join(md_dir, file_name), 'w') as f:
                    output_str = jekyll_str + content
                    f.write(output_str)
            else:
                with open(os.path.join(md_dir, file_name), 'w') as f:
                    output_str = jekyll_str + content
                    f.write(output_str)

    logging.info('Done!')


if __name__ == '__main__':
    to_md_files('jiajiezhuo', 3, 'cookies.txt', 1, 4, True, './mdfiles')