#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
RRFAnalyser version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

import datetime

search_path = '/var/www/RRFTracker/'
search_pattern = datetime.datetime.now().strftime('%Y-%m')
search_type = 'month'
search_room = 'RRF'
search_order = 'BF'

all = dict()