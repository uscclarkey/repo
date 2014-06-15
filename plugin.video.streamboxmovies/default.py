import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
#below you can add anything here just to keep your typing down to a minimum(shortcuts)
import datetime
import time
import checks
# i.e 
#now look at the first addDir where i have written icon then look at second listed item i have put the url for image directly makes no odds how you do it !!
PLUGIN='plugin.video.streamboxmovies'
ADDON = xbmcaddon.Addon(id=PLUGIN)
    
#library=xbmc.translatePath(ADDON.getAddonInfo('profile'))

ORDERBY = ['releaseDate', 'rating', 'views']
URL     = 'http://simplymovies.net/'
from metahandler import metahandlers
 
from metahandler import metacontainers 
grab = metahandlers.MetaData()
icon = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.streamboxmovies', 'icon.png'))



#addDir('name','url','mode','iconimage','triler') mode is where it tells the plugin where to go scroll to bottom to see where mode is
def CATEGORIES():
        addDir('Main Page',     URL, 1, icon)
        addDir('Search Movies', URL, 5, icon)
        addDir('Search TV',     URL, 4, icon)
        addDir('Movie Genre',   URL, 6, icon)
        addDir('TV Genre',      URL, 7, icon)
        addDir('Go To Page',    URL, 1, icon)

        setView('movies', 'default') 
        #setView is setting the automatic view.....first is what section "movies"......second is what you called it in the settings xml  
       
       
                                                                      
def main(name,page = 0):#  cause mode is empty in this one it will go back to first directory
    _name=str(name)
    if 'Go To Page' in name:
        page = int(select_page())
        link = doSearch('movies', '', page = page).replace('\n','').replace('\r','').replace('\t','')
    else:
        link = doSearch('movies', '', page = page).replace('\n','').replace('\r','').replace('\t','')

    link      = link.split('<div class="movieInfoOverlay">')
    url       = '<a href="movie.php(.+?)">'
    name      = '<h3 class="overlayMovieTitle">(.+?)</h3>'
    iconimage = '<img src="(.+?)"'
    trailer   = 'href="http://youtube.com/embed/(.+?)"'
    imdb= 'href="http://www.imdb.com/title/tt(.+?)/"'
    ignore = True

    for p in link:
        if ignore:
            ignore = False
            continue

        match = re.compile(url).findall(p)
        myUrl = match[0]

        match  = re.compile(name).findall(p)
        myName = match[0]

        if 'img src' in p:
            match       = re.compile(iconimage).findall(p)
            myIconimage = match[0]
        else:
            myIconimage = ''

        if 'Trailer' in p:
            match     = re.compile(trailer).findall(p)
            myTrailer = match[0]
        else:
            myTrailer = ''   
             
        if 'imdb.com' in p:
            match     = re.compile(imdb).findall(p)
            imdbid = match[0]
        else:
            imdbid = ''        

        if ADDON.getSetting('meta')=='true':
                infoLabels=GRABMETA(myName,'movie',year=None,imdb=imdbid)
        else:
                infoLabels=''
            
        addDir(myName, URL+'movie.php'+myUrl, 200, myIconimage, myTrailer,'','',infoLabels=infoLabels)
    setView('movies', 'movies')
    
    addMore(len(link), mode = 1, page = page+1,name=_name)
    
    
    
