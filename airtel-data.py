#! /usr/bin/env python
#
# Script to display Airtel Broadband usage statistics
#
# @author: Sreejith K <sreejithemk@gmail.com>
# Created On Jan 21 2013


import sys
import urllib2
from HTMLParser import HTMLParser


USAGE_URL = 'http://122.160.230.125:8080/gbod/'


class AirtelDataUsageParser(HTMLParser):
    """Parses the Data usage from the SmartBytes HTML page.
    """
    def __init__(self):
        self._inbody = False
        self._data_ready = False
        self._usage_info_ready = False
        self._usage_info = []
        HTMLParser.__init__(self)
        self.get_page_info()

    def get_page_info(self):
        """Get the HTML data.
        """
        try:
            response = urllib2.urlopen(USAGE_URL)
        except urllib2.URLError:
            print 'Could not connect to Airtel SmartBytes page'
            sys.exit(-1)

        data = response.read()
        self.feed(data)

    def print_usage_stats(self):
        """Print the data usage statistics.
        """
        try:
            dsl_number = self._usage_info[:2]
            balance_quota = self._usage_info[2:5]
            high_speed_limit = self._usage_info[5:8]
            days_left = self._usage_info[8:10]
        except IndexError:
            print 'Airtel SmartBytes page format changed. ' +\
                  'Could not find the useful information'
            sys.exit(-2)

        print ' '.join(dsl_number)
        print ' '.join(balance_quota)
        print ' '.join(high_speed_limit)
        print ' '.join(days_left)

    def handle_starttag(self, tag, attrs):
        if self._data_ready and tag == 'li':
            self._usage_info_ready = True
        elif self._inbody and tag == 'div'\
                          and attrs == [('class', 'content-data')]:
            self._data_ready = True
        elif tag == 'body':
            self._inbody = True

    def handle_endtag(self, tag):
        if self._data_ready and tag == 'div':
            self._data_ready = False
        if self._usage_info_ready and tag == 'ul':
            self._usage_info_ready = False

    def handle_data(self, data):
        if self._usage_info_ready and not data.isspace():
            self._usage_info.append(data)


def print_usage_stats():
    try:
        parser = AirtelDataUsageParser()
        parser.print_usage_stats()
    except KeyboardInterrupt:
        print 'Exiting...'


if __name__ == '__main__':
    print_usage_stats()
