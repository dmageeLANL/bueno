#
# Copyright (c)      2019 Triad National Security, LLC
#                         All rights reserved.
#
# This file is part of the bueno project. See the LICENSE file at the
# top-level directory of this distribution for more information.
#

'''
The build service module.
'''

from bueno.core import service


class impl(service.Service):
    '''
    Implements the build service.
    '''
    def __init__(self, argv):
        super().__init__(argv)

    def _addargs(self):
        self.argp.add_argument(
            '--test',
            action='store_true',
            help='Test help.',
            required=True
        )

    def start(self):
        print(self.args)
