# -*- coding: utf-8 -*-
# Description: apt python.d module for netdata
# Author: nodiscc (nodiscc@gmail.com)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import apt

from bases.FrameworkServices.SimpleService import SimpleService

priority = 90000
update_every = 120

ORDER = ['upgradable', 'distribution_version']

# CHARTS = {
#     id: {
#         'options': [name, title, units, family, context, charttype],
#         'lines': [
#             [unique_dimension_name, name, algorithm, multiplier, divisor]
#         ]}
CHARTS = {
    'upgradable': {
        'options': [None, 'upgradable packages', 'packages', 'apt', 'apt.upgradable', 'stacked'],
        'lines': [
            ['upgradable', None, 'absolute']
        ]
    },
    'distribution_version': {
        'options': [None, None, None, 'apt', 'apt.distribution_version', 'line'],
        'lines': [
            ['distribution_version', None, 'absolute'],
            ['distribution_version_error', None, 'absolute']
        ]
    }
}

class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.data = dict()
        self.distribution_version_file = '/etc/debian_version'
        self.distribution_version_file_modtime = ''
        self.data['upgradable'] = 0
        self.data['distribution_version_error'] = 0
        self.data['distribution_version'] = 0

    def check(self):
        return self.get_data()

    def get_data(self):
        upgradable_packages_count = 0
        for pkg in apt.Cache():
            if pkg.is_upgradable:
                upgradable_packages_count = upgradable_packages_count + 1
        self.data['upgradable'] = upgradable_packages_count
        if not is_readable(self.distribution_version_file) or is_empty(self.distribution_version_file):
            self.debug("{0} is unreadable or empty".format(self.distribution_version_file))
            self.data['distribution_version_error'] = 1
        if self.distribution_version_file_modtime == os.path.getmtime(self.distribution_version_file):
            self.debug("{0} distribution_version_file modification time unchanged, returning previous values".format(self.distribution_version_file))
            self.data['distribution_version'] = self.data['distribution_version']
        else:
            with open(self.distribution_version_file, 'r') as file:
                self.distribution_version_file_modtime = os.path.getmtime(self.distribution_version_file)
                firstline = file.readline().rstrip()
                try:
                    self.data['distribution_version'] = int(float(firstline))
                except ValueError:
                    # on ubuntu 22 /etc/debian_version only contains "bookworm/sid"
                    # using the same method on debian would have been nice but the lsb_release python module is not provided
                    import lsb_release
                    try:
                        self.data['distribution_version'] = int(float(lsb_release.get_os_release()['RELEASE']))
                    except AttributeError:
                        # ubuntu 18, module 'lsb_release' has no attribute 'get_os_release'
                        self.data['distribution_version'] = int(float(lsb_release.get_distor_information()['RELEASE']))
        return self.data

def is_readable(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)

def is_empty(path):
    return os.path.getsize(path) == 0

