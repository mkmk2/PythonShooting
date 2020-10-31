import pyxel
import random
import math
import imp
import random
import shooting_sub
import effect

PL_SPEED = 1.2

PLST_DEMO = 0
PLST_PLAY = 1
PLST_DAMAGE = 2
PLST_DEATH = 3
PLST_CLEAR = 4


# --------------------------------------------------
# プレイヤークラス
class Player(imp.Sprite):

    ShotTime = 0
    ItemNum = 0     # アイテム取得数
    Level = 0

    # コンストラクタ
    def __init__(self, x, y, id0, id1, item):
        imp.Sprite.__init__(self, x, y, id0, id1, item)       # Spriteクラスのコンストラクタ

        self.PlDir = 0              # 上下のパターン切り替え
        self.PlSt0 = PLST_DEMO      # st0

        self.PosX = 128
        self.PosY = 250
        self.PosAdjX = -4
        self.PosAdjY = -8

        self.Life = 5
        self.HitRectX = 2
        self.HitRectY = 2

    # メイン
    def PlayerMove(self):

        self.HitSt = 0                  # 当たりアリ

        if self.PlSt0 == 0:             # デモ
            self.PosY -= 2
            if self.PosY < 200:
                self.PlSt0 = PLST_PLAY

        elif self.PlSt0 == 1:           # ゲームプレイ中

            if imp.Game_Status == imp.GAME_STATUS_MAIN:     # ゲーム中のみ死にチェック
                if self.Life <= 0:          # 0以下なら死ぬ
                    self.PlSt0 = PLST_DEATH # 死に
                    self.MvWait = 10        # 爆発数
                    self.MvTime = 0         # 爆発タイマー

                if self.Hit != 0:           # 何かにあたった
                    self.PlSt0 = PLST_DAMAGE  # ダメージ
                    self.PtnNo = 0
                    self.MvWait = 0
                    self.MvTime = 40

            if imp.Game_Status == imp.GAME_STATUS_STAGECLEAR:    # ステージクリア
                self.PlSt0 = PLST_CLEAR     # クリア
                self.PlDir = 0                       # 前

            else:
                # プレイヤー移動
                self.PlayerLeverMove()

                # 弾セット(スペースキー)
                if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD_1_A) or pyxel.btn(pyxel.GAMEPAD_1_B):
                    self.ShotTime -= 1
                    if self.ShotTime < 0:
                        self.ShotTime = 5
                        if self.Level == 0:
                            imp.PlBullet.append(PlayerBullet(self.PosX, self.PosY, 0, 0, 0))
                        elif self.Level == 1:
                            imp.PlBullet.append(PlayerBullet(self.PosX - 5, self.PosY, 0, 0, 0))
                            imp.PlBullet.append(PlayerBullet(self.PosX + 5, self.PosY, 0, 0, 0))
                        else:
                            imp.PlBullet.append(PlayerBullet(self.PosX - 6, self.PosY, 1, 0, 0))  # 左側
                            imp.PlBullet.append(PlayerBullet(self.PosX, self.PosY, 0, 0, 0))
                            imp.PlBullet.append(PlayerBullet(self.PosX + 6, self.PosY, 2, 0, 0))  # 右側

                else:
                    self.ShotTime = 0

                if self.ItemNum >= 5:
                    self.ItemNum = 0
                    self.Level += 1

        elif self.PlSt0 == PLST_DAMAGE:           # ダメージ
            self.HitSt = 1                          # 当たりナシ
            # プレイヤー移動
            cpDir = self.PlDir       # PlDirの保存・・・
            self.PlayerLeverMove()
            self.PlDir = cpDir

            self.MvWait -= 1
            if self.MvWait <= 0:
                self.MvWait = 6
                if self.PtnNo == 0:
                    self.PlDir = 0                   # 前
                    self.PtnNo = 1
                elif self.PtnNo == 1:
                    self.PlDir = 1                   # 左
                    self.PtnNo = 2
                elif self.PtnNo == 2:
                    self.PlDir = 2                   # 右
                    self.PtnNo = 3
                elif self.PtnNo == 3:
                    self.PlDir = 1                   # 左
                    self.PtnNo = 0

            self.MvTime -= 1
            if self.MvTime <= 0:
                self.PlSt0 = PLST_PLAY


        elif self.PlSt0 == PLST_DEATH:           # 死に
            # 爆発
            self.MvTime -= 1
            if self.MvTime <= 0:
                imp.Eff.append(effect.Effect(self.PosX - 10 + random.randrange(0, 20, 1), self.PosY - 10 + random.randrange(0, 20, 1), imp.EFF_BOOM, 0, 0))
                imp.Eff.append(effect.Effect(self.PosX - 10 + random.randrange(0, 20, 1), self.PosY - 10 + random.randrange(0, 20, 1), imp.EFF_BOOM, 0, 0))
                self.MvTime = 4
                self.Display = self.MvWait & 1      # 点滅
                self.MvWait -= 1
                if self.MvWait <= 0:
                    self.Death = 1          # 死ぬ
                    print("pl die")

        elif self.PlSt0 == PLST_CLEAR:           # クリア
            if self.PosY > -100:
                self.PosY -= 2


    # 描画
    def Draw(self):
        x = self.PosX + self.PosAdjX
        y = self.PosY + self.PosAdjY
        
        if self.PlDir == 0:
            pyxel.blt(x, y, 0, 0, 0, 8 ,16, 0)       # 前
        elif self.PlDir == 1:
            pyxel.blt(x, y, 0, 8, 0, 8 ,16, 0)       # 左
        else:
            pyxel.blt(x, y, 0, 16, 0, 8 ,16, 0)      # 右

        # 中心の表示
        shooting_sub.DebugDrawPosHitRect(self)

