#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from conftest import *

@pytest.mark.usefixtures('manage_driver')
class ChromeTest(object):
    pass

@pytest.mark.usefixtures('manage_mozilla_driver')
class MozillaTest(object):
    pass

@pytest.mark.usefixtures('manage_ie_driver')
class IeTest(object):
    pass

# methods for your tests
def do_something(self, driver):
    pass

# uploader handling with pywinauto
def upload_screenshots_to_ticket(self, driver):
    # connect with pywinauto and press ENTER
    app = pywinauto.application.Application()
    app.connect(title='Open')
    # in uploader select uploading files and
    app.Dialog.Edit0.TypeKeys(
        r'"your_project\src\data\test_jpg_upload.jpg"', with_spaces=False)
    app.Dialog.Edit0.TypeKeys('{ENTER}')