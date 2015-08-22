__author__ = 'mae'

import xbmc, xbmcgui, xbmcaddon
import util

# Select Wireless Networks Dialog
def selectWirelessNetworks ():
    # load wireless networks
    options = []

    try:
        util.execShell("sudo ip link set wlan0 up")
        output = util.execShellAndGetOutput("sudo iwlist wlan0 scan")
        for line in output:
            util.DEBUG('Scanning line: {}'.format(line))
            if line.find("ESSID:") > 0:
                import re
                essid = re.findall(r'.*ESSID:"(.*)"', line)[0]

                util.DEBUG('found essid: {}'.format(essid))
                options.append ((essid, essid))

        # start selectSetting...
        selectSetting ('essid', options)
    except:
        pass


#@util.busyDialog
def selectSetting (settingName, options):

    T = xbmcaddon.Addon(util.ADDON_ID).getLocalizedString

    if not options:
        xbmcgui.Dialog().ok(T(32153),T(32152))
        return

    ids = []
    displays = []
    for ID,display in options:
        ids.append(ID)
        displays.append(display)

    chosenIndex = xbmcgui.Dialog().select(T(32151),displays)

    if chosenIndex < 0: return
    choice = ids[chosenIndex]

    util.DEBUG('Setting {} set to: {}'.format(settingName, choice))
    util.setSetting('{}'.format(settingName),choice)
