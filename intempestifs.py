#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
RRFAnalyser version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''
from __future__ import division

import settings as s
import lib as l

import os
import glob
import datetime
import time
import sys
import getopt
import json

def main(argv):
    # Check and get arguments
    try:
        options, remainder = getopt.getopt(argv, '', ['help', 'debug=', 'path=', 'year=', 'month=', 'week=', 'day=', 'room=', 'order='])
    except getopt.GetoptError:
        l.usage()
        sys.exit(2)
    for opt, arg in options:
        if opt == '--help':
            usage()
            sys.exit()
        elif opt in ('--path'):
            s.search_path = arg
        elif opt in ('--debug'):
            if arg not in ['True', 'False']:
                print 'Unknown debug mode (choose between \'True\' and \'False\')'
                sys.exit()
            if arg == 'True':
                s.search_debug = True
            else:
                s.search_debug = False
        elif opt in ('--year'):
            s.search_year = arg
        elif opt in ('--month'):
            s.search_month = arg
            s.search_type = 'month'
        elif opt in ('--week'):
            s.search_week = arg
            s.search_type = 'week'
        elif opt in ('--day'):
            s.search_day = arg
            s.search_type = 'day'
        elif opt in ('--room'):
            if arg not in ['ALL', 'RRF', 'TECHNIQUE', 'BAVARDAGE', 'LOCAL', 'INTERNATIONAL', 'FON']:
                print 'Unknown display type (choose between \'ALL\', \'RRF\', \'TECHNIQUE\', \'BAVARDAGE\', \'LOCAL\', \'INTERNATIONAL\' and \'FON\')'
                sys.exit()
            if arg == 'ALL':
                s.search_room = ['RRF', 'TECHNIQUE', 'BAVARDAGE', 'LOCAL', 'INTERNATIONAL']
            else:
                s.search_room = [arg]
        elif opt in ('--order'):
            if arg not in ['BF', 'TX', 'INTEMPESTIF', 'RATIO']:
                print 'Unknown display type (choose between \'BF\', \'TX\', \'INTEMPESTIF\' and \'RATIO\')'
                sys.exit()
            s.search_order = arg

    if s.search_debug is True:
        print l.color.BLUE + 'Path : ' + l.color.END + s.search_path
        print l.color.BLUE + 'Room : ' + l.color.END + ', '.join(s.search_room)
        print l.color.BLUE + 'Search type : ' + l.color.END + s.search_type
        print l.color.BLUE + 'Search year : ' + l.color.END + s.search_year
        if s.search_type == 'month':
            print l.color.BLUE + 'Search month : ' + l.color.END + s.search_month
        elif s.search_type == 'week':
            print l.color.BLUE + 'Search week : ' + l.color.END + s.search_week
        elif s.search_type == 'day':
            print l.color.BLUE + 'Search day : ' + l.color.END + s.search_day
        print '==========='

    time_super_total = 0

    s.all.clear()

    for r in s.search_room:
        file = []

        if s.search_type == 'month':
            s.search_pattern = s.search_year + '-' +  s.search_month
            path = s.search_path + r + '-' + s.search_pattern + '-*/rrf.json'
            file = glob.glob(path)
            file.sort()
        elif s.search_type == 'week':
            s.search_pattern = s.search_week
            start_date = time.asctime(time.strptime(s.search_year + ' %d 1' % int(s.search_pattern), '%Y %W %w'))
            start_date = datetime.datetime.strptime(start_date, '%a %b %d %H:%M:%S %Y')
            file = [s.search_path + 'RRF-' + start_date.strftime('%Y-%m-%d') + '/rrf.json']
            for i in range(1, 7):
                file.append(s.search_path + 'RRF-' + (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') + '/rrf.json')
        else:
            s.search_pattern = int(s.search_day) - 1
            start_date = datetime.datetime.now() - datetime.timedelta(s.search_pattern)
            file = [s.search_path + r + '-' + start_date.strftime('%Y-%m-%d') + '/rrf.json']
            for i in range(1, s.search_pattern + 1):
                file.append(s.search_path + r + '-' + (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') + '/rrf.json')

        time_total = 0

        for f in file:

            if s.search_debug is True:
                print f
            
            if os.path.isfile(f):
                rrf_json = open(f)
                rrf_data = rrf_json.read()
                rrf_data = rrf_data.replace('Extended', '') # Fix old format !
                try:
                    rrf_data = json.loads(rrf_data)

                    for data in rrf_data['all']:
                        try:
                            s.all[data[u'Indicatif'].encode('utf-8')][0] += l.convert_time_to_second(data[u'Durée'])
                            s.all[data[u'Indicatif'].encode('utf-8')][1] += data[u'TX']
                        except:
                            s.all[data[u'Indicatif'].encode('utf-8')] = [l.convert_time_to_second(data[u'Durée']), data[u'TX'], 0, 0]

                    for data in rrf_data['porteuse']:
                        try:
                            s.all[data[u'Indicatif'].encode('utf-8')][2] += data[u'TX']
                            s.all[data[u'Indicatif'].encode('utf-8')][3] = s.all[data[u'Indicatif'].encode('utf-8')][0] / s.all[data[u'Indicatif'].encode('utf-8')][2]
                        except:
                            s.all[data[u'Indicatif'].encode('utf-8')] = [0, 0, data[u'TX'], 0]

                except:
                    pass

    if 'RRF' in s.all:
        del s.all['RRF']
    if 'F5ZIN-L' in s.all:
        del s.all['F5ZIN-L']

    if s.search_order == 'BF':
        tmp = sorted(s.all.items(), key=lambda x: x[1][0])
        tmp.reverse()
    elif s.search_order == 'TX':
        tmp = sorted(s.all.items(), key=lambda x: x[1][1])
        tmp.reverse()
    elif s.search_order == 'INTEMPESTIF':
        tmp = sorted(s.all.items(), key=lambda x: x[1][2])
        tmp.reverse()
    elif s.search_order == 'RATIO':
        tmp = sorted(s.all.items(), key=lambda x: x[1][3])
        tmp.reverse()

    print '===================='
    if len(s.search_room) > 1:
        print l.color.BLUE + 'ALL order by ' + s.search_order + l.color.END
    else:
        print l.color.BLUE + r + ' order by ' + s.search_order + l.color.END
    print '===================='

    if len(tmp) == 0:
        print 'No data !!!'
    else :
        indice = 1
        for e in tmp:
            check = e[0].split(' ')
            if len(check) == 3:
                print '%03d' % indice, '\t',
                print e[0], '\t',
                if len(e[0]) < 7:
                    print '\t',
                if len(e[0]) < 15:
                    print '\t',
                conversion = l.convert_second_to_time(e[1][0])
                print conversion,
                print '\t',
                print e[1][1],
                print '\t',
                print e[1][2],
                print '\t',
                print "% 8.2f" % round(e[1][3], 2)

                indice += 1

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
