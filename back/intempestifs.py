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
        options, remainder = getopt.getopt(argv, '', ['help', 'debug=', 'path=', 'year=', 'month=', 'week=', 'day=', 'room=', 'order=', 'format='])
    except getopt.GetoptError:
        l.usage()
        sys.exit(2)
    for opt, arg in options:
        if opt == '--help':
            usage()
            sys.exit()
        elif opt in ('--path'):
            s.analyse_path = arg
        elif opt in ('--debug'):
            if arg not in ['True', 'False']:
                print 'Unknown debug mode (choose between \'True\' and \'False\')'
                sys.exit()
            if arg == 'True':
                s.analyse_debug = True
            else:
                s.analyse_debug = False
        elif opt in ('--year'):
            s.analyse_year = arg
        elif opt in ('--month'):
            s.analyse_month = arg
            s.analyse_type = 'month'
        elif opt in ('--week'):
            s.analyse_week = arg
            s.analyse_type = 'week'
        elif opt in ('--day'):
            s.analyse_day = arg
            s.analyse_type = 'day'
        elif opt in ('--room'):
            if arg not in ['ALL', 'RRF', 'TECHNIQUE', 'BAVARDAGE', 'LOCAL', 'INTERNATIONAL', 'FON']:
                print 'Unknown room name (choose between \'ALL\', \'RRF\', \'TECHNIQUE\', \'BAVARDAGE\', \'LOCAL\', \'INTERNATIONAL\' and \'FON\')'
                sys.exit()
            if arg == 'ALL':
                s.analyse_room = ['RRF', 'TECHNIQUE', 'BAVARDAGE', 'LOCAL', 'INTERNATIONAL']
            else:
                s.analyse_room = [arg]
        elif opt in ('--order'):
            if arg not in ['BF', 'TX', 'INTEMPESTIF', 'RATIO']:
                print 'Unknown order type (choose between \'BF\', \'TX\', \'INTEMPESTIF\' and \'RATIO\')'
                sys.exit()
            s.analyse_order = arg
        elif opt in ('--format'):
            if arg not in ['TEXT', 'JSON']:
                print 'Unknown format type (choose between \'TEXT\' and \'JSON\')'
                sys.exit()
            s.analyse_format = arg

    # Debug trace

    if s.analyse_debug is True:
        print l.color.BLUE + 'Path : ' + l.color.END + s.analyse_path
        print l.color.BLUE + 'Room : ' + l.color.END + ', '.join(s.analyse_room)
        print l.color.BLUE + 'Search type : ' + l.color.END + s.analyse_type
        print l.color.BLUE + 'Search year : ' + l.color.END + s.analyse_year
        if s.analyse_type == 'month':
            print l.color.BLUE + 'Search month : ' + l.color.END + s.analyse_month
        elif s.analyse_type == 'week':
            print l.color.BLUE + 'Search week : ' + l.color.END + s.analyse_week
        elif s.analyse_type == 'day':
            print l.color.BLUE + 'Search day : ' + l.color.END + s.analyse_day
        print l.color.BLUE + 'Search order : ' + l.color.END + s.analyse_order
        print l.color.BLUE + 'Search format : ' + l.color.END + s.analyse_format
        print '==========='

    # Loop

    time_max = 0

    for r in s.analyse_room:
        file = []

        if s.analyse_type == 'month':
            s.analyse_pattern = s.analyse_year + '-' +  s.analyse_month
            path = s.analyse_path + r + '-' + s.analyse_pattern + '-*/rrf.json'
            file = glob.glob(path)
            file.sort()
        elif s.analyse_type == 'week':
            s.analyse_pattern = s.analyse_week
            start_date = time.asctime(time.strptime(s.analyse_year + ' %d 1' % int(s.analyse_pattern), '%Y %W %w'))
            start_date = datetime.datetime.strptime(start_date, '%a %b %d %H:%M:%S %Y')
            file = [s.analyse_path + 'RRF-' + start_date.strftime('%Y-%m-%d') + '/rrf.json']
            for i in range(1, 7):
                file.append(s.analyse_path + 'RRF-' + (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') + '/rrf.json')
        else:
            s.analyse_pattern = int(s.analyse_day) - 1
            start_date = datetime.datetime.now() - datetime.timedelta(s.analyse_pattern)
            file = [s.analyse_path + r + '-' + start_date.strftime('%Y-%m-%d') + '/rrf.json']
            for i in range(1, s.analyse_pattern + 1):
                file.append(s.analyse_path + r + '-' + (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') + '/rrf.json')

        # Surf files

        for f in file:

            # Debug trace
            if s.analyse_debug is True:
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
                            if s.all[data[u'Indicatif'].encode('utf-8')][0] > time_max:
                                time_max = s.all[data[u'Indicatif'].encode('utf-8')][0]
                            s.all[data[u'Indicatif'].encode('utf-8')][1] += data[u'TX']
                        except:
                            s.all[data[u'Indicatif'].encode('utf-8')] = [l.convert_time_to_second(data[u'Durée']), data[u'TX'], 0, 0]

                    for data in rrf_data['porteuse']:
                        try:
                            s.all[data[u'Indicatif'].encode('utf-8')][2] += data[u'TX']
                        except:
                            s.all[data[u'Indicatif'].encode('utf-8')] = [0, 0, data[u'TX'], 0]
                except:
                    pass 

    # Clean artefect

    if 'RRF' in s.all:
        del s.all['RRF']
    if 'F5ZIN-L' in s.all:
        del s.all['F5ZIN-L']

    time_format = '{:0>' + str(len(str(time_max // 3600))) + 'd}'

    # Compute ratio and abstract

    for e in s.all:
        if s.all[e][2] != 0:
            s.all[e][3] = s.all[e][0] / s.all[e][2]
        s.abstract['Links'] += 1
        s.abstract['Durée'] += s.all[e][0]
        s.abstract['TX'] += s.all[e][1]
        s.abstract['Intempestif'] += s.all[e][2]

    # Sort by order 

    if s.analyse_order == 'BF':
        tmp = sorted(s.all.items(), key=lambda x: x[1][0])
        tmp.reverse()
    elif s.analyse_order == 'TX':
        tmp = sorted(s.all.items(), key=lambda x: x[1][1])
        tmp.reverse()
    elif s.analyse_order == 'INTEMPESTIF':
        tmp = sorted(s.all.items(), key=lambda x: x[1][2])
        tmp.reverse()
    elif s.analyse_order == 'RATIO':
        tmp = sorted(s.all.items(), key=lambda x: x[1][3])
        tmp.reverse()

    # Debug trace

    if s.analyse_debug is True:

        print '===================='
        if len(s.analyse_room) > 1:
            print l.color.BLUE + 'ALL order by ' + s.analyse_order + l.color.END
        else:
            print l.color.BLUE + r + ' order by ' + s.analyse_order + l.color.END
        print '===================='

    # Print result by format

    if s.analyse_format == 'TEXT':

        if len(tmp) == 0:
            print 'No data !!!'
        else:
            indice = 1
            for e in tmp:
                check = e[0].split(' ')
                print '%03d' % indice, '\t',
                print e[0], '\t',
                if len(e[0]) < 7:
                    print '\t',
                if len(e[0]) < 15:
                    print '\t',
                conversion = l.convert_second_to_time(e[1][0], time_format)
                print conversion,
                print '\t',
                print e[1][1],
                print '\t',
                print e[1][2],
                print '\t',
                print "% 8.2f" % round(e[1][3], 2)

                indice += 1

    elif s.analyse_format == 'JSON':

        if len(tmp) == 0:
            data = '{}'
        else :
            data = ''
            data += '{\n'
            data += '"abstract":'
            data += '[\n'
            data += '{\n'
            data += '\t"Links": ' + str(s.abstract['Links']) + ',\n'
            data += '\t"Durée": "' +  l.convert_second_to_time(s.abstract['Durée'], time_format) + '",\n'
            data += '\t"TX": ' + str(s.abstract['TX']) + ',\n'
            data += '\t"Intempestif": ' + str(s.abstract['Intempestif']) + '\n'
            data += '}\n'
            data += '],\n'

            data += '"log":'
            data += '[\n'
            indice = 1
            for e in tmp:
                check = e[0].split(' ')
                data += '{\n'
                data += '\t"Pos": ' + str(indice) + ',\n'
                data += '\t"Indicatif": "' + e[0] + '",\n'
                conversion = l.convert_second_to_time(e[1][0], time_format)
                data += '\t"Durée": "' + conversion + '",\n'
                #data += '\t"Durée": ' + str(e[1][0]) + ',\n'
                data += '\t"TX": ' + str(e[1][1]) + ',\n'
                data += '\t"Intempestif": ' + str(e[1][2]) + ',\n'
                if e[1][2] == 0:
                    data += '\t"Ratio": -1\n'
                else:
                    data += '\t"Ratio": ' + str(round(e[1][3], 2)) + '\n'
                data += '},\n'
                indice += 1
            data += ']\n'
            data += '}\n'

        last = data.rfind(',')
        data = data[:last] + '' + data[last + 1:]

        print data

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
