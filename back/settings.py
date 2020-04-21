#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
RRFAnalyser version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

import datetime

analyse_debug = False
analyse_path = '/var/www/RRFTracker/'
analyse_year = datetime.datetime.now().strftime('%Y')
analyse_month = datetime.datetime.now().strftime('%m')
analyse_type = 'month'
analyse_room = ['RRF']
analyse_order = 'BF'
analyse_format = 'TEXT'

all = dict()
abstract = {
    "Links": 0, 
    "Durée": 0, 
    "TX": 0, 
    "Intempestif": 0
}