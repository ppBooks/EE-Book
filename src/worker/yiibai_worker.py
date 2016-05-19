#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup

from src.tools.http import Http
from src.tools.match import Match
from src.worker.page_worker import PageWorker

from src.lib.parser_tools import ParserTools
from src.lib.yiibai_parser.yiibai import YiibaiParser


class YiibaiWorker(PageWorker):
    u"""
    Yiibai author worker
    """

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        content = Http.get_content(target_url)
        if not content:
            return
        self.info_url_complete_set.add(target_url)
        parser = YiibaiParser(content)
        self.info_list.append(parser.get_extra_info())
        print u"self.info_list???" + str(self.info_list)
        return

    def create_save_config(self):
        config = {
            'generic_article': self.answer_list,
            'generic_info': self.info_list
        }
        return config

    def parse_content(self, content):
        parser = YiibaiParser(content)
        self.answer_list += parser.get_answer_list()

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return

        content = Http.get_content(target_url)
        article_list = YiibaiParser(content).get_article_list()

        self.task_complete_set.add(target_url)
        for item in article_list:
            self.work_set.add(item)
        return
