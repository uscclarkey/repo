import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time
import net
import json


PLUGIN='plugin.video.wliptv'
ADDON = xbmcaddon.Addon(id=PLUGIN)

streamtype = ADDON.getSetting('streamtype')
if streamtype == '0':
    STREAMTYPE = 'WLIPTV-XBMC-HLS-'
elif streamtype == '1':
    STREAMTYPE = 'WLIPTV-XBMC-'


UA=STREAMTYPE + ADDON.getAddonInfo('version') 
    
net=net.Net()

def OPEN_URL(url):
    req = urllib2.Request(url, headers={'User-Agent' : UA} ) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link


    
recordPath = xbmc.translatePath(os.path.join(ADDON.getSetting('record_path')))
        
imageUrl='http://www.wliptv.com/res/content/tv/'
CatUrl='http://www.wliptv.com/res/content/categories/'    
site='http://www.wliptv.com/index.php?c=6&a=0'
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, "wliptv.lwp")
from hashlib import md5    


def LOGIN():
        loginurl = 'http://www.wliptv.com/index.php?c=3&a=4'
        username    =ADDON.getSetting('user')
        password =md5(ADDON.getSetting('pass')).hexdigest()

        data     = {'email': username,
                                                'psw2': password,
                                                'rmbme': 'on'}
        headers  = {'Host':'www.wliptv.com',
                                                'Origin':'http://www.wliptv.com',
                                                'Referer':'http://www.wliptv.com/index.php?c=3&a=0','User-Agent' : UA}
                                                
        html = net.http_POST(loginurl, data, headers).content
        if 'success' in html:
            if os.path.exists(cookie_path) == False:
                    os.makedirs(cookie_path)
            net.save_cookies(cookie_jar)
            
            
def AUTH():
        try:
            os.remove(cookie_jar)
        except:
            pass
        username    =ADDON.getSetting('user')
        password =md5(ADDON.getSetting('pass')).hexdigest()
        url = 'http://wliptv.com/?c=3&a=4&email=%s&psw2=%s&rmbme=on'%(username,password)
        html = net.http_GET(url, headers={'User-Agent' :UA}).content
        if 'success' in html:
            LOGIN()
            ADDON.setSetting('firstrun','true')
        else:
            import firstrun

        

def CATEGORIES():
    AUTH()
    if ADDON.getSetting('enable_record')=='true':
        addDir('My Recordings','url',6,'','','','')
    addDir('My Account','url',8,'','','','')
    net.set_cookies(cookie_jar)
    link = net.http_GET(site+'&mwAction=categories&mwData=tv', headers={'User-Agent' : UA}).content
    data = json.loads(link)
    for field in data:
        cat= str(field['id'])
        name= field['name'].encode("utf-8")
        iconimage= field['icon'].encode("utf-8")
        addDir(name,'url',2,CatUrl+cat+'.png',cat,'','')
    setView('movies', 'main-view')         
        
def CHANNELS(name,cat):
    net.set_cookies(cookie_jar)
    now= datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S').replace(' ','%20')
    url='&mwAction=category&xbmc=1&mwData={"id":"%s","time":"%s","type":"tv"}'%(cat,now)
    link = net.http_GET(site+url, headers={'User-Agent' : UA}).content
    data = json.loads(link)
    channels=data['contents']
    offset= int(data['offset'])
    uniques=[]
    if not 'Favorites' in name:
	    if ADDON.getSetting('genre')=='true':
	        for field in channels:
	            name=field['genre']
	            url=field['genre_id']
	            if name not in uniques:
	                uniques.append(name)
	                addDir(name.title(),'url',5,'',cat,'','')
	                setView('movies', 'main-view')  
	    else:
	        
	        for field in channels:
	            endTime      =  field['time_to']
	            name         =  field['name'].encode("utf-8")
	            channel      =  field['id']
	            whatsup      =  field['whatsup'].encode("utf-8")
	            description  =  field['descr'].encode("utf-8")
	            r=re.compile("(.+?)-(.+?)-(.+?) (.+?):(.+?):(.+?)")
	            matchend     =  r.search(endTime)
	            endyear      =  matchend.group(1)
	            endmonth     =  matchend.group(2)
	            endday       =  matchend.group(3)
	            endhour      =  matchend.group(4)
	            endminute    =  matchend.group(5)

	            endDate  =  datetime.datetime(int(endyear),int(endmonth),int(endday),int(endhour),int(endminute)) + datetime.timedelta(seconds = offset)

	            
	            if ADDON.getSetting('tvguide')=='true':
	                name='%s - [COLOR yellow]%s[/COLOR]'%(name,whatsup)
	            addDir(name,'url',200,imageUrl+channel+'.png',channel,'',description,now,endDate,whatsup)
	            setView('movies', 'channels-view')         
    else:

        for field in channels:
            endTime      =  field['time_to']
            name         =  field['name'].encode("utf-8")
            channel      =  field['id']
            whatsup      =  field['whatsup'].encode("utf-8")
            description  =  field['descr'].encode("utf-8")
            r=re.compile("(.+?)-(.+?)-(.+?) (.+?):(.+?):(.+?)")
            matchend     =  r.search(endTime)
            endyear      =  matchend.group(1)
            endmonth     =  matchend.group(2)
            endday       =  matchend.group(3)
            endhour      =  matchend.group(4)
            endminute    =  matchend.group(5)
            

            endDate  =  datetime.datetime(int(endyear),int(endmonth),int(endday),int(endhour),int(endminute)) + datetime.timedelta(seconds = offset)

            
            if ADDON.getSetting('tvguide')=='true':
                name='%s - [COLOR yellow]%s[/COLOR]'%(name,whatsup)
            addDir(name,'url',200,imageUrl+channel+'.png',channel,'',description,now,endDate,whatsup)
            setView('movies', 'channels-view')         
            
