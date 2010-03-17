# -*- coding: utf-8 -*-
""" A simple script to see who a (host)mask will effect
    Usage: /tmask foo!bar@baz .  * and ? should work as expected

    ---------------------------------------------------------------------
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
    ---------------------------------------------------------------------
"""
import weechat
import re

SNAME = 'tmask'
SVERSION = '0.1'

weechat.register('tmask', '', '0.1', 'AGPL3', '', '', '')
weechat.hook_command('tmask', '', '', '', '', 'main', '')

def main(data, buffer, args):
    if not args:
        weechat.prnt(buffer, 'Error: No mask specified.')
        return weechat.WEECHAT_RC_OK
    elif len(args.split()) > 1:
        weechat.prnt(buffer, 'Error: Sorry, only one mask at a time.')
        return weechat.WEECHAT_RC_OK
    elif not re.match(r'\S*!\S*@\S', args):
        weechat.prnt(buffer, 'Error: Not a valid mask.')
        return weechat.WEECHAT_RC_OK

    mask = args.replace('?', '.?')
    mask = mask.replace('*', '.*')
    mask = re.compile(mask, re.I)

    channel = weechat.buffer_get_string(buffer, 'localvar_channel')
    server = weechat.buffer_get_string(buffer, 'localvar_server')
    
    results = []
    infolist = weechat.infolist_get('irc_nick', '', '{0},{1}'.format(server, channel))
    while weechat.infolist_next(infolist):
        name = weechat.infolist_string(infolist, 'name')
        host = weechat.infolist_string(infolist, 'host')
        n = '{0}!{1}'.format(name, host)
        if mask.match(n):
            results.append('{0} ({1})'.format(name, n))

    weechat.infolist_free(infolist)

    if results:
        weechat.prnt(buffer, 'Found {0} Matches for: {1}'.format(len(results), args))
        for i in results:
            weechat.prnt(buffer, i)
    else:
        weechat.prnt(buffer, 'No match for: {0}'.format(args))

    return weechat.WEECHAT_RC_OK
