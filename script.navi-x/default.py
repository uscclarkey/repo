#############################################################################
#
#   Copyright (C) 2013 Navi-X
#
#   This file is part of Navi-X.
#
#   Navi-X is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   Navi-X is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Navi-X.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

#############################################################################
#
# Navi-X bootloader + auto update installer.
#############################################################################
import xbmc, xbmcgui, xbmcaddon
import re, os, time, datetime, traceback
import urllib2
import zipfile
import shutil
import sys
import downloader
import extract

# Script constants
__scriptname__ = "Navi-X"
__author__ = "Navi-X team"
__url__ = "http://code.google.com/p/navi-x/"
__credits__ = "Navi-X team"
__version__ = "3.8.0"

addon = xbmcaddon.Addon(id='script.navi-x')
RootDir = addon.getAddonInfo('path')
sys.path.append(os.path.join(RootDir.replace(";",""),'src'))

if RootDir[-1]==';': RootDir=RootDir[0:-1]
if RootDir[0] == '/':
    if RootDir[-1] != '/': RootDir = RootDir+'/'
    SEPARATOR = '/'    
else:
    if RootDir[-1] != '\\': RootDir=RootDir+'\\'
    SEPARATOR = '\\'

version_default = '0.0.0'
version_URL=''
update_URL=''

##########Install Hub Repo#############################################################
def HUBINSTALL(name,url,description,filetype,repourl):
    try:
        path=xbmc.translatePath(os.path.join('special://home','addons','packages'))
        dp=xbmcgui.DialogProgress()
        dp.create("Checking Structure:","Installing Proper Repo ",'','Only Shown on First Launch')
        lib=os.path.join(path,name+'.zip')
        try: os.remove(lib)
        except: pass
        downloader.download(url, lib, dp)
        if filetype == 'addon':
            addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
        time.sleep(2)
        #dp.update(0,"","Installing selections.....")
        print '======================================='
        print addonfolder
        print '======================================='
        extract.all(lib,addonfolder,'')
        xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
    except: pass

hubpath=xbmc.translatePath(os.path.join('special://home','addons','repository.xbmchub'))
if not os.path.exists(hubpath): HUBINSTALL('xbmchubrepo','https://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/repository.xbmchub/repository.xbmchub-1.0.3.zip','','addon','none')



#############################################################################
def onReadVersion():
    version = version_default
    try:
        f=open(RootDir + 'version.dat', 'r')
        data = f.read()
        data = data.splitlines()
        version=data[0]
        f.close()
    except IOError:
        pass
    
    return version

#############################################################################
def onReadNewVersion(URL):
    version = version_default
    try:
#oldtimeout=socket_getdefaulttimeout()
#socket_setdefaulttimeout(timeout)
            
        f = urllib2.urlopen(URL)

        data = f.read()
        data = data.splitlines()    
        version=data[0]   

    except IOError:
        pass
#socket_setdefaulttimeout(oldtimeout)       
    return version  

#############################################################################
def onSaveVersion(version):
    try:
        f=open(RootDir + 'version.dat', 'w')
        f.write(version + '\n')
        f.close()
    except IOError:
        pass

