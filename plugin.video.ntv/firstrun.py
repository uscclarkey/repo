import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import net

net=net.Net()
ADDON = xbmcaddon.Addon(id='plugin.video.ntv')
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, "ntv.lwp")
UA="NTV-XBMC-HLS-" + ADDON.getAddonInfo('version') 


from hashlib import md5    

def LOGIN():
        loginurl = 'http://www.ntv.mx/index.php?c=3&a=4'
        username    =ADDON.getSetting('user')
        password =md5(ADDON.getSetting('pass')).hexdigest()

        data     = {'email': username,
                                                'psw2': password,
                                                'rmbme': 'on'}
        headers  = {'Host':'www.ntv.mx',
                                                'Origin':'http://www.ntv.mx',
                                                'Referer':'http://www.ntv.mx/index.php?c=3&a=0','User-Agent' : UA}
                                                
        html = net.http_POST(loginurl, data, headers).content
        if os.path.exists(cookie_path) == False:
                os.makedirs(cookie_path)
        net.save_cookies(cookie_jar)
        ADDON.setSetting('firstrun','true')
        
def EXIT():
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
            
def AUTH():
        try:
            os.remove(cookie_jar)
        except:
            pass
        username    =ADDON.getSetting('user')
        password =md5(ADDON.getSetting('pass')).hexdigest()
        url = 'http://ntv.mx/?c=3&a=4&email=%s&psw2=%s&rmbme=on'%(username,password)
        html = net.http_GET(url).content
        if 'success' in html:
            LOGIN()
            ADDON.setSetting('firstrun','true')
        else:
            dialog = xbmcgui.Dialog()
            winput=re.compile('"message":"(.+?)"').findall(html)
            if dialog.yesno("NTV.mx", winput[0],'', 'Please Try Again'):
                SIGNIN()
            else:
                EXIT()

countries=os.path.join(ADDON.getAddonInfo('path'), 'countries.json')

def OPEN_URL(url):
    req = urllib2.Request(url, headers={'User-Agent' : UA}) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link
    
    
def Search(name):
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Please Enter '+str(name))
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText()
            if search_entered == None:
                return False          
        return search_entered    
        
def Numeric(name):
        dialog = xbmcgui.Dialog()
        keyboard=dialog.numeric(0, 'Please Enter '+str(name))
        return keyboard  
        
def GetCountryID():
        f   = open(countries, "r")
        a = f.read()
        f.close()
        match=re.compile('"id": (.+?),"name": "(.+?)","code_phone": (.+?)]').findall(a)
        countryIDselect=[]
        nameselect=[]
        for countryID,name,code in match:
            nameselect.append(name+' (+'+code+')')
            countryIDselect.append(countryID)
        return countryIDselect[xbmcgui.Dialog().select('Please Country Code', nameselect)]
    
def SIGNIN():

    email=Search('Email')
    ADDON.setSetting('user',email)
    password=Search('Password')
    ADDON.setSetting('pass',password)
    AUTH()
        
    
def Launch():        
    dialog = xbmcgui.Dialog()
    if dialog.yesno("NTV.mx", 'Do you Wish To Register','', "Or Sign In",'Register','Sign In'):
    
        SIGNIN()
    
    else:
        firstname=Search('First Name')
        surname=Search('Surname')
        email=Search('Email')
        password=Search('Password')
        country_id=GetCountryID()
        phone=Numeric('Phone Number')
        url='http://www.ntv.mx/index.php?c=1&a=1&xbmc=1&r=xbmc&accdata={"email":"%s","firstname":"%s","lastname":"%s","psw":"%s","cntid":"%s","phnnm":"%s"}'%(email,firstname,surname,password,country_id,phone)
        link=OPEN_URL(url)
        if 'success' in link:
            dialog.ok("NTV.mx", 'Thank You For Registering','Please Open Your Email Client', 'And Verify Your Email Address')
            ADDON.setSetting('user',email)
            ADDON.setSetting('pass',password)
            ADDON.setSetting('firstrun','true')
        else:
            winput=re.compile('"message":"(.+?)"').findall(link)
            if dialog.yesno("NTV.mx", winput[0],'', 'Exit And Restart Again'):
                Launch()
            else:
                EXIT()


Launch()                
