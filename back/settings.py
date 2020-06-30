#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
RRFAnalyser version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

from dateutil.relativedelta import *
import datetime

analyse_debug = False
analyse_path = '/var/www/RRFTracker/'
analyse_year = datetime.datetime.now().strftime('%Y')
analyse_month = datetime.datetime.now().strftime('%m')
analyse_type = 'month'
analyse_room = ['RRF']
analyse_order = 'BF'
analyse_format = 'TEXT'

today = datetime.date.today().strftime("%Y-%m-%d")
today = datetime.datetime.strptime(today, '%Y-%m-%d').date()

stat_list = [
    {
        'Autres stats' : 'Aujourd\'hui',
    },
    {
        'Autres stats' : 'Depuis le début de la semaine',
    },
    {
        'Autres stats' : 'Depuis le début du mois',
    }
]

for m in range(1, 11):
    past = today + relativedelta(months=-(m))
    past = str(past).split('-')
    stat_list.append({'Autres stats' : 'Mois ' + past[1] + '/' + past[0]})

stat_list += [
    {
        'Autres stats' : 'Sur les 60 derniers jours',
    },
    {
        'Autres stats' : 'Sur les 120 derniers jours',
    },
    {
        'Autres stats' : 'Sur les 180 derniers jours',
    },
    {
        'Autres stats' : 'Sur les 240 derniers jours',
    },
    {
        'Autres stats' : 'Sur les 300 derniers jours',
    }
]