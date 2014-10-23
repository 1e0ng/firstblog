import time
import json
import logging
import traceback

from tornado.web import HTTPError
from bson.objectid import ObjectId
import markdown

from handlers import BaseHandler

class HomeHandler(BaseHandler):
    allow_anony = True
    def get(self):
        pages = list(self.db.page.find({'deleted': False}, sort=[('_id', -1)], limit=30))
        author_mails = [p['author'] for p in pages]
        authors = {u['mail']: u['name'] for u in self.db.user.find({'mail':{'$in': author_mails}})}
        self.render('page_list.html', pages=pages, authors=authors)

class AdminHandler(BaseHandler):
    def get(self):
        query = {'author': self.m} if self.r != 0 else {}
        pages = list(self.db.page.find(query, sort=[('_id', -1)], limit=30))
        author_mails = [p['author'] for p in pages]
        authors = {u['mail']: u['name'] for u in self.db.user.find({'mail':{'$in': author_mails}})}
        self.render('_page_list.html', pages=pages, authors=authors)

    def post(self):
        m =  self.get_argument('m')
        m = json.loads(m)
        self.db.order.drop()
        orders = [{'pid': ObjectId(k), 'order': v} for k, v in m.items()]
        self.db.order.insert(orders)
        self.write({'ok':1})

class PageEditHandler(BaseHandler):
    def get(self, _id):
        page = self.db.page.find_one({'_id': ObjectId(_id)}) if _id else {}
        self.render('_page_form.html', page=page)

    def create(self, title, content, viewed=0):
        page = {
            'title': title,
            'content': content,
            'author': self.m,
            'modified': time.time(),
            'viewed': viewed,
            'deleted': False,
        }
        return self.db.page.insert(page)

    def update(self, page, title, content):
        self.db.page.remove({'_id': page['_id']})
        pid = self.create(title, content, page['viewed'])

        self.db.history.update({'redirect': page['_id']}, {'$set':{'redirect': pid}}, multi=True)
        page['redirect'] = pid
        self.db.history.insert(page)

    def delete(self, _id):
        page = self.db.page.find_one({'_id': ObjectId(_id)})
        deleted = not page['deleted']
        self.db.page.update({'_id':page['_id']}, {'$set':{'deleted': deleted}})

    def post(self, _id):
        action = self.get_argument('action')
        try:
            if action == 'delete':
                self.delete(_id)
            else:
                title = self.get_argument('title')
                content = self.get_argument('content')

                if not _id:
                    self.create(title, content)
                else:
                    page = self.db.page.find_one({'_id': ObjectId(_id)})
                    self.update(page, title, content)
        except Exception, e:
            error_msg = unicode(e) or traceback.format_exc()
            logging.warn(traceback.format_exc())
            self.write(dict(error_msg=error_msg))
            return
        self.write({'ok':1})

class PageHandler(BaseHandler):
    allow_anony = True
    def get(self, _id):
        page = self.db.page.find_one({'_id': ObjectId(_id)})
        if not page:
            raise HTTPError(404)
        self.db.page.update({'_id': page['_id']}, {'$inc': {'viewed': 1}})
        page['content'] = markdown.markdown(page['content'])
        author = self.db.user.find_one({'mail': page['author']})
        self.render('page.html', page=page, author=author)

