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
# skin.py:
# This file loads the GUI elements on the main screen.
#############################################################################

from string import *
import sys, os.path
import urllib
import urllib2
import re, random, string
import xbmc, xbmcgui
import re, os, time, datetime, traceback
import shutil
import zipfile
import socket
from settings import *
from libs2 import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

IMAGE_BG = 102
IMAGE_BG1 = 103
IMAGE_LOGO = 104
IMAGE_THUMB = 105
IMAGE_RATING = 126
LABEL_URLLBL = 106
LABEL_VERSION = 107
LABEL_INFOTEXT = 108
LABEL_DLINFOTEXT = 109
LABEL_LOADING = 110
LABEL_LISTPOS = 111
LIST_LIST1 = 112   
IMAGE_DLLOGO = 118
LABEL_DT = 119
LIST_LIST2 = 120
TEXT_BOX_LIST2 = 121 
LIST_LIST3 = 122
TEXT_BOX_LIST3 = 123
BUTTON_LEFT = 125
LIST_LIST4 = 127
BUTTON_RATE = 128
LIST_LIST5 = 129
BUTTON_RIGHT = 130
BUTTON_EXIT2 = 2125
Label_Protocol = 2108
######################################################################
# Description: creates internal variables for the widget controls
# Parameters : window: handle to the main window
# Return     : -
######################################################################
def load_skin(window):   
    #images
    window.bg = window.getControl(IMAGE_BG)
    window.bg1 = window.getControl(IMAGE_BG1)
    #window.logo = window.getControl(IMAGE_LOGO)
    window.user_thumb = window.getControl(IMAGE_THUMB)
    window.download_logo = window.getControl(IMAGE_DLLOGO)
    window.rating = window.getControl(IMAGE_RATING)    
    window.download_logo.setVisible(0)
                 
    #labels
    window.urllbl = window.getControl(LABEL_URLLBL)
    window.dt = window.getControl(LABEL_DT)
    
    window.version = window.getControl(LABEL_VERSION)
    window.version.setLabel('version: '+ Version + '.' + SubVersion)#, "font10")
    
    window.infotekst = window.getControl(LABEL_INFOTEXT)
    window.infotekst.setVisible(False)
    window.dlinfotekst = window.getControl(LABEL_DLINFOTEXT)
    window.dlinfotekst.setVisible(False)
    window.loading = window.getControl(LABEL_LOADING)
    window.loading.setVisible(False)
    window.listpos = window.getControl(LABEL_LISTPOS)
    
    try: window.labProtocol = window.getControl(Label_Protocol)
    except: pass
    
    #lists
    window.list1 = window.getControl(LIST_LIST1)
    window.list2 = window.getControl(LIST_LIST2)
    window.list2.setVisible(False)
    window.list3 = window.getControl(LIST_LIST3)
    window.list4 = window.getControl(LIST_LIST4) 
    window.list5 = window.getControl(LIST_LIST5)  
    window.list5.setVisible(False)
  
    item = xbmcgui.ListItem("Home")   
    window.list3.addItem(item)
    item = xbmcgui.ListItem("Favorites")   
    window.list3.addItem(item)
    item = xbmcgui.ListItem("Downloads")   
    window.list3.addItem(item) 
    if platform != 'xbox':
        item = xbmcgui.ListItem("View: " + window.listview)   
        window.list3.addItem(item)   
    item = xbmcgui.ListItem("Browse")   
    window.list3.addItem(item)
    item = xbmcgui.ListItem("Sign in")   
    window.list3.addItem(item)    
    item = xbmcgui.ListItem("Exit") 
    window.list3.addItem(item)
    
    item = xbmcgui.ListItem("Play")  
    window.list4.addItem(item)
    item = xbmcgui.ListItem("Add to Favorites")  
    window.list4.addItem(item)    
    item = xbmcgui.ListItem("Download") 
    window.list4.addItem(item)      
    item = xbmcgui.ListItem("Rate It") 
    window.list4.addItem(item)   
    item = xbmcgui.ListItem("Reload Playlist") 
    window.list4.addItem(item)      
    item = xbmcgui.ListItem("More Options...") 
    window.list4.addItem(item)   
    
    #textbox
    window.list2tb = window.getControl(TEXT_BOX_LIST2)
    #window.list2tb.setVisible(False)
 
    #textbox
    window.list3tb = window.getControl(TEXT_BOX_LIST3)
    window.list3tb.setVisible(False) 
    
    #exit button
    #window.exitbutton2 = window.getControl(BUTTON_EXIT2)
    
    #set the large list as default
    window.list = window.list1

    #end of function
    

