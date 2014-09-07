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
import xbmc,sys,os,xbmcaddon,xbmcplugin,urllib2,urllib
def SettingG(setting):
	try: return addon.getSetting(setting)
	except: return ""
def SettingS(setting,value): addon.setSetting(id=setting,value=value)
def gAI(t):
	try: return addon.getAddonInfo(t)
	except: return ""
def tfalse(r,d=False): ## Get True / False
	if   (r.lower()=='true' ) or (r.lower()=='t') or (r.lower()=='y') or (r.lower()=='1') or (r.lower()=='yes'): return True
	elif (r.lower()=='false') or (r.lower()=='f') or (r.lower()=='n') or (r.lower()=='0') or (r.lower()=='no'): return False
	else: return d
def UrlDoGet(url):
  import urllib2
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link
def FileDoSave(path,data):
    file=open(path,'w')
    file.write(data)
    file.close()
def FileDoOpen(path):
    if os.path.isfile(path): ## File found.
        file=open(path, 'r')
        contents=file.read()
        file.close()
        return contents
    else: return '' ## File not found.


#############################################################################

ACTION_MOVE_LEFT       =  1 #Dpad Left
ACTION_MOVE_RIGHT      =  2 #Dpad Right
ACTION_MOVE_UP         =  3 #Dpad Up
ACTION_MOVE_DOWN       =  4 #Dpad Down
ACTION_PAGE_UP         =  5 #Left trigger
ACTION_PAGE_DOWN       =  6 #Right trigger
ACTION_SELECT_ITEM     =  7 #'A'
ACTION_HIGHLIGHT_ITEM  =  8
ACTION_PARENT_DIR      =  9 #'B'
ACTION_PREVIOUS_MENU   = 10 #'Back'
ACTION_SHOW_INFO       = 11
ACTION_PAUSE           = 12
ACTION_STOP            = 13 #'Start'
ACTION_NEXT_ITEM       = 14
ACTION_PREV_ITEM       = 15
ACTION_XBUTTON	       = 18 #'X'
ACTION_YBUTTON 	       = 34	#'Y'
ACTION_MOUSEMOVE       = 90 # Mouse has moved
ACTION_MOUSEMOVE2      = 107 # Mouse has moved
ACTION_PREVIOUS_MENU2  = 92 #'Back'
ACTION_CONTEXT_MENU    = 117 # pops up the context menu
ACTION_CONTEXT_MENU2   = 229 # pops up the context menu (remote control "title" button)


#############################################################################
# auto scaling values
#############################################################################

HDTV_1080i = 0      #(1920x1080, 16:9, pixels are 1:1)
HDTV_720p = 1       #(1280x720, 16:9, pixels are 1:1)
HDTV_480p_4x3 = 2   #(720x480, 4:3, pixels are 4320:4739)
HDTV_480p_16x9 = 3  #(720x480, 16:9, pixels are 5760:4739)
NTSC_4x3 = 4        #(720x480, 4:3, pixels are 4320:4739)
NTSC_16x9 = 5       #(720x480, 16:9, pixels are 5760:4739)
PAL_4x3 = 6         #(720x576, 4:3, pixels are 128:117)
PAL_16x9 = 7        #(720x576, 16:9, pixels are 512:351)
PAL60_4x3 = 8       #(720x480, 4:3, pixels are 4320:4739)
PAL60_16x9 = 9      #(720x480, 16:9, pixels are 5760:4739)


#############################################################################
# directory settings
#############################################################################
import os, xbmcaddon

addon = xbmcaddon.Addon(id='script.navi-x')
RootDir = addon.getAddonInfo('path')
datapaths = xbmc.translatePath(addon.getAddonInfo('profile'))

if RootDir[-1]==';': RootDir=RootDir[0:-1]
if RootDir[0] == '/':
    if RootDir[-1] != '/': RootDir = RootDir+'/'
    myDownloadsDir = RootDir + "My Downloads/"
    myDownloadsDir=xbmc.translatePath(os.path.join(datapaths,'My Downloads'))+"/"
    if os.path.exists(myDownloadsDir)==False:
        try: os.makedirs(myDownloadsDir)
        except: 
        	myDownloadsDir = RootDir + "My Downloads/"
        	#pass
    initDir = RootDir + "init/"
    myPlaylistsDir = RootDir + "My Playlists/"
    myPlaylistsDirB = RootDir + "My Playlists/"
    myPlaylistsDir=xbmc.translatePath(os.path.join(datapaths,'My Playlists'))
    if os.path.exists(myPlaylistsDir)==False:
        try: os.makedirs(myPlaylistsDir)
        except: 
        	myPlaylistsDir = RootDir + "My Playlists/"
        	#pass
    srcDir = RootDir + "src/"
    #imageDir = RootDir + "images/"
    imageDir = RootDir + "resources/skins/Default/media/"
    cacheDir = RootDir + "cache/"
    imageViewCacheDir = RootDir + "cache/mageview/"
    imageCacheDir = RootDir + "cache/images/"
    tempCacheDir = RootDir + "cache/temp/"
    nookieCacheDir = RootDir + "cache/nookies/"
    procCacheDir = RootDir + "cache/proc/"
    favoritesDir = RootDir + "favorites/"
    favoritesDir=xbmc.translatePath(os.path.join(datapaths,'favorites'))
    if os.path.exists(favoritesDir)==False:
        try: os.makedirs(favoritesDir)
        except: 
        	favoritesDir = RootDir + "favorites/"
        	#pass
    SEPARATOR = '/'