def GENRE(name,cat):
    _GENRE_=name.lower()
    now= datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S').replace(' ','%20')
    
    net.set_cookies(cookie_jar)
    url='&mwAction=category&xbmc=2&mwData={"id":"%s","time":"%s","type":"tv"}'%(cat,now)
    link = net.http_GET(site+url, headers={'User-Agent' : UA }).content
    data = json.loads(link)
    channels=data['contents']
    uniques=[]
    
    offset= int(data['offset'])
    for field in channels:
        genre      =  field['genre']
        endTime      =  field['time_to']
        name         =  field['name'].encode("utf-8")
        channel      =  field['id']
        whatsup      =  field['whatsup'].encode("utf-8")
        description  =  field['descr'].encode("utf-8")
        r=re.compile("(.+?)-(.+?)-(.+?) (.+?):(.+?):(.+?)")
        matchend     =  r.search(endTime)
        endyear      =  matchend.group(1)
        endmonth     =  matchend.group(2)
        endday       =  matchend.group(3)
        endhour      =  matchend.group(4)
        endminute    =  matchend.group(5)

        endDate  =  datetime.datetime(int(endyear),int(endmonth),int(endday),int(endhour),int(endminute)) + datetime.timedelta(seconds = offset)

        
        if ADDON.getSetting('tvguide')=='true':
            name='%s - [COLOR yellow]%s[/COLOR]'%(name,whatsup)
        if genre == _GENRE_:
            addDir(name,'url',200,imageUrl+channel+'.png',channel,'',description,now,endDate,whatsup)
        setView('movies', 'channels-view')         
            
            
def MYACCOUNT():
    addDir('Buy Subscription','url',11,'','','','')
    addDir('My Subscriptions','url',9,'','','','')
    addDir('Past Orders','url',10,'','','','')
    
    
def SUBS():
    net.set_cookies(cookie_jar)
    link = net.http_GET('http://www.wliptv.com/?c=1&a=18', headers={'User-Agent' : UA}).content
    data = json.loads(link)
    body = data['body']
    for field in body:
        title= field['title']
        platform= field['platforms'].encode("utf-8")
        status= field['status'].encode("utf-8")
        time_left= field['time_left'].encode("utf-8")
        name='%s-%s-(%s)[COLOR yellow] %s[/COLOR] '%(title,platform,time_left,status)
        addDir_STOP(name,'url','','','','')
    setView('movies', 'main-view') 
    
def ORDERS():
    net.set_cookies(cookie_jar)
    link = net.http_GET('http://www.wliptv.com/?c=1&a=19', headers={'User-Agent' : UA}).content.encode('ascii', 'ignore')
    data = json.loads(link)
    body = data['body']
    for field in body:
        id= field['id'].encode("utf-8")
        price_total= field['price_total'].encode("utf-8")
        created= field['created'].encode("utf-8")
        status= field['status'].encode("utf-8")
        updated= field['updated'].encode("utf-8")
        name='%s-(%s)[COLOR yellow] %s-(%s)[/COLOR] '%(price_total, created, status, updated)
        addDir_STOP(name,'url','','','','')
    setView('movies', 'main-view') 
    
    
def BUYSUBS():
    net.set_cookies(cookie_jar)
    link = net.http_GET('http://wliptv.com/?c=4&a=7', headers={'User-Agent' : UA}).content
    data = json.loads(link)
    for field in data:
        cat= str(field['id'])
        name= field['fullname'].encode("utf-8")
        description= field['description'].encode("utf-8")
        addDir(name,'url',12,'',cat,'',description)
    setView('movies', 'channels-view') 
    
    
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
        
