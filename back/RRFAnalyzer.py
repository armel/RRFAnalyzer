#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
RRFAnalyser version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

from dateutil.relativedelta import *

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
                print('Unknown debug mode (choose between \'True\' and \'False\')')
                sys.exit()
            if arg == 'True':
                s.analyse_debug = True
            else:
                s.analyse_debug = False
        elif opt in ('--year'):
            s.analyse_year = arg
        elif opt in ('--month'):
            s.analyse_month = arg
            if int(s.analyse_month) < 0:
                today = datetime.date.today().strftime("%Y-%m-%d")
                today = datetime.datetime.strptime(today, '%Y-%m-%d').date()
                past = today + relativedelta(months=int(s.analyse_month))
                past = str(past).split('-')
                s.analyse_year = str(past[0])
                s.analyse_month = str(past[1]) 
            s.analyse_type = 'month'
        elif opt in ('--week'):
            s.analyse_week = arg
            if s.analyse_week == '0':
                s.analyse_week = str(datetime.date.today().isocalendar()[1] - 1)
            s.analyse_type = 'week'
        elif opt in ('--day'):
            s.analyse_day = arg
            s.analyse_type = 'day'
        elif opt in ('--room'):
            if arg not in ['ALL', 'RRF', 'TECHNIQUE', 'BAVARDAGE', 'LOCAL', 'INTERNATIONAL', 'FON']:
                print('Unknown room name (choose between \'ALL\', \'RRF\', \'TECHNIQUE\', \'BAVARDAGE\', \'LOCAL\', \'INTERNATIONAL\' and \'FON\')')
                sys.exit()
            if arg == 'ALL':
                s.analyse_room = ['RRF', 'TECHNIQUE', 'BAVARDAGE', 'LOCAL', 'INTERNATIONAL']
            else:
                s.analyse_room = [arg]
        elif opt in ('--order'):
            if arg not in ['BF', 'TX', 'INTEMPESTIF', 'RATIO']:
                print('Unknown order type (choose between \'BF\', \'TX\', \'INTEMPESTIF\' and \'RATIO\')')
                sys.exit()
            s.analyse_order = arg
        elif opt in ('--format'):
            if arg not in ['TEXT', 'JSON']:
                print('Unknown format type (choose between \'TEXT\' and \'JSON\')')
                sys.exit()
            s.analyse_format = arg

    # Debug trace

    when = ''
    if s.analyse_type == 'month':
        if s.analyse_month == str(0):
            when = 'depuis le début du mois'
        else:
            when = 'du mois ' + s.analyse_month + '/' + s.analyse_year
    elif s.analyse_type == 'week':
        when = 'depuis le début de la semaine '
    elif s.analyse_type == 'day':
        if s.analyse_day == str(1):
            when = 'aujourd\'hui'
        else:
            when = 'sur les ' + s.analyse_day + ' derniers jours'

    if s.analyse_debug is True:
        print(l.color.BLUE + 'Path : ' + l.color.END + s.analyse_path)
        print(l.color.BLUE + 'Room : ' + l.color.END + ', '.join(s.analyse_room))
        print(l.color.BLUE + 'Search type : ' + l.color.END + s.analyse_type)
        print(l.color.BLUE + 'Search year : ' + l.color.END + s.analyse_year)
        if s.analyse_type == 'month':
            print(l.color.BLUE + 'Search month : ' + l.color.END + s.analyse_month)
        elif s.analyse_type == 'week':
            print(l.color.BLUE + 'Search week : ' + l.color.END + s.analyse_week)
        elif s.analyse_type == 'day':
            print(l.color.BLUE + 'Search day : ' + l.color.END + s.analyse_day)
        print(l.color.BLUE + 'Search order : ' + l.color.END + s.analyse_order)
        print(l.color.BLUE + 'Search format : ' + l.color.END + s.analyse_format)
        print('===========')

    # Loop

    flux = {}

    for r in s.analyse_room:
        time_max = 0
        file = []
        all = {}

        if s.analyse_type == 'month':
            s.analyse_pattern = s.analyse_year + '-' +  s.analyse_month
            path = s.analyse_path + r + '-' + s.analyse_pattern + '-*/rrf.json'
            file = glob.glob(path)
            file.sort()
        elif s.analyse_type == 'week':
            s.analyse_pattern = s.analyse_week
            start_date = time.asctime(time.strptime(s.analyse_year + ' %d 1' % int(s.analyse_pattern), '%Y %W %w'))
            start_date = datetime.datetime.strptime(start_date, '%a %b %d %H:%M:%S %Y')
            file = [s.analyse_path + r + '-' + start_date.strftime('%Y-%m-%d') + '/rrf.json']
            for i in range(1, 7):
                file.append(s.analyse_path + r + '-' + (start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') + '/rrf.json')
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
                print(f)
            
            if os.path.isfile(f):
                rrf_json = open(f)
                rrf_data = rrf_json.read()
                rrf_data = rrf_data.replace('Extended', '') # Fix old format !
                try:
                    rrf_data = json.loads(rrf_data)

                    for data in rrf_data['all']:
                        indicatif = data['Indicatif']
                        check = indicatif.split(' ')
                        if len(check) == 3 or indicatif in ['GW-C4FM', 'RRF']:
                            try:
                                all[indicatif][0] += l.convert_time_to_second(data['Durée'])
                                if all[indicatif][0] > time_max:
                                    time_max = all[indicatif][0]
                                all[indicatif][1] += data['TX']
                            except:
                                all[indicatif] = [l.convert_time_to_second(data['Durée']), data['TX'], 0, 0, 0]

                    for data in rrf_data['porteuse']:
                        indicatif = data['Indicatif']
                        check = indicatif.split(' ')
                        if len(check) == 3 or indicatif in ['GW-C4FM', 'RRF']:
                            try:
                                all[indicatif][2] += data['TX']
                            except:
                                all[indicatif] = [0, 0, data['TX'], 0, 0]
                except:
                    pass 

        # Clean artefect

        #time_format = '{:0>' + str(len(str(time_max // 3600))) + 'd}'
        time_format = '{:0>3d}'

        # Compute ratio and abstract

        abstract = {
            "Salon": '',
            "Links total": 0, 
            "Emission cumulée": 0, 
            "TX total": 0, 
            "TX moyen": 0,
            "Intempestifs total": 0
        }

        for e in all:
            abstract['Links total'] += 1
            abstract['Emission cumulée'] += all[e][0]
            abstract['TX total'] += all[e][1]
            abstract['Intempestifs total'] += all[e][2]
            if all[e][2] != 0:  # Prevent divide by zero...
                all[e][3] = all[e][0] / all[e][2]
            else:
                all[e][3] = -1
            if all[e][1] != 0:  # Prevent divide by zero...
                all[e][4] = all[e][0] / all[e][1]
            else:
                all[e][4] = -1

        abstract['Salon'] = r
        if abstract['TX total'] != 0:
            abstract['TX moyen'] = abstract['Emission cumulée'] / abstract['TX total']
        else:
            abstract['TX moyen'] = 0
        abstract['Emission cumulée'] = l.convert_second_to_time(abstract['Emission cumulée'])

        # Sort by order 

        if s.analyse_order == 'BF':
            tmp = sorted(list(all.items()), key=lambda x: x[1][0])
            tmp.reverse()
        elif s.analyse_order == 'TX':
            tmp = sorted(list(all.items()), key=lambda x: x[1][1])
            tmp.reverse()
        elif s.analyse_order == 'INTEMPESTIF':
            tmp = sorted(list(all.items()), key=lambda x: x[1][2])
            tmp.reverse()
        elif s.analyse_order == 'RATIO':
            tmp = sorted(list(all.items()), key=lambda x: x[1][3])
            tmp.reverse()
        elif s.analyse_order == 'BAVARD':
            tmp = sorted(list(all.items()), key=lambda x: x[1][4])
            tmp.reverse()

        # Compute log

        log = []
        indice = 1
        for e in tmp:
            log.append({'Pos': indice, 'Indicatif': e[0], 'Emission cumulée': l.convert_second_to_time(e[1][0], time_format), 'TX total': e[1][1], 'TX moyen': e[1][4], 'Intempestifs total': e[1][2], 'Ratio': e[1][3]})
            indice += 1

        # Prepare JSON

        flux.update({r: {'abstract': [abstract], 'log': log}})

    # Prepare total

    total = {}
    for r in s.analyse_room:
        for e in flux[r]['log']:
            indicatif = e['Indicatif']
            emission = l.convert_time_to_second(e['Emission cumulée'])
            tx = e['TX total']
            intempestifs = e['Intempestifs total']

            #print r, indicatif, emission, tx, intempestifs

            if indicatif in total:
                total[indicatif][0] += emission
                total[indicatif][1] += tx
                total[indicatif][2] += intempestifs

            else:
                total[indicatif] = [emission, tx, intempestifs, 0, 0]

    # Compute ratio and abstract

    abstract = {
        "Salon": '',
        "Links total": 0, 
        "Emission cumulée": 0, 
        "TX total": 0, 
        "TX moyen": 0,
        "Intempestifs total": 0
    }

    for e in total:
        abstract['Links total'] += 1
        abstract['Emission cumulée'] += total[e][0]
        abstract['TX total'] += total[e][1]
        abstract['Intempestifs total'] += total[e][2]
        if total[e][2] != 0:  # Prevent divide by zero...
            total[e][3] = total[e][0] / total[e][2]
        else:
            total[e][3] = -1
        if total[e][1] != 0:  # Prevent divide by zero...
            total[e][4] = total[e][0] / total[e][1]
        else:
            total[e][4] = -1

    abstract['Salon'] = 'Global'

    flux.update({'Counter': abstract['Emission cumulée']})
    if abstract['TX total'] != 0:
        abstract['TX moyen'] = abstract['Emission cumulée'] / abstract['TX total']
    else:
        abstract['TX moyen'] = 0
    abstract['Emission cumulée'] = l.convert_second_to_time(abstract['Emission cumulée'])

    # Sort by order 

    if s.analyse_order == 'BF':
        tmp = sorted(list(total.items()), key=lambda x: x[1][0])
        tmp.reverse()
    elif s.analyse_order == 'TX':
        tmp = sorted(list(total.items()), key=lambda x: x[1][1])
        tmp.reverse()
    elif s.analyse_order == 'INTEMPESTIF':
        tmp = sorted(list(total.items()), key=lambda x: x[1][2])
        tmp.reverse()
    elif s.analyse_order == 'RATIO':
        tmp = sorted(list(total.items()), key=lambda x: x[1][3])
        tmp.reverse()
    elif s.analyse_order == 'BAVARD':
        tmp = sorted(list(total.items()), key=lambda x: x[1][4])
        tmp.reverse()

    # Compute log

    log = []
    indice = 1
    for e in tmp:
        log.append({'Pos': indice, 'Indicatif': e[0], 'Emission cumulée': l.convert_second_to_time(e[1][0], time_format), 'TX total': e[1][1], 'TX moyen': e[1][4], 'Intempestifs total': e[1][2], 'Ratio': e[1][3]})
        indice += 1


    flux.update({'Global': {'abstract': [abstract], 'log': log}})

    flux.update({'Stat': s.stat_list})
    flux.update({'When': when})

    now = datetime.datetime.now()
    flux.update({'Update': now.strftime('%H:%M')})

    print(json.dumps(flux, sort_keys=True))

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
