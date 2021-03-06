#
# Copyright (c) 2019-2020 Triad National Security, LLC
#                         All rights reserved.
#
# This file is part of the bueno project. See the LICENSE file at the
# top-level directory of this distribution for more information.
#

'''
The build service module.
'''

from typing import (
    List
)

import os
import sys

from bueno.core import service

from bueno.build import builder

from bueno.public import host
from bueno.public import logger
from bueno.public import metadata
from bueno.public import utils


class impl(service.Base):  # pylint: disable=C0103
    '''
    Implements the build service.
    '''
    class _defaults:
        '''
        Convenience container for build service defaults.
        '''
        desc = 'The build service is a front-end to container builders.'
        # The name of the builder back-end.
        builder = 'charliecloud'
        # Path to save any generated files.
        output_path = os.getcwd()

    def __init__(self, argv: List[str]) -> None:
        super().__init__(impl._defaults.desc, argv)

    @property
    def ibuilder(self) -> builder.Base:
        '''
        Returns image builder.
        '''
        return self._ibuilder

    @ibuilder.setter
    def ibuilder(self, bldr: 'builder.Base') -> None:
        '''
        Sets image builder.
        '''
        self._ibuilder = bldr

    def _addargs(self) -> None:
        self.argp.add_argument(
            '-b', '--builder',
            type=str,
            help='Specifies the container builder back-end to use. '
                 'Default: {}'.format(impl._defaults.builder),
            default=impl._defaults.builder,
            choices=builder.Factory.available(),
            required=False
        )

        self.argp.add_argument(
            '-o', '--output-path',
            type=str,
            help='Specifies the output directory used for all generated files. '
                 'Default: {}'.format('PWD'),
            default=impl._defaults.output_path,
            required=False
        )

        self.argp.add_argument(
            '-s', '--spec',
            type=str,
            help='Path to build specification file (e.g., a Dockerfile).',
            required=True
        )

        self.argp.add_argument(
            '-t', '--tag',
            type=str,
            help='Specifies the container name (required).',
            required=True
        )

    def _populate_service_config(self) -> None:
        self.confd['Configuration'] = vars(self.args)

    def _populate_sys_config(self) -> None:
        self.confd['Host'] = {
            'whoami': host.whoami(),
            'kernel': host.kernel(),
            'kernel_release': host.kernelrel(),
            'hostname': host.hostname(),
            'os_release': host.os_pretty_name()
        }

    def _populate_config(self) -> None:
        self._populate_service_config()
        self._populate_sys_config()

    # TODO(skg) Add more configuration info. pylint: disable=W0511
    def _emit_config(self) -> None:
        # First build up the dictionary containing the configuration used.
        self._populate_config()
        # Add to metadata assets stored to container image.
        metadata.add_asset(metadata.YAMLDictAsset(self.confd, 'environment'))
        # Then print it out in YAML format.
        utils.yamlp(self.confd, self.prog)

    def _do_build(self) -> None:
        self.ibuilder = builder.Factory.build(**vars(self.args))
        self.ibuilder.start()

    def start(self) -> None:
        logger.emlog('# Starting {} at {}'.format(self.prog, utils.nows()))
        logger.log('# $ {}\n'.format(' '.join(sys.argv)))

        try:
            stime = utils.now()
            self._emit_config()
            self._do_build()
            etime = utils.now()

            logger.log('# {} Time {}'.format(self.prog, etime - stime))
            logger.log('# {} Done {}'.format(self.prog, utils.nows()))
        except Exception as exception:
            estr = utils.ehorf()
            estr += 'What: {} error encountered.\n' \
                'Why:  {}'.format(self.prog, exception)
            estr += utils.ehorf()
            raise type(exception)(estr)

# vim: ft=python ts=4 sts=4 sw=4 expandtab
