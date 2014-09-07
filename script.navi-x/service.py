#############################################################################
import xbmc, xbmcgui, xbmcaddon
import re, os, time, datetime, traceback
import urllib2
import zipfile
import shutil
import sys

# Script constants
__scriptname__ = "Navi-X"
__author__ = "Navi-X team"
__url__ = "http://code.google.com/p/navi-x/"
__credits__ = "Navi-X team"
__version__ = "3.8.0"

addon = xbmcaddon.Addon(id='script.navi-x')
RootDir = addon.getAddonInfo('path')
if RootDir[-1]==';': RootDir=RootDir[0:-1]
if RootDir[0] == '/':
    if RootDir[-1] != '/': RootDir = RootDir+'/'
    SEPARATOR = '/'    
else:
    if RootDir[-1] != '\\': RootDir=RootDir+'\\'
    SEPARATOR = '\\'
#############################################################################
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
platform = get_system_platform()
#############################################################################



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
	SplashTxt+="means that Navi-X has, for the first\n"
	SplashTxt+="time, updated automatically on your\n"
	SplashTxt+="system and is now located in the\n"
	SplashTxt+="XBMCHUB.com repository!"
	#splash.do_My_TextSplash(SplashTxt,SplashBH,12,TxtColor='0xff00ff00',Font='font14',BorderWidth=70); 
	splash.do_My_TextSplash2(SplashTxt,SplashBH,12,TxtColor='0xff00ff00',Font='font14',BorderWidth=70,ImgexitBtn=ExitBH); 



#############################################################################
