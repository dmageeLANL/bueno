#
# Copyright (c)      2019 Triad National Security, LLC
#                         All rights reserved.
#
# This file is part of the bueno project. See the LICENSE file at the
# top-level directory of this distribution for more information.
#

'''
Utilities for good.
'''

from datetime import datetime


def now():
    '''
    Returns the current date and time.
    '''
    return datetime.now()


def nows():
    '''
    Returns a string representation of the current date and time.
    '''
    return now().strftime('%Y-%m-%d %H:%M:%S')


def chomp(s):
    '''
    Returns a string without trailing newline characters.
    '''
    return s.rstrip()