def genre_movie(page = 0, genre = None):#  cause mode is empty in this one it will go back to first directory
    if not genre:
        link=OPEN_URL(URL)#.replace('\n','').replace('\r','').replace('\t','')
        link=link.split('onchange="submitForm(\'movies\');">')[2]
        link=link.split('</select>')[0]
        r='<option value=".+?">(.+?)</option>'
        genreSelect=[]
        match=re.compile(r).findall(link)
        for genre in match: 
            if genre not in genreSelect:
                genreSelect.append(genre)

        genre = genreSelect[xbmcgui.Dialog().select('Please Select Genre', genreSelect)]

    link = doSearch('movies', '', page = page, genre = genre).replace('\n','').replace('\r','').replace('\t','')

    link      = link.split('<div class="movieInfoOverlay">')
    url       = '<a href="movie.php(.+?)">'
    name      = '<h3 class="overlayMovieTitle">(.+?)</h3>'
    iconimage = '<img src="(.+?)"'
    trailer   = 'href="http://youtube.com/embed/(.+?)"'
    imdb= 'href="http://www.imdb.com/title/tt(.+?)/"'
    ignore = True

    for p in link:
        if ignore:
            ignore = False
            continue

        match = re.compile(url).findall(p)
        myUrl = match[0]

        match  = re.compile(name).findall(p)
        myName = match[0]

        if 'img src' in p:
            match       = re.compile(iconimage).findall(p)
            myIconimage = match[0]
        else:
            myIconimage = ''

        if 'Trailer' in p:
            match   = re.compile(trailer).findall(p)
            myTrailer = match[0]
        else:
            myTrailer = '' 
                
        if 'imdb.com' in p:
            match     = re.compile(imdb).findall(p)
            imdbid = match[0]
        else:
            imdbid = ''        

        if ADDON.getSetting('meta')=='true':
                infoLabels=GRABMETA(myName,'movie',year=None,imdb=imdbid)
        else:
                infoLabels=''
               
        addDir(myName, URL+'/movie.php'+myUrl, 200, myIconimage, myTrailer,'','',infoLabels=infoLabels)
    setView('movies', 'movies')

    addMore(len(link), mode = 6, page = page+1,name='changeme', genre = genre)
    
    
def genre_tv(page = 0, genre = None):#  cause mode is empty in this one it will go back to first directory
    if not genre:
        link=OPEN_URL(URL)#.replace('\n','').replace('\r','').replace('\t','')
        link=link.split('onchange="submitForm(\'movies\');">')[2]
        link=link.split('</select>')[0]
        r='<option value=".+?">(.+?)</option>'
        genreSelect=[]
        match=re.compile(r).findall(link)
        for genre in match: 
            if genre not in genreSelect:
                genreSelect.append(genre)

        genre = genreSelect[xbmcgui.Dialog().select('Please Select Genre', genreSelect)]

    link = doSearch('tv_shows', '', page = page, genre = genre).replace('\n','').replace('\r','').replace('\t','')

    link      = link.split('<div class="movieInfoOverlay">')
    url       = '<a href="tv_show.php(.+?)">'
    name      = '<h3 class="overlayMovieTitle">(.+?)</h3>'
    iconimage = '<img src="(.+?)"'
    trailer   = 'href="http://youtube.com/embed/(.+?)"'

    ignore = True

    for p in link:
        if ignore:
            ignore = False
            continue

        match = re.compile(url).findall(p)
        myUrl = match[0]

        match  = re.compile(name).findall(p)
        myName = match[0]

        if 'img src' in p:
            match       = re.compile(iconimage).findall(p)
            myIconimage = match[0]
        else:
            myIconimage = ''

        if 'Trailer' in p:
            match   = re.compile(trailer).findall(p)
            myTrailer = match[0]
        else:
            myTrailer = ''        
        addDir(myName, URL+'tv_show.php'+myUrl, 3, myIconimage, myTrailer)
    setView('movies', 'default')

    addMore(len(link), mode = 7, page = page+1,name='changeme', genre = genre)
    
    
def search_tv(page = 0, _search = None):#  cause mode is empty in this one it will go back to first directory
    if not _search:
        _search = getSearch()  
        if not _search:
            return

    link = doSearch('tv_shows', _search, page = page).replace('\n','').replace('\r','').replace('\t','')

    r='<h3 class="overlayMovieTitle">(.+?)</h3>.+?<a href="(.+?)"><img src="(.+?)"'
    match=re.compile(r).findall(link)
    #print '########################################'
    #print match
    for name,url,iconimage in match: 
        addDir(name, URL+url, 3, iconimage,'',name,'')
    setView('tvshows', 'default') 

    addMore(len(match), mode = 4, page = page+1,name='changeme', search = _search)