def CARDDETAILS(cat):
        nameselect=['Cancel','Visa','Mastercard']
        returnselect=['Cancel','visa','master']
        type= returnselect[xbmcgui.Dialog().select('Please Card Type', nameselect)]
        if not 'Cancel' in type:
	        name=Search('Name On Card').replace(' ','%20')
	        card=Numeric('16 Digit Card Number')
	        month=Numeric('Expiry Month')
	        year=Numeric('Expiry Full Year (YYYY)')
	        cvv=Numeric('Security On Back Of Card (CVV)')
	        url='https://www.wliptv.com/?c=8&a=15&oid=%s&card={"type":"%s","number":"%s","name":"%s","month":"%s","year":"%s","cvv":"%s"}'%(cat,type,card,name,month,year,cvv)
	        net.set_cookies(cookie_jar)
	        link = net.http_GET(url, headers={'User-Agent' : UA}).content
	        data = json.loads(link)
	        if 'success' in link:
	            dialog = xbmcgui.Dialog()
	            winput= data['message']
	            dialog.ok("wliptv", '',winput, '')
	        else:
	            dialog = xbmcgui.Dialog()
	            winput= data['message']
	            dialog.ok("wliptv", '',winput, '')
	            if dialog.yesno("wliptv", "Do You Want To Try Again", ""):
	               CARDDETAILS(cat)
	            else:
	                return

class card_payment(xbmcgui.WindowXMLDialog):
    def __init__(self,*args, **kwargs): 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
        self.cat = kwargs['cat'] 
        self.name = ""
        self.card_number = ""
        self.expiry_month = ""
        self.expiry_year = ""
        self.sec_cvv = ""
        self.card_type = ""
                          
    def onClick(self, controlID):
        if controlID == 7:
            if int(self.getControl(5).isSelected()) > 0:  self.card_type = 'master'
            if int(self.getControl(6).isSelected()) > 0:  self.card_type = 'visa'
            xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
            self.close()
            self.name = self.getControl(8).getText().replace(' ','%20') 
            self.card_number = self.getControl(9).getText()
            self.expiry_month = self.getControl(10).getText()
            self.expiry_year = self.getControl(21).getText()
            self.sec_cvv = self.getControl(22).getText()
            net.set_cookies(cookie_jar)
            url = 'https://www.wliptv.com/?c=8&a=15&oid=%s&card={"type":"%s","number":"%s","name":"%s","month":"%s","year":"%s","cvv":"%s"}'%(self.cat,
                                                                                                                                                 self.card_type,
                                                                                                                                                 self.card_number,
                                                                                                                                                 self.name,
                                                                                                                                                 self.expiry_month,
                                                                                                                                                 self.expiry_year,
                                                                                                                                                 self.sec_cvv)
            link = net.http_GET(url, headers={'User-Agent' : UA}).content
            data = json.loads(link)
            if 'success' in link:
                dialog = xbmcgui.Dialog()
                winput= data['message']
                dialog.ok("wliptv", '',winput, '')
            else:
                dialog = xbmcgui.Dialog()
                winput= data['message']
                dialog.ok("wliptv", '',winput, '')
                if dialog.yesno("wliptv", "Do You Want To Try Again", ""):
                    card_payment('thingy.xml',ADDON.getAddonInfo('path'),'DefaultSkin',cat=cat).show() 
                else: return
            
                    
    def show(self):
        self.doModal()
    
    
def CARDPAY(cat):
    dialog = xbmcgui.Dialog()
    if dialog.yesno("wliptv", "Are You Happy To Continue",'', "Please Input Card Details"):
        card_payment('thingy.xml',ADDON.getAddonInfo('path'),'DefaultSkin',cat=cat).show()
        
    else:
        return
    
