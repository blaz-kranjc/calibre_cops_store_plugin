# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, division,
                        absolute_import, print_function)

__license__ = 'GPL 3'
__copyright__ = 'Blaz Kranjc <blaz.kranjc91@gmail.com>'
__docformat__ = 'restructuredtext en'

from PyQt5.Qt import QWidget, QFormLayout, QLabel, QLineEdit


class ConfigWidget(QWidget):

    def __init__(self, config):
        QWidget.__init__(self)
        self.create_ui()
        self.urlField.setText(config.get('url', ''))
        self.usernameField.setText(config.get('user', ''))
        self.passwordField.setText(config.get('pass', ''))

    def create_ui(self):
        self.urlField = QLineEdit()
        self.usernameField = QLineEdit()
        self.passwordField = QLineEdit()
        layout = QFormLayout()
        layout.addRow("URL:", self.urlField)
        layout.addRow("Username:", self.usernameField)
        layout.addRow("Password:", self.passwordField)
        self.setLayout(layout)

    def url(self):
        return self.urlField.text()

    def username(self):
        return self.usernameField.text()

    def password(self):
        return self.passwordField.text()
