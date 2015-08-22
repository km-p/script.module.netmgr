__author__ = 'mae'

import util

def applyNetworkSettings ():

    interface = util.getSetting('interface')
    essid = util.getSetting('essid')
    oldEssid = util.getSetting('old_essid')
    psk = util.getSetting('psk')
    encryption = util.getSetting('encryption')
    useDHCP = util.getSetting('dhcp')
    ipAddress = util.getSetting('ipaddress')
    subnetMask = util.getSetting('subnet')
    gateway = util.getSetting('gateway')

    util.DEBUG('interface={}, essid={}, encryption={}, psk={}, dhcp={}, ipaddress={}, subnetmask={}, gateway={}'.format (interface, essid, encryption, psk, useDHCP, ipAddress, subnetMask, gateway))
    util.DEBUG('old_essid={}, psk_backup={}'.format(oldEssid, util.getSetting('psk_backup')))

    localTempPath = '/tmp/'

    # 0 .. eth0
    # 1 .. wlan0

    interfaceName = ''
    if interface == '0':
        interfaceName = 'eth0'

        networkConfigPath = '/etc/systemd/network/'
        backupConfigPathFilename = '{}_backup_-{}._etwor_.backup'.format (networkConfigPath, interfaceName)
        configFilename = '{}.network'.format (interfaceName)
        localConfigPathFilename = '{}{}'.format (localTempPath, configFilename)
        networkConfigPathFilename = '{}{}'.format (networkConfigPath, configFilename)

        # create new config file...
        file = open (localConfigPathFilename, 'w')
        file.write ('[Match]\n')
        file.write ('Name={}\n'.format(interfaceName))
        file.write ('\n')
        file.write ('[Network]\n')

        # if DHCP -> start dhcp
        # else set fixed route
        if useDHCP.lower() == 'true':
            file.write ('DHCP=both\n')
        else:
            file.write ('DNS={}\n'.format(gateway))
            file.write ('Address={}/{}\n'.format(ipAddress, util.calcNetSize(subnetMask)))
            file.write ('Gateway={}\n'.format(gateway))
            pass

        file.write('\n')
        file.close()

        # backup and replace config file...
        try:
            util.execShell('sudo rm {}'.format (backupConfigPathFilename))
        except:
            util.DEBUG("removing of {} failed...".format(backupConfigPathFilename))

        try:
            util.execShell('sudo mv -v {} {}'.format (networkConfigPathFilename, backupConfigPathFilename))
        except:
            util.DEBUG("backing {} up to {} failed...".format(networkConfigPathFilename, backupConfigPathFilename))

        util.execShell('sudo mv -v {} {}'.format (localConfigPathFilename, networkConfigPathFilename))
        util.execShell('sudo chown -v root:root {}'.format (networkConfigPathFilename))

    else:
        interfaceName = 'wlan0'

        networkConfigPath = '/etc/netctl/'
        backupConfigPathFilename = '{}_backup_-{}-{}._backup'.format (networkConfigPath, interfaceName, essid)
        configFilename = '{}-{}'.format (interfaceName, essid)
        if oldEssid == "":
            oldConfigFilename = ''
        else:
            oldConfigFilename = '{}-{}'.format (interfaceName, oldEssid)
        localConfigPathFilename = '{}{}'.format (localTempPath, configFilename)
        networkConfigPathFilename = '{}{}'.format (networkConfigPath, configFilename)

        # create new config file...
        file = open (localConfigPathFilename, 'w')

        file.write ("Description='Created by script.module.netmgr'\n")
        file.write ("Interface={}\n".format(interfaceName))
        file.write ("Connection=wireless\n")

        security = 'none'
        if encryption == '1':
            security = 'wep'
        elif encryption == '2':
            security = 'wpa'
        file.write ("Security={}\n".format(security))
        file.write ("ESSID={}\n".format (essid))

        ip = 'dhcp'
        if useDHCP == 'false':
            ip = 'static'

        file.write ("IP={}\n".format(ip))

        if useDHCP == 'false':
            file.write("Address='{}/{}'\n".format(ipAddress, util.calcNetSize(subnetMask)))
            file.write("Gateway='{}'\n".format(gateway))
            file.write("DNS=('{}')\n".format(gateway))

        if encryption != '0':
            file.write ("Key={}\n".format(psk))

        file.write('\n')
        file.close()

        # Disable profile (just in case...)
        try:
            util.execShell('sudo systemctl reset-failed')
        except:
            util.DEBUG("call 'systemctl reset-failed' failed...".format(configFilename))

        try:
            util.execShell('sudo netctl disable {}'.format (configFilename))
        except:
            util.DEBUG("disabling of netctl {} failed...".format(configFilename))

        try:
            util.execShell('sudo netctl disable {}'.format (oldConfigFilename))
        except:
            util.DEBUG("disabling of netctl {} failed...".format(oldConfigFilename))

        # backup and replace config file...
        try:
            util.execShell('sudo rm {}'.format (backupConfigPathFilename))
        except:
            util.DEBUG("removing of {} failed...".format(backupConfigPathFilename))

        try:
            util.execShell('sudo mv -v {} {}'.format (networkConfigPathFilename, backupConfigPathFilename))
        except:
            util.DEBUG("backing {} up to {} failed...".format(networkConfigPathFilename, backupConfigPathFilename))

        util.execShell('sudo mv -v {} {}'.format (localConfigPathFilename, networkConfigPathFilename))
        util.execShell('sudo chown -v root:root {}'.format (networkConfigPathFilename))
        util.execShell('sudo chmod -v 600 {}'.format (networkConfigPathFilename))

        # util.execShell('sudo netctl start {}'.format (configFilename))
        util.execShell('sudo netctl enable {}'.format (configFilename))

        # save essid als old_essid
        util.setSetting('old_essid', essid)

    # save password
    util.setSetting("psk_backup", util.getSetting("psk"))
    # remove password from storage...
    util.setSetting("psk", "")

    # reboot the system
    util.execShell('sudo reboot')

    # restart systemd-networkd
    #util.execShell('sudo systemctl stop systemd-networkd')
    #util.execShell('sudo systemctl start systemd-networkd')
