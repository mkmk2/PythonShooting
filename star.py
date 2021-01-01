import pyxel
import imp
import random

StarData = []
STAR_NUM = 100

# --------------------------------------------------
class StarDt:

    # コンストラクタ
    def __init__(self, y):
        self.PosX = random.randrange(0, 255, 1)
        self.PosY = y
        self.VectorX = 0
        self.VectorY = random.randrange(3, 6, 1) / 10

# --------------------------------------------------
# スター
class Star:

    WaitTime = 0
    # コンストラクタ
    def __init__(self):
        for n in range(50):
            StarData.append(StarDt(random.randrange(0, imp.WINDOW_H, 1)))

    # メイン
    def update(self):
        self.WaitTime -= 1
        if self.WaitTime <= 0:
            self.WaitTime = random.randrange(1, 50, 1)
            StarData.append(StarDt(0))

        for s in StarData:
            s.PosX += s.VectorX
            s.PosY += s.VectorY

        for n,s in enumerate(StarData):
            if s.PosY >= imp.WINDOW_H:
                del StarData[n]        # リストから削除する

    # 描画
    def draw(self):
        for s in StarData:
            if pyxel.pget(s.PosX, s.PosY) == 0:
                pyxel.pset(s.PosX, s.PosY, 7)

# --------------------------------------------------

# --------------------------------------------------
