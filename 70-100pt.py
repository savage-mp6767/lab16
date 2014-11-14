# Lab 16
# 70pt -  Add in movement buttons for up, down, left and right using WASD DONE
# 80pt -  Make sure the player can't go out of bounds to the left, right or down. DONE
# 90pt -  When you hit space, fire a missile straight up!  DONE
#         Subtract from how many missiles you have left DONE
# 100pt - Destroy the target if a missile hits it! DONE
# Hints: use drawpad.delete(enemy) in the collision detect function, which you can trigger DONE
# from the key press event... maybe a loop to keep checking until the rocket goes out of bounds? DONE
from Tkinter import *
root = Tk()
drawpad = Canvas(root, width=800,height=600, background='white')
player = drawpad.create_oval(390,580,410,600, fill="blue")
enemy = drawpad.create_rectangle(50,50,100,60, fill="red")
rocket1Fired = False
enemyAlive = True
direction = 5

class Rocket:
    def __init__(self,par,idx,x,y):
        global drawpad
        self.rocket = drawpad.create_rectangle(x,y,x + 5,y + 5)
        self.idx = idx
        self.parent = par
    
    def Animate(self):
        global drawpad
        global enemyAlive
        x1,y1,x2,y2 = drawpad.coords(self.rocket)
        if y1 > 0:
            drawpad.move(self.rocket,0,-4)
            if self.collisionDetect():
                drawpad.delete(enemy)
                enemyAlive = False
        else:
            drawpad.delete(self.rocket)
            self.parent.rocketList.remove(self)
            del self
    
    def collisionDetect(self):
        global oval
	global drawpad
	global enemy
	global enemyAlive
	if not enemyAlive:
	    return
	    
        x1,y1,x2,y2 = drawpad.coords(self.rocket) #top left, top right, bottom left, bottom right
        plyW = x2 - x1
        plyH = y2 - y1
        tx1,ty1,tx2,ty2 = drawpad.coords(enemy)
        tarW = tx2 - tx1
        tarH = ty2 - ty1
        
        if x1 > tx1 or x1 == tx1:
            if y1 > ty1 or y1 == ty1:
                if x2 < tx2 or x2 == tx2:
                    if y2 < ty2 + tarH or y2 == ty2:
                        return True
        return False

class myApp(object):
    def __init__(self, parent):
        
        global drawpad
        self.myParent = parent  
        self.myContainer1 = Frame(parent)
        self.myContainer1.pack()
        
        # Enter my text
        self.prompt = "Rockets left :"
        
        self.MoreRockets = Button(root,text="More rockets!",bg='Green')
        self.MoreRockets.pack()
        self.MoreRockets.bind("<Button-1>",self.AddRkts)
        
        self.label1 = Label(root, text=self.prompt, width=len(self.prompt), bg='green')
        self.label1.pack()

        self.rockets = 3
        self.strVar = StringVar()
        self.strVar.set(str(self.rockets))
        self.rocketList = []
        
        self.rocketsTxt = Label(root, textvariable=self.strVar, width=len(str(self.rockets)), bg='green')
        self.rocketsTxt.pack()
        
        # Adding the drawpad, adding the key listener, starting animation
        drawpad.pack()
        root.bind_all('<Key>', self.key)
        self.animate()
    
    def AddRkts(self,event):
        self.rockets += 3
        self.strVar.set(str(self.rockets))
    
    def animate(self):
        global drawpad
        global enemy
        global direction
        global rocket1
        global rocket1Fired
        global enemyAlive
        if enemyAlive:
            x1,y1,x2,y2 = drawpad.coords(enemy)
            if x2 > 800:
                direction = - 5
            elif x1 < 0:
                direction = 5
            drawpad.move(enemy, direction, 0)
            
        px1,py1,px2,py2 = drawpad.coords(player)
        
        for r in self.rocketList:
            r.Animate()

        drawpad.after(5,self.animate)
        
                
    def edgeDetect(self,direction): #direction = 1 up 2 down 3 left 4 right
            global drawpad
            x1,y1,x2,y2 = drawpad.coords(player)
            pw = x2 - x1
            ph = y2 - y1
            if x2 > drawpad.winfo_width() - pw: 
                if direction == 4:
                    return False
            elif x1 < 0 + pw:
                if direction == 3:
                    return False
            elif y1 > drawpad.winfo_height() - ph:
                if direction == 2:
                    return False
            elif y2 < 0 + ph:
                if direction == 1:
                    return False
            return True
            
    def key(self,event):
        global player
        global rocket1Fired
        if event.char == "w":
            if self.edgeDetect(1):
                drawpad.move(player,0,-4)
                #drawpad.move(rocket1,0,-4)
        elif event.char == "s":
            if self.edgeDetect(2):
                drawpad.move(player,0,4)
                #drawpad.move(rocket1,0,4)
        elif event.char == "a":
            if self.edgeDetect(3):
                drawpad.move(player,-4,0)
                #drawpad.move(rocket1,-4,0)
        elif event.char == "d":
            if self.edgeDetect(4):
                drawpad.move(player,4,0)
                #drawpad.move(rocket1,4,0)
        elif event.char == " ":
            if self.rockets > 0:
                px1,py1,px2,py2 = drawpad.coords(player)
                self.rockets = self.rockets - 1
                self.rocketList.append(Rocket(self,len(self.rocketList),px1,py1))
                self.strVar.set(str(self.rockets))
    
    def collisionDetect(self, rocket):
        rx1,ry1,rx2,ry2 = drawpad.coords(rocket)
app = myApp(root)
root.mainloop()