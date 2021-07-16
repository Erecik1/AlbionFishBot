import time
import wx
import win32api
import win32con

threshold = 93 
greenthreshold = 14 
drowned = 0.6 
catchtimeout = 30 
sizex = 50 
sizey = 120 
offsetx = -5 
offsety = 30 
splawikoffsety = 10 
splawikoffsetx = 0 
controlpixeloffsetx = 50 
timetosetcursor = 3 
screenscanfactor = (0.25, 0.25) 
testmode = 0 
timetohold = 0.4 


locale = wx.Locale.GetSystemLanguage()
app = wx.App(redirect=False)
app.locale = wx.Locale(locale)


screen = wx.ScreenDC()
screensize = screen.GetSize()
    
scansizex = int(screensize[0] * screenscanfactor[0]) 
scansizey = int(screensize[1] * screenscanfactor[1]) 

screenshot = wx.Bitmap(scansizex, scansizey)
mem2 = wx.MemoryDC(screenshot)


splawik = wx.Bitmap(sizex, sizey)
mem = wx.MemoryDC(splawik)
cursorpos = (0,0)


redness = 0
truex = 0
truey = 0
sumr = 0
    

time.sleep(timetosetcursor) 
cursorpos = win32api.GetCursorPos() 
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,cursorpos[0],cursorpos[1],0,0)
time.sleep(timetohold) 
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,cursorpos[0],cursorpos[1],0,0)
time.sleep(2)
win32api.SetCursorPos((0,0)) 


mem2.Blit(0,0, scansizex, scansizey, screen, cursorpos[0] - scansizex/2, cursorpos[1] - scansizey/2)
image = screenshot.ConvertToImage()
if (testmode == 1):
    image.SaveFile('splawdik.png', wx.BITMAP_TYPE_PNG)

if (image.HasAlpha()):
    image.ClearAlpha()
datapixel = image.GetData() 
stride = scansizex*3

for y in range(0,stride*scansizey, stride):
    for x in range(0,sizex*3, 3):
        index = y + x
        temp = datapixel[index] - datapixel[index + 1] - datapixel[index + 2]
        if (temp > threshold):
            sumr += temp


constantsizex = sizex*3 
constantsizey = sizey*stride 
constantscansizex = scansizex*3 
constantendy = (scansizey-sizey) * stride
y = 0
while True:

    for x in range(constantsizex, constantscansizex, 3):
        for sy in range(y, y+constantsizey, stride):
            index = sy + x
            temp = datapixel[index] - datapixel[index + 1] - datapixel[index + 2]
            if (temp > threshold):
                sumr += temp
                
            index -= constantsizex
            temp = datapixel[index] - datapixel[index + 1] - datapixel[index + 2]
            if (temp > threshold):
                sumr -= temp
                
        if (sumr > redness):
            truex = x - constantsizex
            truey = y
            redness = sumr
            
  
    y += stride
    if (y == constantendy):
        break
    for sx in range(constantscansizex - constantsizex, constantscansizex, 3):
        index = y + sx
        temp = datapixel[index] - datapixel[index + 1] - datapixel[index + 2]
        if (temp > threshold):
            sumr -= temp
            
        index += constantsizey
        temp = datapixel[index] - datapixel[index + 1] - datapixel[index + 2]
        if (temp > threshold):
            sumr += temp
                
    if (sumr > redness):
        truex = x - constantsizex
        truey = y
        redness = sumr

        
    for x in range(constantscansizex - constantsizex - 3, -3, -3):
        for sy in range(y, y + constantsizey, stride):
            index = sy + x
            temp = datapixel[index] - datapixel[index + 1] - datapixel[index + 2]
            if (temp > threshold):
                sumr += temp
                
            index += constantsizex
            temp = datapixel[index] - datapixel[index + 1] - datapixel[index + 2]
            if (temp > threshold):
                sumr -= temp
                
        if (sumr > redness):
            truex = x
            truey = y
            redness = sumr
            

    y += stride
    if (y == constantendy):
        break
    for sx in range(constantscansizex - constantsizex, constantscansizex, 3):
        index = y + sx
        temp = datapixel[index] - datapixel[index + 1] - datapixel[index + 2]
        if (temp > threshold):
            sumr -= temp
            
        index += constantsizey
        temp = datapixel[index] - datapixel[index + 1] - datapixel[index + 2]
        if (temp > threshold):
            sumr += temp
    if (sumr > redness):
        truex = x
        truey = y
        redness = sumr

