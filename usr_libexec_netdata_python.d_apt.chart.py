# -*- coding: utf-8 -*-
# Description: apt python.d module for netdata
# Author: nodiscc (nodiscc@gmail.com)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re

from bases.FrameworkServices.SimpleService import SimpleService

priority = 90000
update_every = 120

ORDER = ['upgradeable', 'distribution_version']

# CHARTS = {
#     id: {
#         'options': [name, title, units, family, context, charttype],
#         'lines': [
#             [unique_dimension_name, name, algorithm, multiplier, divisor]
#         ]}
CHARTS = {
    'upgradeable': {
        'options': [None, 'Upgradeable packages', 'packages', 'apt', 'apt.upgradeable', 'stacked'],
        'lines': [
            ['packages', None, 'absolute'],
            ['upgradeable_packages_error', None, 'stacked'],
        ]
    },
    'distribution_version': {
        'options': [None, 'Distribution version', None, 'apt', 'apt.distribution_version', 'line'],
        'lines': [
            ['version', None, 'absolute'],
            ['distribution_version_error', None, 'stacked'],
        ]
    },
}

class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.upgradeable_count_file = '/var/log/netdata/netdata-apt.log'
        self.distribution_version_file = '/etc/debian_version'
        self.distribution_version_file_modtime = ''
        self.upgradeable_count_file_modtime = ''
        ############ TODO #############
        ######### https://github.com/netdata/netdata/blob/master/collectors/python.d.plugin/openldap/openldap.chart.py

    def check(self):
        return self.get_data()

    def get_data(self):
        self.data = dict()
        self.data['upgradeable_packages_error'] = 0
        self.data['distribution_version_error'] = 0
        if not is_readable(self.upgradeable_count_file) or is_empty(self.upgradeable_count_file):
            self.debug("{0} is unreadable or empty".format(self.upgradeable_count_file))
            self.data['upgradeable_packages_error'] = 1
        if not is_readable(self.distribution_version_file) or is_empty(self.distribution_version_file):
            self.debug("{0} is unreadable or empty".format(self.distribution_version_file))
            self.data['distribution_version_error'] = 1

        if self.upgradeable_count_file_modtime == os.path.getmtime(self.upgradeable_count_file):
            self.debug("{0} upgradeable_count_file modification time unchanged, returning previous values".format(self.upgradeable_count_file))
            return self.data
        else:
            with open(self.upgradeable_count_file, 'r') as file:
                self.upgradeable_count_file_modtime = os.path.getmtime(self.upgradeable_count_file)
                firstline = file.readline().rstrip()
                self.data['upgradeable'] = firstline
            print('DEBUG ' + str(self.data))

        if self.distribution_version_file_modtime == os.path.getmtime(self.distribution_version_file):
            self.debug("{0} distribution_version_file modification time unchanged, returning previous values".format(self.distribution_version_file))
        else:
            with open(self.distribution_version_file, 'r') as file:
                self.distribution_version_file_modtime = os.path.getmtime(self.distribution_version_file)
                firstline = file.readline().rstrip()
                self.data['distribution_version'] = firstline
            print('DEBUG ' + str(self.data))

        return self.data

def is_readable(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)

def is_empty(path):
    return os.path.getsize(path) == 0

