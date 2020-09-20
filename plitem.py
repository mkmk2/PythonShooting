import pyxel
import imp

# Id0
# 0:
# 1: 

# --------------------------------------------------
# 敵クラス
class PlItem(imp.Sprite):

    # コンストラクタ
    def __init__(self, x, y, id0, id1, item):
        imp.Sprite.__init__(self, x, y, id0, id1, item)       # Spriteクラスのコンストラクタ

        self.PosAdjX = -4
        self.PosAdjY = -4

        self.PosVectorY = -4

        self.PtnTime = 300
        self.PtnNo = 0

        self.HitPoint = 1
        self.HitRectX = 8
        self.HitRectY = 8

        self.ScreenTime = 120

    # メイン
    def PlItemMove(self):

        if self.PosVectorY < 0:
            self.PosVectorY += 0.2
            self.PosY += self.PosVectorY
        else:
            self.PosVectorY = 0

        self.PosY += 0.5
        
    #    self.PtnTime -= 1
    #    if self.PtnTime <= 0:
    #        self.Death = 1

        # 画面内チェック
        self.ScreenTime -= 1
        if self.ScreenTime < 0:
            if imp.CheckScreenIn(self) == False:
                self.Death = 1

    # 描画
    def Draw(self):
        x = self.PosX - 4
        y = self.PosY - 4
        pyxel.blt(x, y, 0, 48, 0, 8, 8, 0)

# --------------------------------------------------

# --------------------------------------------------
