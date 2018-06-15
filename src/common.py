#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from conftest import *

class ChromeTest(object):
    # methods for your tests
    def do_something(self, driver):
        pass

class MozillaTest(object):
    pass

class IeTest(object):
    pass

# uploader handling with pywinauto
def upload_screenshots_to_ticket(self, driver):
    # connect with pywinauto and press ENTER
    app = pywinauto.application.Application()
    app.connect(title='Open')
    # in uploader select uploading files and
    app.Dialog.Edit0.TypeKeys(
        r'"AutoTestsTemplate\src\data\test_jpg_upload.jpg"', with_spaces=False)
    app.Dialog.Edit0.TypeKeys('{ENTER}')