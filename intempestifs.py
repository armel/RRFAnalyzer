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
        options, remainder = getopt.getopt(argv, '', ['help', 'path=', 'month=', 'week=', 'room=', 'order='])
    except getopt.GetoptError:
        l.usage()
        sys.exit(2)
    for opt, arg in options:
        if opt == '--help':
            usage()
            sys.exit()
        elif opt in ('--path'):
            s.search_path = arg
        elif opt in ('--month'):
            s.search_pattern = arg
            s.search_type = 'month'
        elif opt in ('--week'):
            s.search_pattern = arg
            s.search_type = 'week'
        elif opt in ('--room'):
            if arg not in ['RRF', 'TECHNIQUE', 'BAVARDAGE', 'LOCAL', 'INTERNATIONAL', 'FON']:
                print 'Unknown display type (choose between \'RRF\', \'TECHNIQUE\', \'BAVARDAGE\', \'LOCAL\', \'INTERNATIONAL\' and \'FON\')'
                sys.exit()
            s.search_room = arg
        elif opt in ('--order'):
            if arg not in ['BF', 'TX', 'INTEMPESTIF', 'RATIO']:
                print 'Unknown display type (choose between \'BF\', \'TX\', \'INTEMPESTIF\' and \'RATIO\')'
                sys.exit()
            s.search_order = arg


    print l.color.BLUE + 'Path ' + l.color.END + s.search_path,
    print ' with ',
    print l.color.BLUE + 'Pattern ' + l.color.END + s.search_pattern,
    print '...'

    time_super_total = 0

    for r in [s.search_room]:

        s.all.clear()

        if s.search_type == 'month':
            path = s.search_path + r + '-' + s.search_pattern + '-*/rrf.json'
            file = glob.glob(path)
            file.sort()
        else:
            file = []
            start_date = time.asctime(time.strptime(str(datetime.datetime.today().year) + ' %d 1' % int(s.search_pattern), '%Y %W %w'))
            start_date = datetime.datetime.strptime(start_date, '%a %b %d %H:%M:%S %Y')
            file = [search_path + 'RRF-' + start_date.strftime('%Y-%m-%d') + '/rrf.json']
            for i in range(1, 7):
                file.append(s.search_path + 'RRF-' + (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') + '/rrf.json')

        #for f in file:
        #    print f

        time_total = 0

        for f in file:
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

        print tmp

        print '===================='
        print l.color.BLUE + r + ' order by ' + s.search_order + l.color.END
        print '===================='

        i = 1
        for e in tmp:
            check = e[0].split(' ')
            if len(check) == 3:
                print '%03d' % i, '\t',
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

                i += 1

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
