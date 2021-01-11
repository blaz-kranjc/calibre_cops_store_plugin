# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, division,
                        absolute_import, print_function)

__license__ = 'GPL 3'
__copyright__ = 'Blaz Kranjc <blaz.kranjc91@gmail.com>'
__docformat__ = 'restructuredtext en'

from base64 import b64encode
from contextlib import closing
from urllib.parse import urljoin
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.utils.opensearch.query import Query
from calibre.utils.xml_parse import safe_xml_fromstring
from calibre import (browser, guess_extension)
from calibre_plugins.cops_store.config_widget import ConfigWidget


AUTHORIZE_HEADER = "Authorization"


def get_template(browser, url):
    with closing(browser.open(url, timeout=15)) as f:
        doc = safe_xml_fromstring(f.read())

    for element in doc.xpath('//*[local-name() = "Url"]'):
        template = element.get('template')
        type = element.get('type')
        if template and type:
            return urljoin(url, template)

    for element in doc.xpath('//*[local-name() = "link"]'):
        if element.get('rel') != 'search':
            continue
        href = element.get('href')
        type = element.get('type')
        if href and type:
            return get_template(browser, urljoin(url, href))

    else:
        raise RuntimeError('Unable to find the template to use.')


def is_book(data):
    id = ''.join(data.xpath('./*[local-name() = "id"]/text()')).strip()
    return id.startswith('urn:')


def parse_book(data, base_url):
    s = SearchResult()
    s.detail_item = ''.join(data.xpath(
        './*[local-name() = "id"]/text()')).strip()

    for link in data.xpath('./*[local-name() = "link"]'):
        rel = link.get('rel')
        href = link.get('href')
        type = link.get('type')

        if rel and href and type:
            link_url = urljoin(base_url, href)
            if 'http://opds-spec.org/thumbnail' in rel:
                s.cover_url = link_url
            elif 'http://opds-spec.org/image/thumbnail' in rel:
                s.cover_url = link_url
            elif 'http://opds-spec.org/acquisition/buy' in rel:
                s.detail_item = link_url
            elif 'http://opds-spec.org/acquisition/sample' in rel:
                pass
            elif 'http://opds-spec.org/acquisition' in rel:
                if type:
                    ext = guess_extension(type)
                    if ext:
                        ext = ext[1:].upper().strip()
                        s.downloads[ext] = link_url
    s.formats = ', '.join(s.downloads.keys()).strip()

    s.title = ' '.join(data.xpath(
        './*[local-name() = "title"]//text()')).strip()
    s.author = ', '.join(data.xpath(
        './*[local-name() = "author"]//*[local-name() = "name"]//text()')).strip()

    price_e = data.xpath('.//*[local-name() = "price"][1]')
    if price_e:
        price_e = price_e[0]
        currency_code = price_e.get('currencycode', '')
        price = ''.join(price_e.xpath('.//text()')).strip()
        s.price = currency_code + ' ' + price
        s.price = s.price.strip()

    return s


def search(browser, url, timeout=60):
    with closing(browser.open(url, timeout=timeout)) as f:
        data = safe_xml_fromstring(f.read())
        for entry in data.xpath('//*[local-name() = "entry"]'):
            if is_book(entry):
                yield parse_book(entry, url)
            else:
                for link in entry.xpath('./*[local-name() = "link"]'):
                    href = link.get('href')
                    type = link.get('type')
                    if href and type:
                        next_url = urljoin(url, href)
                        for book in search(browser, next_url, timeout):
                            yield book


class CopsStorePlugin(BasicStoreConfig, StorePlugin):

    _b = None
    _updateBrowser = False

    def browser(self):
        if not self._b:
            self._b = browser().clone_browser()
            self._updateBrowser = True
        if self._updateBrowser:
            if self.config['user'] and self.config['pass']:
                value = self.config['user'] + ':' + self.config['pass']
                value = b64encode(value.encode('ascii')).decode('ascii')
                self._b.set_current_header(AUTHORIZE_HEADER, "Basic " + value)
            else:
                self._b.set_current_header(AUTHORIZE_HEADER)
        return self._b

    def config_widget(self):
        return ConfigWidget(self.config)

    def save_settings(self, config_widget):
        self.config['url'] = config_widget.url()
        self.config['user'] = config_widget.username()
        self.config['pass'] = config_widget.password()
        self._updateBrowser = True

    def search(self, query, max_results=10, timeout=60):
        q = Query(get_template(self.browser(), self.config['url']))
        q.searchTerms = query
        q.count = max_results
        count = 0
        for book in search(self.browser(), q.url(), timeout):
            if count >= max_results:
                return
            else:
                yield book