def search_movies(page = 0, _search = None):#  cause mode is empty in this one it will go back to first directory+)
    if not _search:
        _search = getSearch()  
        if not _search:
            return
    link = doSearch('movies', _search, page = page).replace('\n','').replace('\r','').replace('\t','')
    link = doSearch('movies', _search, page = page).replace('\n','').replace('\r','').replace('\t','')


    link      = link.split('<div class="movieInfoOverlay">')
    url       = '<a href="(.+?)">'
    name      = '<h3 class="overlayMovieTitle">(.+?)</h3>'
    iconimage = '<img src="(.+?)"'
    trailer   = 'href="http://youtube.com/embed/(.+?)"'
    imdb= 'href="http://www.imdb.com/title/tt(.+?)/"'
    ignore = True

    for p in link:
        if ignore:
            ignore = False
            continue

        match = re.compile(url).findall(p)
        myUrl = match[0]

        match  = re.compile(name).findall(p)
        myName = match[0]

        if 'img src' in p:
            match       = re.compile(iconimage).findall(p)
            myIconimage = match[0]
        else:
            myIconimage = ''

        if 'Trailer' in p:
            match   = re.compile(trailer).findall(p)
            myTrailer = match[0]
        else:
            myTrailer = '' 
             
        if 'imdb.com' in p:
            match     = re.compile(imdb).findall(p)
            imdbid = match[0]
        else:
            imdbid = ''        

        if ADDON.getSetting('meta')=='true':
                infoLabels=GRABMETA(myName,'movie',year=None,imdb=imdbid)
        else:
                infoLabels=''
        addDir(myName, URL+myUrl, 200, myIconimage, myTrailer,'','',infoLabels=infoLabels)

    setView('movies', 'movies') 

    addMore(len(link), mode = 5, page = page+1,name='changeme', search = _search)





   

def get_episodes(name,url,iconimage,showname):#  cause mode is empty in this one it will go back to first directory
    showname=name
    link=OPEN_URL(url).replace('make money','')
    if 'http://www.imdb.com/title' in link:
        match   = re.compile('http://www.imdb.com/title/tt(.+?)/').findall(link)
        imdbid = match[0]
    else:
        imdbid = ''        
    r='<h3>(.+?)</h3>'
    match=re.compile(r).findall(link)
    urlselect=[]
    nameselect=[]
    for season in match:
        urlselect.append(season)
        nameselect.append(season)
    season=nameselect[xbmcgui.Dialog().select('Please Select Season', urlselect)]
    r='<h3>%s</h3>'% season
    link=link.split(r)[1]
    link=link.split('<h3>')[0]
    r='<a href="(.+?)">(.+?)</a>'
    match=re.compile(r).findall(link)
    for url,name in match: 
        if ADDON.getSetting('meta')=='true':
            season=season.replace('Season ','')
            episode=name.replace('Episode ','')
            try:
                _name=episode.split(':')[0]
            except:
                _name=episode
            infoLabels=GRABMETA(showname,'tvshow',year=None,season=season,episode=_name,imdb=imdbid)
            if infoLabels['title']=='':
                name=name
            else:
                name=infoLabels['title']
            if infoLabels['cover_url']=='':
                iconimage=iconimage
            else:
                iconimage=infoLabels['cover_url']
        else:
            infoLabels=None
        addDir(name, URL+url, 200, iconimage,'',showname,season,infoLabels=infoLabels)
    setView('tvshows', 'episode') 
    
    
def getSearch():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search StreamBox Movies')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20            
        return search_entered


def doSearch(category, search, page = 0, genre = ''):
    limit      = int(ADDON.getSetting('results'))
    lastRecord = page * limit

    data = dict()
    data['table']      = category
    data['lastRecord'] = lastRecord
    data['limit']      = limit
    data['where']      = '1 && title LIKE \'%' + search +'%\' && genres LIKE \'%' + genre +'%\''
    data['orderBy']    = ORDERBY[int(ADDON.getSetting('sort'))] + ' DESC'

    url = 'loadMore.php'
    if category == 'tv_shows':     
        url = 'loadMoreTvShows.php'
        if data['orderBy'] == 'releaseDate DESC':
            data['orderBy'] = 'rating DESC'    

    data     = urllib.urlencode(data)
    response = urllib.urlopen(URL+url, data).read()

    if response == '0' or response == '1':
        if page == 0:
            return oldSearch(category, search)
      
    if response == '0': 
        return 'error'
    if response == '1':
        return 'finished'

    return response  
    
