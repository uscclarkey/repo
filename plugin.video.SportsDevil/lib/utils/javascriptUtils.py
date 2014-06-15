# -*- coding: latin-1 -*-

import re
import urllib
from string import join

class JsFunctions:
    
    def hp_d01(self, s):
        ar=[]
        os=""
        for i in range(0,len(s)-1):
            c = ord(s[i])
            if c < 128:
                c = c^2
            os += chr(c)
            if len(os) > 80:
                ar.append(os)
                os = ""
        o = join(ar,'') + os
        return o
    
    def o61a2a8f(self, s):
        r = "";
        tmp = s.split("18267506");
        s = urllib.unquote(tmp[0]);
        k = urllib.unquote(tmp[1] + "511382");
        for i in range(0,len(s)-1):
            r += chr((int(k[i%len(k)])^ord(s[i]))+1);
        return r;
    
    def n98c4d2c(self, s):
        txtArr = s.split('18234663')
        s = urllib.unquote(txtArr[0])
        t = urllib.unquote(txtArr[1] + '549351')
        tmp=''
        for i in range(0,len(s)-1):
            tmp += chr((int(t[i%len(t)])^ord(s[i]))+-6)
        return urllib.unquote(tmp)
    
    def RrRrRrRr(self, teaabb):
        tttmmm=""
        l=len(teaabb)
        www = hhhhffff = int(round(l/2))
        if l<2*www:
            hhhhffff -= 1
        for i in range(0,hhhhffff-1):
            tttmmm = tttmmm + teaabb[i] + teaabb[i+hhhhffff]
        if l<2*www :
            tttmmm = tttmmm + teaabb[l-1]
        return tttmmm
    
    def ew_dc(self, s):
        d=''
        a=[]
        for i in range(0, len(s)-1):
            c = ord(s[i])
            if (c<128):
                c = c^5
            d += chr(c)
            if (i+1) % 99 == 0:
                a.append(d)
                d=''
        r = join(a,'') + d
        return r
    
    def pbbfa0(self, s):
        r = ""
        tmp = s.split("17753326")
        s = urllib.unquote(tmp[0])
        k = urllib.unquote(tmp[1] + "527117")
        for i in range(0,len(s)):
            r += chr((int(k[i%len(k)])^ord(s[i]))+7)
        return r
    

    
    
class JsUnpacker:

    def unpackAll(self, data):
        sPattern = '(eval\(function\(p,a,c,k,e,d\)\{while.*?)\s*</script>'
        return re.sub(sPattern, lambda match: self.unpack(match.group(1)), data)
    
    def containsPacked(self, data):
        return 'p,a,c,k,e,d' in data
        
    def unpack(self, sJavascript):
        aSplit = sJavascript.split(";',")
        p = str(aSplit[0])
        aSplit = aSplit[1].split(",")
        a = int(aSplit[0])
        c = int(aSplit[1])
        k = aSplit[2].split(".")[0].replace("'", '').split('|')
        e = ''
        d = ''
        sUnpacked = str(self.__unpack(p, a, c, k, e, d))
        return sUnpacked.replace('\\', '')
    
    def __unpack(self, p, a, c, k, e, d):
        while (c > 1):
            c = c -1
            if (k[c]):
                p = re.sub('\\b' + str(self.__itoa(c, a)) +'\\b', k[c], p)
        return p
    
    def __itoa(self, num, radix):
        result = ""
        while num > 0:
            result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
            num /= radix
        return result

