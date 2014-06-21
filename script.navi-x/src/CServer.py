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
###############################################################################

#############################################################################
#
# CServer:
# Handles all services with the Navi-Xtreme server.
#############################################################################

from string import *
import sys, os.path
import urllib
import urllib2
import re, random, string
import xbmc, xbmcgui, xbmcaddon
import re, os, time, datetime, traceback
import shutil
import zipfile
from settings import *
from CFileLoader import *
from libs2 import *
from CDialogLogin import *
from CDialogRating import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

######################################################################
# Description: Text viewer
######################################################################
class CServer: 
    def __init__(self):
        
        #public member of CServer class.
        self.user_id = ''
        
        #read the stored user ID
        self.read_user_id()

    ######################################################################
    # Description: -
    # Parameters : -
    # Return     : -
    ######################################################################            
    def login(self):
        keyboard = xbmc.Keyboard('', 'Enter User name')
        keyboard.doModal()
        if (keyboard.isConfirmed() != True):
            return -2
            
        username = keyboard.getText()

        keyboard = xbmc.Keyboard('', 'Enter Password')
        keyboard.doModal()
        if (keyboard.isConfirmed() != True):
            return -2
            
        password = keyboard.getText()
                   
        #login to the Navi-X server
        self.user_id = self.nxLogin(username, password)
        if self.user_id == '':
            #failed
            return -1

        print "Login to the NXServer was successful"

        #save the returned user ID
        self.save_user_id()             
        #success   
        return 0          

    ######################################################################
    # Description: Login function for Navi-Xtreme login.
    # Parameters : username: user name
    #              password: user password
    # Return     : blowfish-encrypted string identifying the user for 
    #              saving locally, or an empty string if the login failed.
    ######################################################################  
    def nxLogin(self, username, password):
        return getRemote('http://www.navixtreme.com/login/',{
            'method':'post',
            'postdata':urllib.urlencode({'username':username,'password':password})
        })['content']

    ######################################################################
    # Description: -
    # Parameters : -
    # Return     : -
    ######################################################################                     
    def logout(self):
        #empty the user ID
        self.user_id=''
        self.save_user_id()

    ######################################################################
    # Description: -
    # Parameters : -
    # Return     : -
    ######################################################################             
    def is_user_logged_in(self):
        if self.user_id != '':
            return True  
        return False

    ######################################################################
    # Description: -
    # Parameters : -
    # Return     : -
    ######################################################################            
    def rate_item(self, mediaitem):    
        #rate = CDialogRating("CRatingskin.xml", os.getcwd())
        rate = CDialogRating("CRatingskin.xml", addon.getAddonInfo('path'))
        rate.doModal()
        if rate.state != 0:
            return -2
                
        if self.is_user_logged_in() == False:
            dialog = xbmcgui.Dialog()
            dialog.ok(" Error", "You are not logged in.")
            return -1

        #login to the Navi-X server
        result = self.nxrate_item(mediaitem, rate.rating)

    ######################################################################
    # Description: -
    # Parameters : mediaitem: CMediaItem instance to rate
    #              rating = value [0-5]
    # Return     : -
    # API Return : Success: value [0-5] representing the new average rating
    #              Failure: error message string
    ######################################################################      
    def nxrate_item(self, mediaitem, rating):  
        result=getRemote('http://www.navixtreme.com/rate/',{
            'method':'post',
            'postdata':urllib.urlencode({'url':mediaitem.URL,'rating':rating}),
            'cookie':'nxid='+nxserver.user_id
        })['content']

        dialog = xbmcgui.Dialog()                            
        p=re.compile('^\d$')
        match=p.search(result)
        if match:
            dialog.ok(" Rate", "Rating Successful.")
            mediaitem.rating=result
        else:
            dialog.ok(" Rate", result)

        return 0
    
    ######################################################################
    # Description: -
    # Parameters : -
    # Return     : -
    ######################################################################     
    def read_user_id(self):
        try:
            f=open(RootDir + 'user_id.dat', 'r')
            self.user_id = f.read()
            f.close()
        except IOError:
            return   

    ######################################################################
    # Description: -
    # Parameters : -
    # Return     : -
    ###################################################################### 
    def save_user_id(self):
        f=open(RootDir + 'user_id.dat', 'w')
        f.write(self.user_id)    
        f.close()
        pass
 

#Create server instance here and use it as a global variable for all other components that import CServer.py.
global nxserver
nxserver = CServer() 

global re_server
re_server = re.compile('^[^:]+://(?:www\.)?([^/]+)')