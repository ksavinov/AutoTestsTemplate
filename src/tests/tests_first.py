#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from common import *

@pytest.mark.usefixtures('unauthorized_driver')
class TestSuite(ChromeTest):
    def test_case_one(self, driver):
        do_something(self, driver)
        assert "Home" in driver.instance.title, "No Home in title!"

    def test_export_file(self, driver):
        do_something(self, driver)
        time.sleep(5)
        assert os.path.isfile("your_file.docx"), "Your file is not saved!"
        assert os.stat("your_file.docx").st_size != 0, "Your file is empty!"
        delete_newautopay_rules(self, driver)
        os.remove("your_file.docx")