else:
    if RootDir[-1] != '\\': RootDir = RootDir+'\\'
    myDownloadsDir = RootDir + "My Downloads\\"
    myDownloadsDir=xbmc.translatePath(os.path.join(datapaths,'My Downloads'))+"\\"
    if os.path.exists(myDownloadsDir)==False:
        try: os.makedirs(myDownloadsDir)
        except: 
        	myDownloadsDir = RootDir + "My Downloads\\"
        	#pass
    initDir = RootDir + "init\\"
    myPlaylistsDir = RootDir + "My Playlists\\"
    myPlaylistsDirB = RootDir + "My Playlists\\"
    myPlaylistsDir=xbmc.translatePath(os.path.join(datapaths,'My Playlists'))
    if os.path.exists(myPlaylistsDir)==False:
        try: os.makedirs(myPlaylistsDir)
        except: 
        	myPlaylistsDir = RootDir + "My Playlists\\"
        	#pass
    srcDir = RootDir + "src\\"
    #imageDir = RootDir + "images\\"
    imageDir = RootDir + "resources\\skins\\Default\\media\\"
    cacheDir = RootDir + "cache\\"
    imageViewCacheDir = RootDir + "cache\\imageview\\"
    imageCacheDir = RootDir + "cache\\images\\"
    tempCacheDir = RootDir + "cache\\temp\\"
    nookieCacheDir = RootDir + "cache\\nookies\\"
    procCacheDir = RootDir + "cache\\proc\\"
    favoritesDir = RootDir + "favorites\\"
    favoritesDir=xbmc.translatePath(os.path.join(datapaths,'favorites'))
    if os.path.exists(favoritesDir)==False:
        try: os.makedirs(favoritesDir)
        except: 
        	favoritesDir = RootDir + "favorites\\"
        	#pass
    SEPARATOR = '\\'

import xbmc
#version = xbmc.getInfoLabel("System.BuildVersion")[:1]
try:
  The1stTwo=xbmc.getInfoLabel("System.BuildVersion")[:2]
  #if xbmc.getInfoLabel("System.BuildVersion")[:2] == '10':
  if The1stTwo == '10':
    scriptDir = "special://home/addons/"
    pluginDir = "special://home/addons/"
    skinDir = "special://home/skin/"
  elif xbmc.getInfoLabel("System.BuildVersion")[:1] == '9':
    scriptDir = "special://home/scripts/"
    pluginDir = "special://home/plugins/"
    skinDir = "special://home/skin/"
  elif int(The1stTwo) > 10:
    scriptDir = "special://home/addons/"
    pluginDir = "special://home/addons/"
    skinDir = "special://home/skin/"
  else: 
    scriptDir = "Q:\\scripts\\"
    pluginDir = "Q:\\plugins\\"
    skinDir = "Q:\\skin\\"
except:
    scriptDir = "Q:\\scripts\\"
    pluginDir = "Q:\\plugins\\"
    skinDir = "Q:\\skin\\"

useLibrtmp=os.path.exists(xbmc.translatePath('special://xbmc/system/players/dvdplayer/librtmp.dll'))

######################################################################
#program version: Combination of version and subversion
Version='3' 
SubVersion='8.2'
try:
  Version=addon.getAddonInfo('version').split('.')[0]
  SubVersion=addon.getAddonInfo('version')[len(Version)+1:]
  if ' ' in SubVersion: SubVersion=SubVersion.split(' ')[0]
except: pass
favorite_file='favorites.plx' #the favorite list is also a playlist
downloads_file='downlmenu.plx' #the downloads list is also a playlist
downloads_queue='downlqueue.plx'
downloads_complete='downloads.plx'
parent_list='blacklist.plx'
history_list='history.plx'
plxVersion = '8'
#home_URL_old='http://navi-x.googlecode.com/svn/trunk/Playlists/home.plx'
home_URL_old='http://navi-x.googlecode.com/svn/trunk/Playlists/home2.plx'
#home_URL='http://navi-x.googlecode.com/svn/trunk/Playlists/home2.plx'
#home_URL='http://raw.github.com/HIGHWAY99/navi-x-storage-unit/master/Playlists/home2.plx'
home_URL='http://offshoregit.com/navixtreme/navi-x-support-files/raw/master/Playlists/home2.plx'
home_URL_offshore='http://offshoregit.com/navixtreme/navi-x-support-files/raw/master/Playlists/home2.plx'
home_URL_github='http://raw.github.com/HIGHWAY99/navi-x-storage-unit/master/Playlists/home2.plx'
home_URL_googlecode='http://navi-x.googlecode.com/svn/trunk/Playlists/home2.plx'
core_homepage=SettingG("core-homepage").lower()
if   core_homepage=="default":      pass
elif core_homepage=="offshore":     home_URL=home_URL_offshore
elif core_homepage=="github":       home_URL=home_URL_github
elif core_homepage=="googlecode":   home_URL=home_URL_googlecode

home_URL_mirror='http://navi-x.googlecode.com/svn/trunk/Playlists/home2.plx'
#home_URL_mirror='http://raw.github.com/HIGHWAY99/navi-x-storage-unit/master/Playlists/home2.plx'
background_image1 = 'background1.jpg'
background_image2 = 'background2.png'
searchhistory_file = 'search.dat'
nxserver_URL = 'http://www.navixtreme.com'

url_open_timeout = 60 #60 seconds
page_size = 200 #display maximum 200 entries on one page
history_size = 50 #maximum of entries in the history list

user_agent_default = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4';

#############################################################################

mediaFolder=os.path.join(RootDir,'resources','skins','Default','media')
SplashBH=os.path.join(mediaFolder,'default-panel1.png')
ExitBH=os.path.join(mediaFolder,'navi-x3.png')

#############################################################################