if(truex != 0):
    positionx = cursorpos[0] - scansizex/2 + truex/3 + offsetx
    positiony = cursorpos[1] - scansizey/2 + truey/stride + offsety
    stride = 3 * sizex
    mem.Blit(0,0, sizex, sizey, screen, positionx, positiony)
    skanminigra = wx.Bitmap(1,1)
    controlpixel = wx.Bitmap(1,1)
    mem3 = wx.MemoryDC(skanminigra)
    mem4 = wx.MemoryDC(controlpixel)
    win32api.SetCursorPos(cursorpos)


    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,cursorpos[0],cursorpos[1],0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,cursorpos[0],cursorpos[1],0,0)
    time.sleep(4)

    while True:
        win32api.SetCursorPos(cursorpos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,cursorpos[0],cursorpos[1],0,0)
        time.sleep(timetohold) 
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,cursorpos[0],cursorpos[1],0,0)
        time.sleep(1.6) 
        win32api.SetCursorPos((0,0)) 

        mem.Blit(0,0, sizex, sizey, screen, positionx, positiony)
        datapixel = splawik.ConvertToImage().GetData()
        
        if (testmode == 1):
            splawik.ConvertToImage().SaveFile('splawik.png', wx.BITMAP_TYPE_PNG)


        sumr = 0
        for y in range(0,stride*sizey, stride):
            for x in range(0,constantsizex, 3):
                index = y + x
                temp = datapixel[index] - datapixel[index + 1] - datapixel[index + 2]
                if (temp > threshold):
                    sumr += temp
        redness = sumr

        catch = 0
        start = time.clock()
        down = 0
        while (time.clock() - start < catchtimeout):
            mem.Blit(0,0, sizex, sizey, screen, positionx, positiony)
            datapixel = splawik.ConvertToImage().GetData()
            sumr = 0
            for y in range(0,stride*sizey, stride):
                for x in range(0,constantsizex, 3):
                    index = y + x
                    temp = datapixel[index] - datapixel[index + 1] - datapixel[index + 2]
                    if (temp > threshold):
                        sumr += temp
            if (sumr == 0):
                break 
            if (redness - sumr > redness*drowned):
                if (testmode == 1):
                    print("catch")
                catch = 1
                win32api.SetCursorPos(cursorpos)
                time.sleep(0.05) 
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,cursorpos[0],cursorpos[1],0,0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,cursorpos[0],cursorpos[1],0,0)
                time.sleep(0.3)
                mem3.Blit(0,0, 1, 1, screen, int(screensize[0]/2)+splawikoffsety, int(screensize[1]/2)+splawikoffsetx)
                mem4.Blit(0,0, 1, 1, screen, int(screensize[0]/2)+controlpixeloffsetx, int(screensize[1]/2))
                controlimg = controlpixel.ConvertToImage()
                print((controlimg.GetGreen(0,0) - controlimg.GetBlue(0,0) - controlimg.GetRed(0,0)))
                skanimg = skanminigra.ConvertToImage()
                while ((controlimg.GetGreen(0,0) - controlimg.GetBlue(0,0) - controlimg.GetRed(0,0)) > greenthreshold):
                    if ((skanimg.GetGreen(0,0) - skanimg.GetBlue(0,0) - skanimg.GetRed(0,0)) > greenthreshold):
                        win32api.SetCursorPos(cursorpos)
                        if (down == 0):
                            down = 1
                            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,cursorpos[0],cursorpos[1],0,0)
                    else:
                        if (down == 1):
                            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,cursorpos[0],cursorpos[1],0,0)
                            down = 0
                    mem3.Blit(0,0, 1, 1, screen, screensize[0]/2+splawikoffsety, screensize[1]/2+splawikoffsetx)
                    mem4.Blit(0,0, 1, 1, screen, screensize[0]/2+controlpixeloffsetx, screensize[1]/2)
                    controlimg = controlpixel.ConvertToImage()
                    skanimg = skanminigra.ConvertToImage()

        if (down == 1):
            win32api.SetCursorPos(cursorpos)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,cursorpos[0],cursorpos[1],0,0)
        if (catch == 0 and sumr != 0):
            win32api.SetCursorPos(cursorpos)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,cursorpos[0],cursorpos[1],0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,cursorpos[0],cursorpos[1],0,0)
            time.sleep(0.4)
            print("timeout")
        else:
            time.sleep(0.5) #Gotcha