
import xbmc
import xbmcaddon
import os

ADDON = xbmcaddon.Addon(id='plugin.video.ntv')
IMAGE = os.path.join(ADDON.getAddonInfo('path'), 'icon.jpg')


def notification(message, time = 0):
    message = message.replace('"',  '')
    message = message.replace('\'', '')
    message = message.replace(',',  '')
    message = message.replace('(',  '')
    message = message.replace(')',  '')
 
    if time == 0:
        time = 6

    header = 'NTV.mx'

    cmd  = 'XBMC.Notification(%s, %s, %d, %s)' % (header, message, time*1000, IMAGE)
    print cmd
    xbmc.executebuiltin(cmd)