def select_page():
    dialog = xbmcgui.Dialog()
    start = 0
    page  = []
    pageshow  = []
    for yr in range(start, 200):
        page.append(str(yr))
        pageshow.append('Page '+str(yr))
    return page[xbmcgui.Dialog().select('Please Select A Page !', pageshow)]
    
    
def doSearchGOTO(category, search, page = 0, genre = ''):
    limit      = int(ADDON.getSetting('results'))


    data = dict()
    data['table']      = category
    data['lastRecord'] = lastRecord
    data['limit']      = limit
    data['where']      = '1 && title LIKE \'%' + search +'%\' && genres LIKE \'%' + genre +'%\''
    data['orderBy']    = ORDERBY[int(ADDON.getSetting('sort'))] + ' DESC'

    url = 'loadMore.php'
    if category == 'tv_shows':     
        url = 'loadMoreTvShows.php'
        if data['orderBy'] == 'releaseDate DESC':
            data['orderBy'] = 'rating DESC'    

    data     = urllib.urlencode(data)
    response = urllib.urlopen(URL+url, data).read()

    if response == '0' or response == '1':
        if page == 0:
            return oldSearch(category, search)
      
    if response == '0': 
        return 'error'
    if response == '1':
        return 'finished'

    return response     

def oldSearch(category, search):
    url = 'index.php'
    if category == 'tv_shows':  
        url = 'tv_shows.php'    

    url += '?searchTerm=' + urllib.quote_plus(search)

    return urllib.urlopen(URL+url).read()

def oldSearch(category, search):
    url = 'index.php'
    if category == 'tv_shows':  
        url = 'tv_shows.php'    

    url += '?searchTerm=' + urllib.quote_plus(search)

    return urllib.urlopen(URL+url).read()
    
     
    
def downloadPath(title):        		
    downloadFolder = ADDON.getSetting('download_folder')

    if ADDON.getSetting('ask_folder') == 'true':
        dialog = xbmcgui.Dialog()
	downloadFolder = dialog.browse(3, 'Save to folder...', 'files', '', False, False, downloadFolder)
	if downloadFolder == '' :
	    return None

    if downloadFolder is '':
        d = xbmcgui.Dialog()
	d.ok('StreamBox Movies','You have not set the default download folder.\nPlease update the addon settings and try again.','','')
	ADDON.openSettings(sys.argv[0])
	downloadFolder = ADDON.getSetting('download_folder')

    if downloadFolder == '' and ADDON.getSetting('ask_folder') == 'true':
        dialog = xbmcgui.Dialog()
	downloadFolder = dialog.browse(3, 'Save to folder...', 'files', '', False, False, downloadFolder)	

    if downloadFolder == '' :
        return None

    filename = title
    ext      = 'mp4'
   
    if ADDON.getSetting('ask_filename') == 'true':
        kb = xbmc.Keyboard(title, 'Save movie as...' )
	kb.doModal()
	if kb.isConfirmed():
	    filename = kb.getText()
	else:
	    return None
    else:
        filename = title

    filename  = re.sub('[:\\/*?\<>|"]+', '', filename)
    filename  = capitalize(filename)

    if not os.path.exists(downloadFolder ):
        os.mkdir(downloadFolder)

    filename += '.'
    filename += ext

    return os.path.join(downloadFolder, filename)

def capitalize(text):
    words = text.split(' ')
    nWord = len(words)
    
    text = ''

    for i in range(nWord):
        word = words[i].strip()
        if len(word) > 0:
            if i > 0:
                text += ' '
            if len(word) == 1:
                text += word[0].upper()
            else:
                text += word[0].upper() + word[1:]

    return text

