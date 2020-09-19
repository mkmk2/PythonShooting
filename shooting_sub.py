import pyxel
import random
import math
import imp
import enemy

#  ------------------------------------------
def GetDirection(self, x1, y1, x2, y2):
    
    x = x2 - x1
    y = y2 - y1
    a = math.atan2(y , x)
#        print(math.degrees(a))

    return a

#  ------------------------------------------
def SetVector(self, rot, rate):
    self.VectorX = math.cos(rot) * rate
    self.VectorY = math.sin(rot) * rate

#        print(self.VectorX)
#        print(self.VectorY)

#  ------------------------------------------
def DebugDrawPosHitRect(self):
    if imp._DEBUG_ == True:
        pyxel.pset(self.PosX, self.PosY, pyxel.frame_count % 16)
        pyxel.rectb(self.PosX - (self.HitRectX / 2), self.PosY - (self.HitRectY / 2), self.HitRectX, self.HitRectY, pyxel.frame_count % 16)
    return

