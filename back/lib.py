#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
RRFAnalyser version Web
Learn more about RRF on https://f5nlg.wordpress.com
Check video about RRFTracker on https://www.youtube.com/watch?v=rVW8xczVpEo
73 & 88 de F4HWN Armel
'''

# Ansi color
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Usage
def usage():
    print 'Usage: RRFTracker.py [options ...]'
    print
    print '--help               this help'
    print
    print 'Search settings:'
    print '  --debug        debug mode (default=False, choose between [True, False]) '
    print '  --path         set path to RRF files (default=/var/www/RRFTracker/)'
    print '  --room         analyse room (default=RRF, choose between [ALL, RRF, TECHNIQUE, BAVARDAGE, LOCAL, INTERNATIONAL,FON]) '
    print '  --year         analyse on year (default=current year)'
    print '  --month        analyse on month (default=current month)'
    print '  --week         analyse on week'
    print '  --order        analyse room (default=BF, choose between [BF, TX, INTEMPESTIF, RATIO]) '
    print '  --format       analyse room (default=TEXT, choose between [TEXT, JSON]) '
    print
    print '88 & 73 from F4HWN Armel'

# Convert second to time
def convert_second_to_time(time, time_format='{:0>2d}'):
    hours = time // 3600
    time = time - (hours * 3600)

    minutes = time // 60
    seconds = time - (minutes * 60)

    '''
    if hours == 0:
        return str('{:0>2d}'.format(int(minutes))) + 'm ' + str('{:0>2d}'.format(int(seconds))) + 's'
    else:
        return str('{:0>2d}'.format(int(hours))) + 'h ' + str('{:0>2d}'.format(int(minutes))) + 'm ' + str('{:0>2d}'.format(int(seconds))) + 's'
    '''
    return str(time_format.format(int(hours))) + 'h ' + str('{:0>2d}'.format(int(minutes))) + 'm ' + str('{:0>2d}'.format(int(seconds))) + 's'


# Convert time to second
def convert_time_to_second(time):
    time = time.replace('h ', ':')
    time = time.replace('m ', ':')
    time = time.replace('s', '')

    if len(time) > 5:
        format = [3600, 60, 1]
    else:
        format = [60, 1]

    return sum([a * b for a, b in zip(format, map(int, time.split(':')))])