def DOWNLOAD(name, url, iconimage):
    name = capitalize(name)
    url = getUrl(url, ADDON.getSetting('download_best'))

    savePath = downloadPath(name)

    if savePath:
        t = 200*len(savePath)
        xbmc.executebuiltin('XBMC.Notification(' + 'StreamBox Movies' + ', Downloading: ' + savePath + ',' + str(t) + ')')
        #print "Saving %s to %s" % (url, savePath)
        #urllib.urlretrieve(url, savePath)

        xbmc.sleep(t+500)
        script = os.path.join(xbmc.translatePath(ADDON.getAddonInfo('path')), "DownloadInBackground.py" )
        xbmc.executebuiltin( "RunScript(%s, %s, %s, %s, %s)" % ( script, urllib.unquote_plus(url), urllib.unquote_plus(savePath), urllib.unquote_plus(name), '10'))


def cleanFilename(filename):
    filename = re.sub('[:\\/*?\<>|"]+', ' ', filename)
    return filename
    
        
def LIBRARY_TV(name,url,iconimage):#  cause mode is empty in this one it will go back to first directory
    link=OPEN_URL(url)
    r='<h3>(.+?)</h3>'
    match=re.compile(r).findall(link)

    #foldermain = os.path.join(library, 'TV')
    foldermain = xbmc.translatePath(ADDON.getSetting('tvshow-folder'))
    if not os.path.exists(foldermain):
        os.mkdir(foldermain)

    foldername = os.path.join(foldermain, capitalize(cleanFilename(name)))
    if not os.path.exists(foldername):
        os.mkdir(foldername)

    for season in match:
        seasonfolder = capitalize(os.path.join(foldername, cleanFilename(season)))
        if not os.path.exists(seasonfolder):
            os.mkdir(seasonfolder)

        _r='<h3>%s</h3>'% season
        #print season
        firstsplit=link.split(season)[1]
        secondsplit=firstsplit.split('<h3>')[0]
        r_='<a href="(.+?)">(.+?)</a>'
        match1=re.compile(r_).findall(secondsplit)
        for _url,name_ in match1:
            Theurl = URL+_url
            _name=name_.replace(':','-')

            strm     = '%s?mode=1200&name=%s&url=%s&iconimage=None&trailer=None'% (sys.argv[0], _name,urllib.quote_plus(Theurl))
            _name    = name_.replace(':','-')
            filename = '%sx%s.strm'%(season.replace('Season ',''),_name.replace('Episode ',''))
            filename = cleanFilename(filename)
            filename = capitalize(filename)
            file     = os.path.join(seasonfolder,filename)
            #print file

            a = open(file, "w")
            a.write(strm)
            a.close()

    
def LIBRARY_MOVIE(name,url,iconimage,trailer):#  cause mode is empty in this one it will go back to first directory

    strm='%s?mode=1200&url=%s&name=%s&iconimage=%s&trailer=%s'% (sys.argv[0],urllib.quote_plus(url), name,iconimage,trailer)

    #foldername=os.path.join(library, 'Movies')
    foldermain = xbmc.translatePath(ADDON.getSetting('movie-folder'))

    if not os.path.exists(foldermain):
        os.mkdir(foldermain)

    filename = cleanFilename(str(name))
    filename = capitalize(filename) + '.strm'
    file     = os.path.join(foldermain,filename)
    #print file

    a = open(file, "w")
    a.write(strm)
    a.close()


def validateStream(url):
    try:
        req = urllib2.Request(url)
        req.add_header('Referer', URL)
        resp    = urllib2.urlopen(req)

        #content = int(resp.headers['Content-Length'])
        #type    = resp.headers['Content-Type'] #expect to be 'video/mp4'
        return resp
    except Exception, e:
        print "ERROR IN StreamBox Movies: " + str(e)
        return None

