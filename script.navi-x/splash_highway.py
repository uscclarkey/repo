### ####################################################################### ### 
### import splash_highway as splash
### splash.do_My_Splash('http://i.imgur.com/NAiexjN.png',5); 
### splash.do_My_Splash('http://i.imgur.com/NAiexjN.png',2,True,100,100,600,400); 
### splash.do_My_TextSplash("Hello Player.\n",artj('text_splash01'),8,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=70); 
### ####################################################################### ### 
import xbmc,xbmcgui,time
### ####################################################################### ### 
class MyWindowCountDown(xbmcgui.WindowDialog):
	scr={}; #scr['L']=0; scr['T']=0; scr['W']=1280; scr['H']=720; 
	def __init__(self,bgArt='',L=0,T=0,W=1280,H=720):
		self.background=bgArt; self.scr['L']=L; self.scr['T']=T; self.scr['W']=W; self.scr['H']=H; 
		self.BG=xbmcgui.ControlImage(self.scr['L'],self.scr['T'],self.scr['W'],self.scr['H'],self.background,aspectRatio=0); 
		self.addControl(self.BG); 
		#t='0'; self.BG.setAnimations([('WindowOpen','effect=fade time='+t+' start=0 end=100'),('WindowClose','effect=fade time='+t+' end=0')])
		#self.close()
	def see(self): self.show(); 
	def updateBG(self,bgArt=''): self.background=bgArt; self.setImage(self.background); 
	def updateY(self,x,y): self.BG.setPosition(x,y); self.scr['L']=x; self.scr['T']=y; 
	def updateSize(self,w,h): self.BG.setWidth(w); self.BG.setHeight(h); self.scr['W']=w; self.scr['H']=h; 
	def updateW(self,w): self.BG.setWidth(w); self.scr['W']=w; 
	def updateH(self,h): self.BG.setHeight(h); self.scr['H']=h; 
	#def onInit(self): 
	#def onClick(self,control): 
	#def onControl(self,control): 
	#def onFocus(self,control): 
	#def onAction(self,action): 
def do_My_Splash(img='http://i.imgur.com/NAiexjN.png',HowLong=10,resize=False,L=0,T=0,W=1280,H=720): #HowLong in seconds.
	if resize==False: maxW=1280; maxH=720; W=maxW/2; H=maxH/2; L=maxW/4; T=maxH/4; 
	TempWindow2=MyWindowCountDown(bgArt=img,L=L,T=T,W=W,H=H); 
	StartTime=time.clock(); 
	while (time.clock()-StartTime) < HowLong:
		TempWindow2.show(); 
	try: del self.TempWindow2; 
	except: pass
### ####################################################################### ### 
class MyWindowCountDownWithText(xbmcgui.WindowDialog):
	scr={}; #scr['L']=0; scr['T']=0; scr['W']=1280; scr['H']=720; 
	def __init__(self,msg='',bgArt='',L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=10):
		self.background=bgArt; self.scr['L']=L; self.scr['T']=T; self.scr['W']=W; self.scr['H']=H; 
		self.BG=xbmcgui.ControlImage(self.scr['L'],self.scr['T'],self.scr['W'],self.scr['H'],self.background,aspectRatio=0); 
		self.addControl(self.BG); 
		self.TxtMessage=xbmcgui.ControlTextBox(self.scr['L']+BorderWidth,self.scr['T']+BorderWidth,self.scr['W']-(BorderWidth*2),self.scr['H']-(BorderWidth*2),font=Font,textColor=TxtColor); 
		self.addControl(self.TxtMessage); 
		self.TxtMessage.setText(msg); 
	def see(self): self.show(); 
	def updateBG(self,bgArt=''): self.background=bgArt; self.setImage(self.background); 
	def updateY(self,x,y): self.BG.setPosition(x,y); self.scr['L']=x; self.scr['T']=y; 
	def updateSize(self,w,h): self.BG.setWidth(w); self.BG.setHeight(h); self.scr['W']=w; self.scr['H']=h; 
	def updateW(self,w): self.BG.setWidth(w); self.scr['W']=w; 
	def updateH(self,h): self.BG.setHeight(h); self.scr['H']=h; 
	#def onInit(self): 
	#def onClick(self,control): 
	#def onControl(self,control): 
	#def onFocus(self,control): 
	#def onAction(self,action): 