def PAYSUBS(cat):
    dialog = xbmcgui.Dialog()
    net.set_cookies(cookie_jar)
    URL='http://www.wliptv.com/?c=4&a=8&item_id=%s&amount=1'%cat
    link = net.http_GET(URL, headers={'User-Agent' : UA}).content
    data = json.loads(link)
    if 'success' in link:
        cat= str(data['body'])
        CARDPAY(cat)
    elif 'failure' in link:
        dialog = xbmcgui.Dialog()
        winput= data['message']
        dialog.ok("wliptv", '',winput, '')
        return
    else:
        if dialog.yesno("wliptv", "You Have a Similar Subscription",'', "What Do You Want To Do","Extend","Create New"):
                print '######################################   CREATE NEW'
                link = net.http_GET(URL+'&force=1', headers={'User-Agent' : UA}).content
                data = json.loads(link)
                if 'success' in link:
                    cat= str(data['body'])
                    CARDPAY(cat)
                elif 'failure' in link:
                    winput= data['message']
                    dialog.ok("wliptv", '',winput, '')
                    return
        else:
                print '######################################   EXTEND'
                titlereturn = ['Cancel']
                idreturn = ['Cancel']
                body = data['body']
                candidates = body['candidates']
                
                for field in candidates:  
                    name='%s-(%s) [COLOR yellow]%s[/COLOR]'%(field['title'],field['time_left'],field['status_tag'])               
                    titlereturn.append(name)             
                    idreturn.append(field['id'])   
                cat= idreturn[xbmcgui.Dialog().select('Which Do You Want To Extend', titlereturn)]
                if 'Cancel' in cat:
	                print 'Cancel'
                else:
	                net.set_cookies(cookie_jar)
	                url=URL+'&opt=%s'%cat
	                link = net.http_GET(url, headers={'User-Agent' : UA}).content
	                data = json.loads(link)
	                
	                
	                if 'success' in link:
	                    cat= str(data['body'])
	                    CARDPAY(cat)
	                elif 'failure' in link:
	                    winput= data['message']
	                    dialog.ok("wliptv", '',winput, '')
	                    return
    
            
def ADD_FAV(cat):
    net.set_cookies(cookie_jar)
    url='&mwAction=favorite&mwData={"id":"%s","type":"tv"}'%cat
    link = net.http_GET(site+url, headers={'User-Agent' : UA}).content
    return
        
        
def TVGUIDE(name,cat):
    try:
        name.split(' -')[0]
    except:
        pass
    net.set_cookies(cookie_jar)
    now= datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S').replace(' ','%20')
    url='&mwAction=content&xbmc=1&mwData={"id":"%s","time":"%s","type":"tv"}'%(cat,now)
    link = net.http_GET(site+url, headers={'User-Agent' : UA}).content
    data = json.loads(link)
    offset= int(data['offset'])
    guide=data['guide']
    for field in guide:
        r=re.compile("(.+?)-(.+?)-(.+?) (.+?):(.+?):(.+?)")
        startTime= field['time']
        endTime= field['time_to']
        name= field['name'].encode("utf-8")
        recordname= field['name'].encode("utf-8")
        description= field['description'].encode("utf-8")
        match = r.search(startTime)
        matchend = r.search(endTime)
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        hour = match.group(4)
        minute = match.group(5)
        endyear = matchend.group(1)
        endmonth = matchend.group(2)
        endday = matchend.group(3)
        endhour = matchend.group(4)
        endminute = matchend.group(5)

        startDate= datetime.datetime(int(year),int(month),int(day),int(hour),int(minute)) + datetime.timedelta(seconds = offset)
        endDate= datetime.datetime(int(endyear),int(endmonth),int(endday),int(endhour),int(endminute)) + datetime.timedelta(seconds = offset)
        time='[COLOR yellow](%s) - [/COLOR]'%(startDate.strftime('%H:%M'))
        

        addDir(time+name,'url',200,imageUrl+cat+'.png',cat,startDate,description,startDate,endDate,recordname)
        setView('movies', 'tvguide-view')         
        
        
    
def PLAY_STREAM(name,url,iconimage,cat):
    try:
        _name=name.split(' -')[0].replace('[/COLOR]','').replace('[COLOR yellow]','')
        playername=name.split('- ')[1].replace('[/COLOR]','').replace('[COLOR yellow]','')
    except:
        _name=name.replace('[/COLOR]','')
        playername=name.replace('[/COLOR]','')
    net.set_cookies(cookie_jar)
    url = '&mwAction=content&xbmc=1&mwData={"id":%s,"type":"tv"}'%cat
    link = net.http_GET(site+url, headers={'User-Agent' : UA}).content
    
    if '"allown":false' in link:
        try:
            match=re.compile('"message":"(.+?)"').findall(link)
            dialog = xbmcgui.Dialog()
            dialog.ok("wliptv", '', match[0].replace('\/','/'))
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("wliptv", '', 'Please Sign Up To Watch The Streams')
        
    else:
        match=re.compile('"src":"(.+?)","type":"rtmp"').findall(link)
        if match:
            rtmp=match[0].replace('\/','/')
            playpath=rtmp.split('live/')[1]
            app='live?'+rtmp.split('?')[1]
            url='%s swfUrl=http://wliptv.com/inc/strobe/StrobeMediaPlayback.swf app=%s playPath=%s pageUrl=http://wliptv.com/?c=2&a=0&p=50 timeout=10'%(rtmp,app,playpath)
        else:
            match=re.compile('"src":"(.+?)","type":"hls"').findall(link)
            hls=match[0].replace('\/','/')
            url=hls
        liz=xbmcgui.ListItem(playername, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": playername} )
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
            


        
def EXIT():
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
        

def scheduleRecording(cat, startDate, endDate, recordname):
    import recordings
    recordings.add(cat, startDate, endDate, recordname)
    
    
def DOWNLOADS():
     import glob
     path = recordPath
     for infile in glob.glob(os.path.join(path, '*.flv')):
         addFile(infile)

def addFile(file):
        name = file.replace(recordPath,'').replace('.flv','')
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png")
        liz.setInfo( type="Video", infoLabels={ "Title": str(name)})
        liz.setProperty("IsPlayable","true")
        contextMenu = []
        contextMenu.append(('Delete', 'XBMC.RunPlugin(%s?mode=102&url=%s)'% (sys.argv[0], file)))
        liz.addContextMenuItems(contextMenu,replaceItems=True)
        xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url=file,listitem = liz, isFolder = False)
        setView('movies', 'main-view')
        
        
