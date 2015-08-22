__author__ = 'mae'

import xbmc, xbmcaddon
import subprocess, binascii

ADDON_ID = "script.module.netmgr"

def LOG (message):
    xbmc.log ('{}: {}'.format(ADDON_ID, message), xbmc.LOGNOTICE)

def DEBUG (message):
    xbmc.log ('{}: {}'.format (ADDON_ID, message), xbmc.LOGDEBUG)

def execShellAndGetOutput (command):
    output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).splitlines()
    return output

def execShell (command):
    output = execShellAndGetOutput(command)
    for l in output:
        DEBUG(l)

def calcNetSize (subnetMask):
    binaryString = ''
    for octet in subnetMask.split('.'):
        binaryString += bin(int(octet))[2:].zfill(8)
    return str(len(binaryString.rstrip('0')))

#

def busyDialog(func):
    def inner(*args,**kwargs):
        try:
            xbmc.executebuiltin("ActivateWindow(10138)")
            func(*args,**kwargs)
        finally:
            xbmc.executebuiltin("Dialog.Close(10138)")
    return inner

def getSetting(key):
    return xbmcaddon.Addon(ADDON_ID).getSetting(key)

def setSetting(key,value):
    value = _processSettingForWrite(value)
    xbmcaddon.Addon(ADDON_ID).setSetting(key,value)

def _processSettingForWrite(value):
    if isinstance(value,list):
        value = binascii.hexlify('\0'.join(value))
    elif isinstance(value,bool):
        value = value and 'true' or 'false'
    return str(value)
