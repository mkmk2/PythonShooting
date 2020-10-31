
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

SCREEN_TIME = 100           # 画面外にセットされたあとに画面内判定を開始するまでの時間

EM0 = 0
EM1 = 1
EM2 = 2
EMBOSS = 10

# エフェクトId
EFF_BOOM = 0
EFF_BOOM_MOVE = 1
EFF_GAMEOVER = 4
EFF_CLEAR = 5


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

        self.HitSt = 0                  # 1:当たりナシ
        self.HitRedtX = 0
        self.HitRectY = 0
        self.HitPoint = 0
        self.Hit = 0                    # 1:何かに当たった

#  ------------------------------------------
# 画面内チェック
def CheckScreenIn(self):
    if self.ScreenTime >= SCREEN_TIME:
        SafeArea = 10           # 画面外のチェックする幅
        if _DEBUG_ == True:
            SafeArea = -20       # Debug 画面の中で判定する

        if -SafeArea < self.PosX and self.PosX < WINDOW_W + SafeArea:
            if -SafeArea < self.PosY and self.PosY < WINDOW_H + SafeArea:
                return True     # 画面内

        self.Death = 1          # 消す
        print("out")
        return False            # 画面外

    else:
        self.ScreenTime += 1
    return True     # 画面内

#  ------------------------------------------
def GetPl(self):
    if len(Pl) > 0:
        return Pl[0]
    
    return 0
    
