import pyxel
import imp
import random
import shooting_sub

# Id0
# 0:
# 1: 

# --------------------------------------------------
# 敵クラス
class Effect(imp.Sprite):

    # コンストラクタ
    def __init__(self, x, y, id0, id1, item):
        imp.Sprite.__init__(self, x, y, id0, id1, item)       # Spriteクラスのコンストラクタ

        self.PosAdjX = -8
        self.PosAdjY = -4

        self.PtnTime = 4
        self.PtnNo = 0

        if self.Id0 == 1:       # 移動する
            shooting_sub.SetVector(self, self.Id1, (random.randrange(5, 20, 1) / 10))

    # メイン
    def EffectMove(self):
        if self.Id0 != 4:       # GameOver以外
            self.PtnTime -= 1
            if self.PtnTime <= 0:
                self.PtnTime = 6

                self.PtnNo += 1
                if self.PtnNo >= 3:
                    self.PtnNo = 3
                    self.Death = 1

            if self.Id0 == 1:       # 移動する
                self.PosX += self.VectorX
                self.PosY += self.VectorY

    # 描画
    def Draw(self):
        if self.Id0 != 4:           # GameOver以外
            if self.PtnNo == 0:
                x = self.PosX - 4
                y = self.PosY - 4
                pyxel.blt(x, y, 0, 0, 8*20, 8, 8, 0)
            elif self.PtnNo == 1:
                x = self.PosX - 4
                y = self.PosY - 4
                pyxel.blt(x, y, 0, 8, 8*20, 8, 8, 0)
            elif self.PtnNo == 2:
                x = self.PosX - 4
                y = self.PosY - 4
                pyxel.blt(x, y, 0, 16, 8*20, 12, 12, 0)
            elif self.PtnNo == 3:
                x = self.PosX - 4
                y = self.PosY - 4
                pyxel.blt(x, y, 0, 32, 8*20, 12, 12, 0)
        else:
            # GAME OVER
            pyxel.blt(self.PosX,      self.PosY, 0, 0,    8*18, 8*4, 16, 0)
            pyxel.blt(self.PosX + 40, self.PosY, 0, 8*4,  8*18, 8*4, 16, 0)

# --------------------------------------------------

# --------------------------------------------------
