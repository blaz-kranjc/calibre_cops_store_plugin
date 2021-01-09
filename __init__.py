# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, division,
                        absolute_import, print_function)

__license__ = 'GPL 3'
__copyright__ = 'Blaz Kranjc <blaz.kranjc91@gmail.com>'
__docformat__ = 'restructuredtext en'

from calibre.customize import StoreBase


class JernejStore(StoreBase):
    name = 'COPS server store'
    description = 'Store connected to COPS server'
    version = (0, 0, 1)
    actual_plugin = 'calibre_plugins.cops_store.plugin:CopsStorePlugin'
    author = 'Blaz Kranjc'

    drm_free_only = True
    headquarters = 'SI'
    formats = ['EPUB', 'MOBI']
    affiliate = False