def getUrl(url, setting):
    maxQuality = 0
    maxUrl     = ''

    link   = OPEN_URL(url)
    r      = '<iframe class="videoPlayerIframe" src="(.+?)"></iframe>'
    match  = re.compile(r).findall(link)

    link   = OPEN_URL(match[0])
    r      ='url(.+?)=(.+?)&amp'
    match  = re.compile(r).findall(link)

    urlselect  = []
    resolution = []

    for res, url in match:
        if url not in urlselect:
            urlselect.append(url)
        if res not in resolution:
            resolution.append(res)
            value = int(res)
            if value > maxQuality:
                maxQuality = value
                maxUrl     = url

    if setting == 'true':
        url = maxUrl
    else:
        url = urlselect[xbmcgui.Dialog().select('Please Select Resolution', resolution)]    

    #print  url
    return url
        
def PLAY_STREAM(name, url, iconimage, strm = False,liz=None):

    url = getUrl(url, ADDON.getSetting('play_best'))

    resp = validateStream(url)
    
    if not resp:
        dlg = xbmcgui.Dialog()
        dlg.ok('StreamBox Movies', 'There was a problem trying to play %s' % name, '', 'Please note, some ISPs appear to block StreamBox Movies :-(')
        return

    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty("IsPlayable","true")
    if not strm:
        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        pl.clear()
        pl.add(url, liz)
        xbmc.Player().play(pl)
        return

    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    
    
def PLAY_TRAILER(name, url, iconimage, trailer):    
    if not iconimage:
        iconimage = "DefaultVideo.png"
    url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % trailer
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty("IsPlayable","true")
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()
    pl.add(url, liz)
    xbmc.Player().play(pl)

 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link
    
    
    
    
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

        
        
def GRABMETA(name,types,year=None,season=None,episode=None,imdb=None):
        type = types
        if year=='': year=None
        #
        if year==None:
                try: year=re.search('\s*\((\d\d\d\d)\)',name).group(1)
                except: year=None
        if year is not None: name=name.replace(' ('+year+')','').replace('('+year+')','')
        #
        if 'movie' in type:
                ### grab.get_meta(media_type, name, imdb_id='', tmdb_id='', year='', overlay=6)
                meta = grab.get_meta('movie',name,imdb,None,year,overlay=6)
                infoLabels = {'rating': meta['rating'],'trailer_url': meta['trailer_url'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],'director': meta['director'],'cast': meta['cast'],'fanart': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
        elif 'tvshow' in type:
                meta = grab.get_episode_meta(name,imdb, season, episode)
                infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'fanart': meta['backdrop_url'],'Episode': meta['episode'],'Aired': meta['premiered']}
        return infoLabels    
        
        
        
# this is the listing of the items        
def addDir(name, url, mode, iconimage, trailer='',showname='',season='',infoLabels=None):
        u  = sys.argv[0]
        u += "?url="       + urllib.quote_plus(url)
        u += "&mode="      + str(mode)
        u += "&name="      + urllib.quote_plus(name)
        u += "&iconimage=" + urllib.quote_plus(iconimage)
        u += "&trailer="   + urllib.quote_plus(trailer)
        u += "&showname="   + urllib.quote_plus(showname)
        u += "&season="   + urllib.quote_plus(season)

        menu=[]
        if mode==200 or mode==201:
            if 'movie.php' in url:
                if ADDON.getSetting('meta')=='true':
                        #print infoLabels['trailer_url'] 
                        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
                        liz.setInfo( type="Video", infoLabels=infoLabels)
                        if ADDON.getSetting('fanart')=='true':
                            liz.setProperty( "Fanart_Image", infoLabels['fanart'] )
                else:
                    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
                    liz.setInfo( type="Video", infoLabels={ "Title": name })
            else:
                if ADDON.getSetting('meta')=='true':
                    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
                    liz.setInfo( type="Video", infoLabels=infoLabels)
                    if ADDON.getSetting('fanart')=='true':
                        liz.setProperty( "Fanart_Image", infoLabels['fanart'] )
                else:
                    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
                    liz.setInfo( type="Video", infoLabels={ "Title": name })
            if trailer != '':
                menu.append(('Play Trailer','XBMC.RunPlugin(%s?mode=201&url=None&name=%s&iconimage=%s&trailer=%s)'% (sys.argv[0], name,iconimage,trailer)))
	        liz.addContextMenuItems(items=menu, replaceItems=False)
            menu.append(('Download','XBMC.RunPlugin(%s?mode=1000&url=%s&name=%s&iconimage=%s&trailer=%s)'% (sys.argv[0], urllib.quote_plus(url), name, iconimage, trailer)))        
            menu.append(('Add To Library','XBMC.RunPlugin(%s?mode=2000&name=%s&url=%s&iconimage=%s&trailer=%s)'% (sys.argv[0], name,urllib.quote_plus(url), iconimage, trailer)))
	    liz.addContextMenuItems(items=menu, replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
        elif mode==3:
            liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
            menu.append(('Add To Library','XBMC.RunPlugin(%s?mode=2001&name=%s&url=%s&iconimage=%s)'% (sys.argv[0], name,urllib.quote_plus(url),  iconimage)))
            liz.addContextMenuItems(items=menu, replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=True)
        else:
            liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=True)

        
