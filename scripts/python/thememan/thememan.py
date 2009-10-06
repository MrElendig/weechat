#!/usr/bin/python 
# -*- coding: utf-8 -*-

""" A script to add and themes to weechat
    Copyright (C) 2009  Øyvind Heggstad

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import weechat
import ConfigParser
import os.path

weechat.register('thememan',
        'Øyvind Heggstad',
        '0.0.1',
        'AGPLv3',
        'A simple theme manager',
        '',
        '')

weechat.hook_command('theme',
        'loads and saves themes',
        '[load theme] | [save theme]',
        '',
        'load %(filename)'
        '|| save %(filename)',
        'theme_cb',
        '')
def print_error(buffer, text):
    weechat.prnt(buffer, '{0}{1}'.format(weechat.prefix('error'), text))

def config_set(option, value):
    option = weechat.config_get(option)
    if option:
        weechat.config_option_set(option, value, 1)

def load_theme(theme):
    tc = ConfigParser.SafeConfigParser()
    weechat.prnt('', os.path.abspath(theme))
    try:
        fd = open(os.path.expanduser(theme), 'r')
        tc.readfp(fd)
        fd.close()
    except IOError as (errno, strerror):
        print_error('', 'Error loading themefile "{0}"'.format(os.path.expanduser(theme)))
        print_error('', 'I/O error({0}): {1}'.format(errno, strerror))
    except ConfigParser.ParsingError:
        print_error('', 'Could not parse themefile "{0}", check the syntax?'.format(os.path.expanduser(theme)))

    for s in tc.sections():
        for k, v in tc.items(s):
            tmp = config_set(k, v)

def theme_cb(data, buffer, argv):
    weechat.prnt('', weechat.info_get('weechat_dir', ''))
    argv = argv.split()
    argc = len(argv)
    if not argc:
        print_error('', 'Error: Must have an argument')
        return weechat.WEECHAT_RC_OK
    elif argc > 2:
        print_error('', 'Error: Too many arguments')
        return weechat.WEECHAT_RC_OK
    elif argc == 2 and argv[0] == 'load':
        load_theme(argv[1])
    elif argc == 2 and argv[0] == 'save':
        pass
    return weechat.WEECHAT_RC_OK
    

