#coding: utf8

import logging
import requests
import markdown

class HackerNews():
    def __init__(self):
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        self.base_url = "https://api.github.com/repos/headllines/hackernews-daily/issues"

    def get_data(self):
        ret_issues = requests.get(self.base_url, headers=self.headers)

        if ret_issues.status_code != 200:
            logging.error('request %s error, %d', self.base_url, ret_issues.status_code)
            return None
        
        if len(ret_issues.json()) <= 0:
            logging.error('empty result')
            return None
        number = ret_issues.json()[0].get('number')
        
        ret_issue = requests.get('{}/{}'.format(self.base_url, number), headers=self.headers)
        if ret_issue.status_code != 200:
            logging.error('request issue %d error, %d', number, ret_issues.status_code)
            return None

        result = ret_issue.json().get('body')
        return result
        

    def get_html(self):
        prefix = '<H1>HackerNews:</H1><br></br>'
        result = self.get_data()
        if not result:
            return prefix
        
        return prefix + markdown.markdown(result, extensions=['markdown.extensions.tables'])