#same as above but this is addlink this is where you pass your playable content so you dont use addDir you use addLink "url" is always the playable content         
def addLink(name, url, iconimage, trailer):
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty("IsPlayable","true")
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz, isFolder=False)


def addMore(more, mode, page,name, search = '', genre = ''):
    if more < int(ADDON.getSetting('results')):
        return

    u =  sys.argv[0]

    u += "?url="  + str('url')
    u += "&mode=" + str(mode)
    u += "&page=" + str(page)
    u += "&name=" + str(name)
    if search != '':
        u += "&search=" + urllib.quote_plus(search)

    if genre != '':
        u += "&genre=" + urllib.quote_plus(genre) 
        
    #print '#######################'+name+'####################################'
    if 'Go To Page' in name:
        page=int(page)-1
        name='[COLOR yellow]Page %s Load More...[/COLOR]'%(str(page))
        u = u.replace('Go To Page','Main Page')
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
        
    elif 'changeme' in name:
        liz = xbmcgui.ListItem(' Load More...', iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
    else:
        page=int(page)-1
        name='[COLOR yellow]Page %s Load More...[/COLOR]'%(str(page))
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
        
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
 
        
#below tells plugin about the views                
def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url       = None
name      = None
mode      = None
iconimage = None
trailer   = None
showname  = None
season  = None

genre     = None
search    = None
page      = 0

#print params


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
        trailer=urllib.unquote_plus(params["trailer"])
except:
        pass
try:        
        page=int(params["page"])
except:
        pass
try:        
        genre=urllib.unquote_plus(params["genre"])
except:
        pass
try:        
        search=urllib.unquote_plus(params["search"])
except:
        pass
try:        
        showname=urllib.unquote_plus(params["showname"])
except:
        pass
try:        
        season=urllib.unquote_plus(params["season"])
except:
        pass
        

#print "Mode: "      + str(mode)
#print "URL: "       + str(url)
#print "Name: "      + str(name)
#print "IconImage: " + str(iconimage)
#print "Page: "      + str(page)
#print "Search: "    + str(search)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
        
elif mode==2:
        choose_search()
       
elif mode==1:
        print page
        main(name,page)
        
elif mode==3:
        get_episodes(name,url,iconimage,showname)
        
elif mode==4:
        search_tv(page, search)
        
elif mode==5:
        search_movies(page, search)
        
elif mode==6:
        genre_movie(page, genre)
        
elif mode==7:
        genre_tv(page, genre)
        
elif mode==8:
        GoToPage()
        
elif mode==200:
        PLAY_STREAM(name,url,iconimage,False)

elif mode==1200:
        PLAY_STREAM(name,url,iconimage,True)
        
elif mode==201:
        PLAY_TRAILER(name,url,iconimage,trailer)
        
elif mode==1000:
        DOWNLOAD(name,url,iconimage)
        
elif mode==2000:
        LIBRARY_MOVIE(name,url,iconimage,trailer)
elif mode==2001:
        LIBRARY_TV(name,url,iconimage)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
