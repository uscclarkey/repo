import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

import json
import base64

ADDON = xbmcaddon.Addon(id='plugin.video.tvplayer')





def CATEGORIES():
   

    response=OPEN_URL('http://d3gbuig838qdtm.cloudfront.net/json/tvp/channels.json')
    
    link=json.loads(response)

    data=link['data']
    

    for field in data:
        name= field['channel']['name'].encode("utf-8")
        
        status=field['channel']['status']
        id=field['channel']['id']
        
        if status=='online':
            status='[COLOR green]   (%s)[/COLOR]'%status
        else:
            status='[COLOR red]   (%s)[/COLOR]'%status
        icon='http://static.simplestream.com/tvplayer/logos/150/Inverted/%s.png' % id    
        addDir(name+status,id,200,icon,'')
    if ADDON.getSetting('sort')== 'true':    
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)             
    setView('movies', 'default') 
       
               
 
def OPEN_URL(url):
    if ADDON.getSetting('proxy')== 'true':
        url='http://www.justproxy.co.uk/index.php?q='+base64.b64encode(url)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    


    
def PLAY_STREAM(name,url,iconimage):
    url='http://d2sy1af2shs9ve.cloudfront.net/tvplayer/streams/playlist/%s' % url
    
    response=OPEN_URL(url)    
    
    link=json.loads(response)

    
     
    stream=link['stream']

    

    server='http://'+re.compile('http://(.+?)/').findall (stream)[0]

    m3u8=OPEN_URL(stream)        
    
    if not 'chunklist' in  m3u8 :
        #M3U8_PATH=xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'), 'yo.m3u8'))
        if not 'http' in m3u8:

            match=re.compile('(.+?)\n').findall (m3u8)
            amount =len(match)-1
            g=server+match[amount]
        else:
            match=re.compile('http://(.+?)\n').findall (m3u8)
            amount =len(match)-1
            g='http://'+match[amount]
            
        M3U8_PATH=g
    else:
            
            M3U8_PATH=stream
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(M3U8_PATH)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    
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

def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        if mode ==200:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
        
 
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


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
        description=urllib.unquote_plus(params["description"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       

elif mode==200:

        PLAY_STREAM(name,url,iconimage)
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