def deleteFile(file):
    tries    = 0
    maxTries = 10
    while os.path.exists(file) and tries < maxTries:
        try:
            os.remove(file)
            break
        except:
            xbmc.sleep(500)
            tries = tries + 1
        
        
                    
        
        

                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addDir(name,url,mode,iconimage,cat,date,description,startDate='',endDate='',recordname=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&cat="+urllib.quote_plus(cat)+"&date="+str(date)+"&description="+urllib.quote_plus(description)+"&startDate="+str(startDate)+"&endDate="+str(endDate)+"&recordname="+urllib.quote_plus(recordname)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        menu=[]
        if mode==200 or mode==12:
            menu.append(('[COLOR yellow][B]TV Guide[/B][/COLOR]','XBMC.Container.Update(%s?name=None&mode=4&url=None&iconimage=None&cat=%s)'% (sys.argv[0],cat)))
            if ADDON.getSetting('enable_record')=='true':
                menu.append(('[COLOR red][B]RECORD[/B][/COLOR]','XBMC.RunPlugin(%s?mode=2001&url=url&cat=%s&startDate=%s&endDate=%s&recordname=%s)'% (sys.argv[0],urllib.quote_plus(cat),startDate,endDate,urllib.quote_plus(recordname))))
            menu.append(('[COLOR orange][B]Toggle Favourites[/B][/COLOR]','XBMC.RunPlugin(%s?name=None&mode=7&url=None&iconimage=None&cat=%s)'% (sys.argv[0],cat)))
            liz.setProperty("IsPlayable","true")
            liz.addContextMenuItems(items=menu, replaceItems=True)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def addDir_STOP(name,url,iconimage,cat,date,description,startDate='',endDate='',recordname=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&cat="+urllib.quote_plus(cat)+"&date="+str(date)+"&description="+urllib.quote_plus(description)+"&startDate="+str(startDate)+"&endDate="+str(endDate)+"&recordname="+urllib.quote_plus(recordname)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Premiered":date,"Plot":description} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
 
        
#below tells plugin about the views                
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
date=None
description=None
cat=None
startDate=None
endDate=None
record=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:
        cat=urllib.unquote_plus(params["cat"])
except:
        pass
try:
        date=str(params["date"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:
        startDate=str(params["startDate"])
except:
        pass
try:
        endDate=str(params["endDate"])
except:
        pass
try:
        recordname=urllib.unquote_plus(params["recordname"])
except:
        pass
        
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)

        
#these are the modes which tells the plugin where to         
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
               
elif mode==2:
        CHANNELS(name,cat)
                
elif mode==4:
        TVGUIDE(name,cat)
        
elif mode==5:
        GENRE(name,cat)
        
elif mode==6:
    DOWNLOADS()
    
elif mode==7:
    ADD_FAV(cat)
    
elif mode==8:
    MYACCOUNT()
    
elif mode==9:
    SUBS()
    
elif mode==10:
    ORDERS()
    
elif mode==11:
    BUYSUBS()
    
elif mode==12:
    PAYSUBS(cat)
    
elif mode==102:
    deleteFile(url)
    xbmc.executebuiltin("Container.Refresh")

        
elif mode==200:
        PLAY_STREAM(name,url,iconimage,cat)

elif mode==2001:
        scheduleRecording(cat, startDate, endDate,recordname)
                
xbmcplugin.endOfDirectory(int(sys.argv[1]))