# --------------------------------------------------
    # プレイヤー移動
    def PlayerLeverMove(self):
        # プレイヤー移動
        self.PlDir = 0                       # 前
        # 上移動(上カーソルキー)
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            self.PosY -= PL_SPEED
            if self.PosY < 50:
                self.PosY = 50

        # 下移動(下カーソルキー)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
            self.PosY += PL_SPEED
            if self.PosY > imp.WINDOW_H - 16:
                self.PosY = imp.WINDOW_H - 16

        # 右移動(右カーソルキー)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.PosX += PL_SPEED
            self.PlDir = 2                   # 右
            if self.PosX > imp.WINDOW_W - 8:
                self.PosX = imp.WINDOW_W - 8

        # 左移動(左カーソルキー)
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.PosX -= PL_SPEED
            self.PlDir = 1                   # 左
            if self.PosX < 8:
                self.PosX = 8

        scX = self.PosX - 128
        imp.TilePosX = -scX / 10

# --------------------------------------------------
# プレイヤークラス
class PlayerBullet(imp.Sprite):

    # コンストラクタ
    def __init__(self, x, y, id0, id1, item):
        imp.Sprite.__init__(self, x, y, id0, id1, item)       # Spriteクラスのコンストラクタ

        self.PosAdjX = -1
        self.PosAdjY = -2
        self.Life = 1
        self.HitPoint = 1
        self.HitRectX = 1
        self.HitRectY = 5

        if self.Id0 == 0:   # 前
            self.VectorX = 0
            self.VectorY = -3.5
        if self.Id0 == 1:   # 左側
            self.VectorX = -0.25
            self.VectorY = -3.5
        if self.Id0 == 2:   # 右側
            self.VectorX =  0.25
            self.VectorY = -3.5

    # メイン
    def PlayerBulletMove(self):
        self.PosX += self.VectorX
        self.PosY += self.VectorY

        # 画面内チェック
        imp.CheckScreenIn(self)

    # 描画
    def Draw(self):
        x = self.PosX + self.PosAdjX
        y = self.PosY + self.PosAdjY
        pyxel.blt(x, y, 0, 32, 0, 2 ,4, 0)

        # 中心の表示
        shooting_sub.DebugDrawPosHitRect(self)

