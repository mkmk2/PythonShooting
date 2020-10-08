
_DEBUG_ = False

WINDOW_W = 255
WINDOW_H = 240
CAT_H = 16
CAT_W = 16

COLOR_WHITE = 7
COLOR_RED = 8

BLOCK_DOWN_WAIT = 6

GAME_STATUS_TITLE = 0
GAME_STATUS_MAIN = 1
GAME_STATUS_GAMEOVER = 2
GAME_STATUS_STAGECLEAR = 3

POS_FIELD_X = 10
POS_FIELD_Y = 4

SCREEN_TIME = 100

EM0 = 0
EM1 = 1
EM2 = 2
EMBOSS = 10

# 敵のセット位置
STAGE_EM_POS = [            # 時間, X, Y, id0, id1, item

    [ 100, 128,   0, EMBOSS,  0, 0,],   # Boss

    [ 200,  128-60,   0,  EM2,  0, 0,],    # まっすぐ
    [ 240,  128-60,   0,  EM2,  0, 0,],
    [ 280,  128-60,   0,  EM2,  0, 1,],

    [ 500,  128+60,   0,  EM2,  0, 0,],
    [ 540,  128+60,   0,  EM2,  0, 0,],
    [ 580,  128+60,   0,  EM2,  0, 1,],

    [ 760,  128-20,   0,  EM1,  0, 0,],    # カーブ
    [ 780,  128-40,   0,  EM1,  0, 0,],
    [ 800,  128-60,   0,  EM1,  0, 1,],

    [1000,  128+20,   0,  EM1,  0, 0,],
    [1020,  128+40,   0,  EM1,  0, 0,],
    [1040,  128+60,   0,  EM1,  0, 1,],

    [1300,  128-40,   0,  EM1,  0, 0,],    # カーブ
    [1340,  128-60,   0,  EM1,  0, 0,],
    [1380,  128-80,   0,  EM1,  0, 1,],

    [1600,  128+40,   0,  EM1,  0, 1,],
    [1640,  128+60,   0,  EM1,  0, 1,],
    [1680,  128+80,   0,  EM1,  0, 1,],

    [1750,  128-40,   0,  EM0,  0, 1,],    # 撃ってもどる
    [1800,  128+40,   0,  EM0,  0, 1,],

    [1900,  128-00,   0,  EM0,  2, 1,],    # 全方向撃って戻る
    [2300,  128-40,   0,  EM0,  2, 1,],    # 全方向撃って戻る
    [2700,  128+40,   0,  EM0,  2, 1,],    # 全方向撃って戻る

    [3500, 128,   0, EMBOSS,  0, 0,],   # Boss

]

TEST_EM_POS = [            # 時間, X, Y, id0, id1
    [ 20, 180,   0,  EM0,  1,],       #test
    [ 40, 100,   0,  EM2,  0,],

    [ 50,  40,   0,  EM0,  0,],
    [100,  60,   0,  EM0,  0,],
    [150,  80,   0,  EM0,  0,],
    [200, 100,   0,  EM0,  0,],
    [250, 120,   0,  EM0,  0,],

    [300, 215,   0,  EM0,  0,],
    [350, 195,   0,  EM0,  0,],
    [400, 175,   0,  EM0,  0,],
    [450, 155,   0,  EM0,  0,],
    [500, 135,   0,  EM0,  0,],

    [550,  80,   0,  EM1,  0,],
    [570,  80,   0,  EM1,  0,],

    [ 20, 128,   0, EMBOSS,  0,],   # Boss

]


# プレイヤーオブジェクト
Pl = []
# プレイヤーの弾
PlBullet = []

# 敵オブジェクト
Em = []
# 敵の弾
EmBullet = []

# エフェクト
Eff = []

# アイテム
Itm = []

TilePosX = 0
TilePosY = 0

Game_Status = GAME_STATUS_TITLE

# スコア
Score = 0


# --------------------------------------------------
# スプライト表示の共通クラス
class Sprite:

    # コンストラクタ
    def __init__(self, x, y, id0, id1, itemset):
        self.PosX = x
        self.PosY = y
        self.VectorX = 0
        self.VectorY = 0
        self.PosAdjX = 0
        self.PosAdjY = 0
        self.Rot = 0
        self.Id0 = id0
        self.Id1 = id1
        self.ItemSet = itemset

        self.St0 = 0
        self.St1 = 0
        self.St2 = 0

        self.PtnTime = 0
        self.PtnNo = 0

        self.Display = 1
        self.Life = 10
        self.Death = 0                  # 1:インスタンスを削除する
        self.ScreenTime = 0             # 画面内チェックの開始時間
        self.Score = 0

        self.HitRedtX = 0
        self.HitRectY = 0
        self.HitPoint = 0

#  ------------------------------------------
def CheckScreenIn(self):
    SafeArea = 10           # 画面外のチェックする幅
    if _DEBUG_ == True:
        SafeArea = -20       # Debug 画面内

    if -SafeArea < self.PosX and self.PosX < WINDOW_W + SafeArea:
        if -SafeArea < self.PosY and self.PosY < WINDOW_H + SafeArea:
            return True
    return False

#  ------------------------------------------
def GetPl(self):
    if len(Pl) > 0:
        return Pl[0]
    
    return 0
    
