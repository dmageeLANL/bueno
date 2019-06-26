#
# Copyright (c)      2019 Triad National Security, LLC
#                         All rights reserved.
#
# This file is part of the bueno project. See the LICENSE file at the
# top-level directory of this distribution for more information.
#

'''
The good stuff typically called by main().
'''

from bueno.core import service

import sys
import os


class Bueno:
    '''
    Implements the bueno service dispatch system.
    '''

    @staticmethod
    def usage():
        '''
        Emits bueno usage information.
        '''
        # TODO(skg)
        u = 'usage:'
        print()
        print(u)
        print('Services Available:')
        for s in service.ServiceFactory.available():
            print('- {}'.format(s))
        print()
        sys.exit(os.EX_USAGE)

    def check_args(self):
        if self.argc < 2:
            Bueno.usage()

    def __init__(self):
        self.argc = len(sys.argv)
        self.argv = sys.argv

        self.check_args()

        self.service = service.ServiceFactory.build(self.argv[1:])
        self.service.start()


def main():
    try:
        Bueno()
    except ValueError as e:
        print(e)
        Bueno.usage()
        return os.EX_USAGE
    return os.EX_OK