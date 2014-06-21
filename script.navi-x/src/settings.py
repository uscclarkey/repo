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

if RootDir[-1]==';': RootDir=RootDir[0:-1]
if RootDir[0] == '/':
    if RootDir[-1] != '/': RootDir = RootDir+'/'
    myDownloadsDir = RootDir + "My Downloads/"
    initDir = RootDir + "init/"
    myPlaylistsDir = RootDir + "My Playlists/"
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
    SEPARATOR = '/'
else:
    if RootDir[-1] != '\\': RootDir = RootDir+'\\'
    myDownloadsDir = RootDir + "My Downloads\\"
    initDir = RootDir + "init\\"
    myPlaylistsDir = RootDir + "My Playlists\\"
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
    SEPARATOR = '\\'

import xbmc
#version = xbmc.getInfoLabel("System.BuildVersion")[:1]
if xbmc.getInfoLabel("System.BuildVersion")[:2] == '10':
    scriptDir = "special://home/addons/"
    pluginDir = "special://home/addons/"
    skinDir = "special://home/skin/"
elif xbmc.getInfoLabel("System.BuildVersion")[:1] == '9':
    scriptDir = "special://home/scripts/"
    pluginDir = "special://home/plugins/"
    skinDir = "special://home/skin/"
else: 
    scriptDir = "Q:\\scripts\\"
    pluginDir = "Q:\\plugins\\"
    skinDir = "Q:\\skin\\"


useLibrtmp=os.path.exists(xbmc.translatePath('special://xbmc/system/players/dvdplayer/librtmp.dll'))

######################################################################
#program version: Combination of version and subversion
Version='3' 
SubVersion='7.8'

favorite_file='favorites.plx' #the favorite list is also a playlist
downloads_file='downlmenu.plx' #the downloads list is also a playlist
downloads_queue='downlqueue.plx'
downloads_complete='downloads.plx'
parent_list='blacklist.plx'
history_list='history.plx'
plxVersion = '8'
home_URL_old='http://navi-x.googlecode.com/svn/trunk/Playlists/home.plx'
home_URL='http://navi-x.googlecode.com/svn/trunk/Playlists/home2.plx'
home_URL_mirror='http://navi-x.googlecode.com/svn/trunk/Playlists/home2.plx'
background_image1 = 'background1.jpg'
background_image2 = 'background2.png'
searchhistory_file = 'search.dat'
nxserver_URL = 'http://www.navixtreme.com'

url_open_timeout = 60 #60 seconds
page_size = 200 #display maximum 200 entries on one page
history_size = 50 #maximum of entries in the history list

user_agent_default = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4';
