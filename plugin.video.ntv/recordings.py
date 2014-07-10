
import datetime
import os
import xbmc
import xbmcaddon
import time
import datetime
import utils

from sqlite3 import dbapi2 as sqlite3

RECORDS_DB = 'recordings.db'
ADDON      = xbmcaddon.Addon()


def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today()



def getConnection():    
    dbPath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    if not os.path.exists(dbPath):
        os.mkdir(dbPath)
   
    conn   = sqlite3.connect(os.path.join(dbPath, RECORDS_DB), timeout = 10, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread = False)

    createTable(conn)
    return conn



def createTable(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS recordings (cat TEXT, name TEXT, start TEXT, end TEXT)")
    c.close()



def getRecordings():
   c = getConnection().cursor()
   c.execute("SELECT DISTINCT cat, name, start, end FROM recordings")
   recordings = c.fetchall()
   c.close()
   return recordings



def add(cat, startDate, endDate, recordname):
    conn = getConnection()
    c    = conn.cursor()
    c.execute("INSERT OR REPLACE INTO recordings(cat, name, start, end) VALUES(?, ?, ?, ?)", [cat, recordname, startDate, endDate])
    conn.commit()
    c.close()
    if schedule(cat, startDate, endDate, recordname):
        utils.notification('Recording set for %s' % recordname)



def schedule(cat, startDate, endDate, recordname):
    startDate = parseDate(startDate)
    endDate   = parseDate(endDate)

    t = startDate - datetime.datetime.now()
    timeToRecording = (t.days * 86400) + t.seconds        
    
    now = datetime.datetime.now()
    
    startPadding = 180 #3 minutes
    endPadding   = 180 #3 minutes
    
    #startPadding = ADDON.getSetting('start_Padding')
    #endPadding   = ADDON.getSetting('end_Padding')    
                    
    timeToRecording = timeToRecording - startPadding  

    showNotification = True
    
    if timeToRecording < 0:
        #check if program is actually on now            
        if (endDate - now).days < 0:
            return False
        else:   
            showNotification = False
            timeToRecording  = 0
            startDate        = now
    else:
        startDate = startDate - datetime.timedelta(seconds = startPadding)
        #modify startDate if necessary; it shouldn't be earlier that 'now'
        if startDate < now:
            startDate = now           
                                  
    name = 'ntv-recording-%s-%s' % (cat, startDate)
    #cancel alarm first just in case it already exists
    xbmc.executebuiltin('CancelAlarm(%s,True)' % name)     
                        
    duration = endDate - startDate
    duration = (duration.days * 86400) + duration.seconds
    duration = duration + endPadding
    script   = os.path.join(ADDON.getAddonInfo('path'), 'record.py')
    args     = str(cat) + ',' + str(startDate) + ',' + str(endDate) + ',' + str(duration) + ',' + str(recordname)
    
    cmd = 'AlarmClock(%s,RunScript(%s,%s),%d,True)' % (name.encode('utf-8', 'replace'), script.encode('utf-8', 'replace'), args.encode('utf-8', 'replace'), timeToRecording/60)
    print "cmd = " + cmd
    xbmc.executebuiltin(cmd)
    return showNotification



def reschedule():
    try:
        recordings = getRecordings()

        for index in range(0, len(recordings)): 
            cat       = recordings[index][0]
            name      = recordings[index][1]
            startDate = recordings[index][2]
            endDate   = recordings[index][3]
    except:
        pass
        schedule(cat, startDate, endDate, name)