def do_My_TextSplash(msg='',img='http://i.imgur.com/NAiexjN.png',HowLong=10,resize=False,L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=10): #HowLong in seconds.
	if resize==False: maxW=1280; maxH=720; W=maxW/2; H=maxH/2; L=maxW/4; T=maxH/4; 
	TempWindow2=MyWindowCountDownWithText(msg=msg,bgArt=img,L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
	StartTime=time.clock(); 
	while (time.clock()-StartTime) < HowLong:
		TempWindow2.show(); 
	try: del self.TempWindow2; 
	except: pass
### ####################################################################### ### 
class MyWindowCountDownWithText2(xbmcgui.WindowDialog):
	scr={}; #scr['L']=0; scr['T']=0; scr['W']=1280; scr['H']=720; 
	def __init__(self,msg='',bgArt='',L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=10,ImgexitBtn=''):
		self.background=bgArt; self.scr['L']=L; self.scr['T']=T; self.scr['W']=W; self.scr['H']=H; 
		self.BG=xbmcgui.ControlImage(self.scr['L'],self.scr['T'],self.scr['W'],self.scr['H'],self.background,aspectRatio=0,colorDiffuse='0xff00ff00'); 
		self.addControl(self.BG); 
		self.TxtMessage=xbmcgui.ControlTextBox(self.scr['L']+BorderWidth,self.scr['T']+BorderWidth,self.scr['W']-(BorderWidth*2),self.scr['H']-(BorderWidth*2),font=Font,textColor=TxtColor); 
		self.addControl(self.TxtMessage); 
		self.exitBtn=xbmcgui.ControlButton(self.scr['L']+self.scr['W']-13-22,self.scr['T']+10,22,22,"",textColor="0xFFFFFFFF",focusedColor="0xFFFF0000",font="font10",alignment=2,focusTexture=ImgexitBtn,noFocusTexture=ImgexitBtn); 
		self.addControl(self.exitBtn); 
		self.TxtMessage.setText(msg); 
		self.setFocus(self.exitBtn)
	def see(self): self.show(); 
	def updateBG(self,bgArt=''): self.background=bgArt; self.setImage(self.background); 
	def updateY(self,x,y): self.BG.setPosition(x,y); self.scr['L']=x; self.scr['T']=y; 
	def updateSize(self,w,h): self.BG.setWidth(w); self.BG.setHeight(h); self.scr['W']=w; self.scr['H']=h; 
	def updateW(self,w): self.BG.setWidth(w); self.scr['W']=w; 
	def updateH(self,h): self.BG.setHeight(h); self.scr['H']=h; 
	#def onInit(self): 
	#def onClick(self,control): 
	def onControl(self,control): 
		if control==self.exitBtn: self.close()
	#def onFocus(self,control): 
	def onAction(self,action): 
		if action in [10,92,7]: self.close() ## Escape, Backspace, Select ##

def do_My_TextSplash2(msg='',img='http://i.imgur.com/NAiexjN.png',HowLong=10,resize=False,L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=10,ImgexitBtn=''): #HowLong in seconds.
	if resize==False: maxW=1280; maxH=720; W=maxW/2; H=maxH/2; L=maxW/4; T=maxH/4; 
	TempWindow2=MyWindowCountDownWithText2(msg=msg,bgArt=img,L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth,ImgexitBtn=ImgexitBtn); 
	#StartTime=time.clock(); 
	#while (time.clock()-StartTime) < HowLong:
	#	TempWindow2.show(); 
	TempWindow2.doModal(); 
	try: del self.TempWindow2; 
	except: pass
def do_My_TextSplash3(msg='',img='http://i.imgur.com/NAiexjN.png',HowLong=10,resize=False,L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=10,ImgexitBtn=''): #HowLong in seconds.
	if resize==False: maxW=1280; maxH=720; W=1000; H=650; L=(maxW-W)/2; T=(maxH-H)/2; 
	TempWindow2=MyWindowCountDownWithText2(msg=msg,bgArt=img,L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth,ImgexitBtn=ImgexitBtn); 
	#StartTime=time.clock(); 
	#while (time.clock()-StartTime) < HowLong:
	#	TempWindow2.show(); 
	TempWindow2.doModal(); 
	try: del self.TempWindow2; 
	except: pass
### ####################################################################### ### 
