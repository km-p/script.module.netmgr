__author__ = 'mae'

# -*- coding: utf-8 -*-
import sys

from lib import util, applySettings, selectSettings

if __name__ == '__main__':

    util.DEBUG('Running {}.main.py'.format (util.ADDON_ID))

    arg = None
    if len(sys.argv) > 1:
        arg = sys.argv[1] or False
    extra = sys.argv[2:]

    if arg and arg.startswith('ApplySettings'):
        util.DEBUG("apply network settings")
        applySettings.applyNetworkSettings()
    elif arg and arg.startswith ('ScanWireless'):
        util.DEBUG("scan wireless networks")
        selectSettings.selectWirelessNetworks()
    else:
        util.DEBUG('no args...')