######################################################################
def installUpdate(URL):
    try:
        #oldtimeout=socket_getdefaulttimeout()
        #socket_setdefaulttimeout(timeout)
            
        f = urllib2.urlopen(URL)

        file = open(RootDir + "update.zip", "wb")
        file.write(f.read())
        file.close()  

    except IOError:
        #socket_setdefaulttimeout(oldtimeout)  
        return -1

    #socket_setdefaulttimeout(oldtimeout)       

    zfobj = zipfile.ZipFile(RootDir + "update.zip")

    for name in zfobj.namelist():
        index = name.rfind('/')
        if index != -1:
            #entry contains path
            if not os.path.exists(RootDir+name[:index+1]):
                try:
                    #create the directory structure
                    os.makedirs(os.path.join(RootDir, name[:index+1]))
                except IOError:
                    return -1 #failure
                    
        if not name.endswith('/'):
            #entry contains a filename
            try:
                outfile = open(os.path.join(RootDir, name), 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()
            except IOError:
                pass #There was a problem. Continue...

    zfobj.close()

    try:
        os.remove(RootDir + "update.zip")
    except IOError:
        pass
        
    return 0 #succesful

######################################################################
def socket_getdefaulttimeout():
    return socket.getdefaulttimeout()

######################################################################
def socket_setdefaulttimeout(url_open_timeout):
    if platform == "xbox":
        socket.setdefaulttimeout(url_open_timeout)

#############################################################################
def Trace(string):
    f = open(RootDir + "trace.txt", "a")
    f.write(string + '\n')
    f.close()

######################################################################  
def get_system_platform():
    platform = "unknown"
    if xbmc.getCondVisibility( "system.platform.linux" ):
        platform = "linux"
    elif xbmc.getCondVisibility( "system.platform.xbox" ):
        platform = "xbox"
    elif xbmc.getCondVisibility( "system.platform.windows" ):
        platform = "windows"
    elif xbmc.getCondVisibility( "system.platform.osx" ):
        platform = "osx"
#    Trace("Platform: %s"%platform)
    return platform

#############################################################################
#############################################################################
#check for updates from the Navi-X website

#retrieve the platform.
platform = get_system_platform()

#read the current version installed
#version = onReadVersion()
#newversion = onReadNewVersion(version_URL)

#if (version != version_default) and (newversion != version_default) and \
#    (version != newversion):
#    installUpdate(update_URL)
#    #save updated version.
#    onSaveVersion(newversion)
#    dialog = xbmcgui.Dialog()
#    dialog.ok("Message", "Navi-X has been updated.")


#############################################################################
#Splash Screen
#############################################################################
def SettingG(setting):
	try: return addon.getSetting(setting)
	except: return ""
def SettingS(setting,value): addon.setSetting(id=setting,value=value)
def gAI(t):
	try: return addon.getAddonInfo(t)
	except: return ""
import splash_highway as splash
mediaFolder=os.path.join(RootDir,'resources','skins','Default','media')
SplashBH=os.path.join(mediaFolder,'default-panel1.png')
ExitBH=os.path.join(mediaFolder,'navi-x3.png')
try: LastVerMessageID=str(SettingG("LastVerMessageID"))
except: LastVerMessageID=""
try: curVerID=str(gAI("version"))
except: curVerID=''
#print [LastVerMessageID,curVerID]
#LastVerMessageID="" ## Used for testing.
if (len(LastVerMessageID)==0) or (not LastVerMessageID==curVerID):
	SettingS("LastVerMessageID",curVerID)
	#SplashTxt="Hello User,\n\n        "
	#SplashTxt+="NAVI-X may now be found for download on the XBMCHUB.COM repository."
	SplashTxt="Navi-X and Team XBMCHUB.com\n\n"
	SplashTxt+="If you're receiving this message it\n"
	SplashTxt+="means that Navi-X has for the first\n"
	SplashTxt+="time updated automatically on your\n"
	SplashTxt+="system and is now located in the\n"
	SplashTxt+="XBMCHUB.com repository!"
	#splash.do_My_TextSplash(SplashTxt,SplashBH,12,TxtColor='0xff00ff00',Font='font14',BorderWidth=70); 
	splash.do_My_TextSplash2(SplashTxt,SplashBH,12,TxtColor='0xff00ff00',Font='font14',BorderWidth=70,ImgexitBtn=ExitBH); 
	
#############################################################################
#Start Navi-X
#############################################################################
import navix
win = navix.MainWindow("skin2.xml", addon.getAddonInfo('path')) #,'Default','720p'
win.doModal()
del win

#xbmc.executescript(RootDir + 'default_.py')

