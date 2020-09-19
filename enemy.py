import pyxel
import random
import math
import imp
import random
import shooting_sub
import plitem
import effect

EMBOSS_ENTER = 0    # 登場
EMBOSS_AT_BO = 1    # BOSS連射
EMBOSS_MOVE = 2     # 移動
EMBOSS_RETURN = 3   # 帰る
EMBOSS_BOMB = 4     # 爆発

# Id0
# 0: まっすぐ下に降りてきて画面真ん中あたりで
#     Id1:0 弾撃って引き返す
#     Id1:1 止まって3Wayx10
# 1: まっすぐ下に降りてきてプレイヤーに向かってカーブ、画面真ん中あたりで弾撃つ
# 2: まっすぐ下に移動するだけ

# 敵のセット位置
BOSS_MOVE_TBL = [          # X, Y, Time, Wait
    [ 100,   90,   60*3,  60*1,],
    [ 200,   80,   60*2,  60*1,],
    [ 150,  100,   60*1,  60*1,],
    [ 180,   80,   60*2,  60*1,],
    [   0,    0,   60*3,    -1,],   # 攻撃
    [  60,  150,   60*1,  60*1,],
    [  40,   40,   60*2,  60*1,],
    [ 100,   50,   60*1,  60*1,],
    [  60,  100,   60*1,  60*1,],
    [ 200,   50,   60*1,  60*1,],
    [ 100,   50,   60*1,  60*1,],
    [  60,  100,   60*1,  60*1,],
    [ 200,   50,   60*1,  60*1,],
    [   0,    0,     -1,     0,],   # 終わり
]

# --------------------------------------------------
# 敵クラス
class Enemy(imp.Sprite):

    BulletTime = 0

    MvTargetPosX = 0
    MvTargetPosY = 0
    MvTime = 0
    MvWait = 0
    BossMoveTblPtr = 0

    # コンストラクタ
    def __init__(self, x, y, id0, id1):
        imp.Sprite.__init__(self, x, y, id0, id1)       # Spriteクラスのコンストラクタ

        if self.Id0 == imp.EM0:
            self.PosAdjX = -8
            self.PosAdjY = -4
            self.HitPoint = 1
            self.HitRectX = 14
            self.HitRectY = 6
            if self.Id1 == 0:
                self.Life = 4
            elif self.Id1 == 1:
                self.Life = 10          # 撃って戻る
            elif self.Id1 == 2:
                self.Life = 40          # 全方向撃って戻る

        elif self.Id0 == imp.EM1:       # カーブ
            self.PosAdjX = -4
            self.PosAdjY = -4
            self.Life = 2
            self.HitPoint = 1
            self.HitRectX = 8
            self.HitRectY = 8
            self.Score = 10

            self.BulletTime = random.randrange(40, 60, 1)

        elif self.Id0 == imp.EM2:       # まっすぐ
            self.PosAdjX = -8
            self.PosAdjY = -4
            self.Life = 4
            self.HitPoint = 10
            self.HitRectX = 14
            self.HitRectY = 12
            self.Score = 10

        elif self.Id0 == imp.EMBOSS:
            self.PosAdjX = -8*3
            self.PosAdjY = -8*2
            self.Life = 600
            self.HitPoint = 1
            self.HitRectX = 48
            self.HitRectY = 16
            self.Score = 1000

    # メイン
    def EnemyMove(self):
        if self.Id0 == imp.EM0:     # -----------------------------------------------
        # id0 0
            if self.Id1 == 0:     # -----------------------------------------------
                # 止まって弾撃って引き返す
                if self.St0 == 0:
                    self.PosY += 1.5
                    if self.PosY > 130:
                        imp.EmBullet.append(EnemyBullet(self.PosX,self.PosY,0,0))
                        self.St0 = 1
                else:
                    self.PosY -= 1.5
            elif self.Id1 == 1:
                #止まって3Way
                if self.St0 == 0:
                    self.PosY += 1.5
                    if self.PosY > 130:
                        self.BulletTime = 0
                        self.MvWait = 0
                        self.St0 = 1

                elif self.St0 == 1:
                    self.MvWait -= 1
                    if self.MvWait < 0:
                        self.MvWait = 30

                        imp.EmBullet.append(EnemyBullet(self.PosX,self.PosY,1,7))
                        imp.EmBullet.append(EnemyBullet(self.PosX,self.PosY,1,8))
                        imp.EmBullet.append(EnemyBullet(self.PosX,self.PosY,1,9))

                        self.BulletTime += 1
                        if self.BulletTime >= 10:
                            self.St0 = 2

                    self.PosY -= 0.1

                else:
                    self.PosY -= 0.6

            elif self.Id1 == 2:
                # 全方向撃って戻る
                if self.St0 == 0:
                    self.PosY += 1.5
                    if self.PosY > 80:
                        self.BulletTime = 0
                        self.MvWait = 0
                        self.St0 = 1

                if self.St0 == 1:
                    self.MvWait -= 1
                    if self.MvWait < 0:
                        self.MvWait = 60
                        for n in range(32):
                            imp.EmBullet.append(EnemyBullet(self.PosX,self.PosY,1,n))

                        self.BulletTime += 1
                        if self.BulletTime >= 8:
                            self.St0 = 2

                if self.St0 == 2:
                    self.PosY -= 0.8

        elif self.Id0 == imp.EM1:     # -----------------------------------------------
        # id0 1
            if self.St0 == 0:
                self.PosY += 1.2
                if self.PosY > 40:
                    pl = imp.GetPl(self)
                    if self.PosX < pl.PosX:
                        self.VectorX += 0.015
                        self.St1 = 1    # 右回転
                    else:
                        self.VectorX -= 0.015
                        self.St1 = 2    # 左回転

            self.PosX += self.VectorX

            self.BulletTime -= 1
            if self.BulletTime <= 0:
                self.BulletTime = random.randrange(10, 20, 1)

        elif self.Id0 == imp.EM2:     # -----------------------------------------------
        # id0 2
            self.PosY += 1.0

        elif self.Id0 == imp.EMBOSS:     # -----------------------------------------------BOSS
        # id0 10 Boss

            if self.St0 == EMBOSS_ENTER:
                self.PosY += 1.5
                if self.PosY > 60:
                    self.St0 = 1

                    self.BulletTime = 0
                    self.St1 = 5

            elif self.St0 == EMBOSS_AT_BO:
                self.BulletTime -= 1
                if self.BulletTime < 0:
                    self.BulletTime = 15
                    if (self.St1 & 1) == 0:
                        imp.EmBullet.append(EnemyBullet(self.PosX - 8,self.PosY,3,0))
                    else:
                        imp.EmBullet.append(EnemyBullet(self.PosX + 8,self.PosY,3,0))

                    self.St1 -= 1
                    if self.St1 <= 0:
                        self.St0 = 2
                        self.St1 = 0

                        self.BossMoveTbl = 0

            elif self.St0 == EMBOSS_MOVE:
                if self.St1 == 0:
                    self.MvTargetPosX = BOSS_MOVE_TBL[self.BossMoveTblPtr][0]
                    self.MvTargetPosY = BOSS_MOVE_TBL[self.BossMoveTblPtr][1]
                    self.MvTime = BOSS_MOVE_TBL[self.BossMoveTblPtr][2]
                    self.MvWait = BOSS_MOVE_TBL[self.BossMoveTblPtr][3]

                    if self.MvWait != -1:
                        self.St1 = 1    # 移動
                    else:
                        self.St1 = 2    # 攻撃
                        self.BulletTime = 0
                        self.MvWait = 5

                elif  self.St1 == 1:
                    # 移動
                    xx = self.MvTargetPosX - self.PosX
                    xx = xx / self.MvTime
                    yy = self.MvTargetPosY - self.PosY
                    yy = yy / self.MvTime
                    self.PosX += xx
                    self.PosY += yy

                    self.MvTime -= 1
                    if self.MvTime <= 0:
                        self.St1 = 3
                        self.St2 = 0

                elif  self.St1 == 2:
                    # 攻撃
                    self.BulletTime -= 1
                    if self.BulletTime < 0:
                        self.BulletTime = 15
                        if (self.MvWait & 1) == 0:
                            imp.EmBullet.append(EnemyBullet(self.PosX - 8,self.PosY,3,0))
                        else:
                            imp.EmBullet.append(EnemyBullet(self.PosX + 8,self.PosY,3,0))

                        self.MvWait -= 1
                        if self.MvWait <= 0:
                            self.St1 = 3

                elif  self.St1 == 3:
                    if  self.St2 == 0:
                        # 全方向弾撃つ
                        for n in range(32):
                            imp.EmBullet.append(EnemyBullet(self.PosX,self.PosY,1,n))
                        self.St2 = 1
                    else:
                        # 待機
                        self.MvWait -= 1
                        if self.MvWait <= 0:
                            # 次のTbl
                            self.BossMoveTblPtr += 1
                            if BOSS_MOVE_TBL[self.BossMoveTblPtr][2] != -1:
                                self.St1 = 0        # 次のTbl
                            else:
                                self.St0 = 3        # 終わり

            elif self.St0 == EMBOSS_RETURN:
                # 帰る
                self.PosY -= 0.5

            elif self.St0 == EMBOSS_BOMB:
                # 爆発
                self.MvTime -= 1
                if self.MvTime <= 0:
                    imp.Eff.append(effect.Effect(self.PosX - 25 + random.randrange(0, 50, 1), self.PosY - 10 + random.randrange(0, 20, 1), 0, 0))
                    imp.Eff.append(effect.Effect(self.PosX - 25 + random.randrange(0, 50, 1), self.PosY - 10 + random.randrange(0, 20, 1), 0, 0))
                    imp.Eff.append(effect.Effect(self.PosX - 25 + random.randrange(0, 50, 1), self.PosY - 10 + random.randrange(0, 20, 1), 1, random.randrange(0, 31, 1)))
                    self.MvTime = 6
                    self.Display = self.MvWait & 1      # 点滅
                    self.MvWait -= 1
                    if self.MvWait <= 0:
                        self.Death = 1          # 死ぬ

            # Boss死にチェック
            if self.Life <= 0 and self.St0 != EMBOSS_BOMB:          # 0以下なら死ぬ
                self.St0 = EMBOSS_BOMB
                print("boss die")
                self.MvWait = 30       # 爆発数
                self.MvTime = 0         # 爆発タイマー

        # 死にチェック
        if self.Id0 != imp.EMBOSS:     # Boss以外は共通の死にチェック、Bossは自分でチェックして爆発とかする
            if self.Life <= 0:          # 0以下なら死ぬ
                self.Death = 1          # 死ぬ
                print("enemy die")
                imp.Itm.append(plitem.PlItem(self.PosX,self.PosY,0,0))

        # 画面内チェック
        self.ScreenTime += 1
        if self.ScreenTime >= imp.SCREEN_TIME:
            if imp.CheckScreenIn(self) == False:
                self.Death = 1
# -----------------------------------------------
    # 描画
    def Draw(self):
        x = self.PosX + self.PosAdjX
        y = self.PosY + self.PosAdjY

        if self.Id0 == imp.EM0:
        # Id 0
            if self.Id1 == 0:
                if self.St0 == 0:
                    pyxel.blt(x, y, 0, 0, 8*8 , 16, 8, 0)
                else:
                    pyxel.blt(x, y, 0, 0, 8*8 , 16,-8, 0)
            elif self.Id1 == 1:
                    pyxel.blt(x, y, 0, 0, 8*8 , 16, 8, 0)
            elif self.Id1 == 2:
                    pyxel.blt(x, y, 0, 0, 8*8 , 16, 8, 0)

        elif self.Id0 == imp.EM1:
        # Id 1
            if self.St1 == 0:
                pyxel.blt(x, y, 0, 8, 8*9 , 8, 8, 0)
            else:
                self.PtnTime -= 1
                if self.PtnTime <= 0:
                    self.PtnTime = 8

                    if self.St1 == 1:
                        self.PtnNo += 1
                        if self.PtnNo >= 7:
                            self.PtnNo = 0
                    else:
                        self.PtnNo -= 1
                        if self.PtnNo < 0:
                            self.PtnNo = 7

                pyxel.blt(x, y, 0, 8 * self.PtnNo, 8*9 , 8, 8, 0)

        elif self.Id0 == imp.EM2:
        # Id 2
            pyxel.blt(x, y, 0, 0, 8*8 , 16, 8, 0)

        elif self.Id0 == imp.EMBOSS:
        # Id10 Boss
            if self.Display != 0:
        #    pyxel.blt(x, y, 0, 0, 8*11 , 8*6, 8*4, 0)
                pyxel.blt(x,       y, 0, 0, 8*11 ,  8*3, 8*4, 0)
                pyxel.blt(x+(8*3), y, 0, 0, 8*11 , -8*3, 8*4, 0)

                # デバッグ用MovePos
                if imp._DEBUG_ == True and self.St0 == 2:
                    pyxel.rectb(self.MvTargetPosX-4, self.MvTargetPosY-4, 8, 8, 10)

        # 中心の表示
        shooting_sub.DebugDrawPosHitRect(self)

# --------------------------------------------------
# 敵の弾クラス
class EnemyBullet(imp.Sprite):

    st = 0

    # コンストラクタ
    def __init__(self, x, y, id0, id1):
        imp.Sprite.__init__(self, x, y, id0, id1)       # Spriteクラスのコンストラクタ

        self.Life = 1
        self.HitPoint = 1
        self.HitRectX = 2
        self.HitRectY = 2

        if self.Id0 == 0:           # 〇弾 狙って撃つ
            self.PosAdjX = -2
            self.PosAdjY = -2
        elif self.Id0 == 1:         # 線弾 指定の方向
            self.PosAdjX = -4
            self.PosAdjY = -4
        elif self.Id0 == 2:         # 〇弾 指定の方向
            self.PosAdjX = -2
            self.PosAdjY = -2
        elif self.Id0 == 3:         # ボス弾大 前
            self.PosAdjX = -4
            self.PosAdjY = -8
            self.VectorX = 0
            self.VectorY = 1.8

    # メイン
    def EnemyBulletMove(self):
        if self.Id0 == 0:           # 狙って撃つ
            if self.st == 0:
                self.Rot = shooting_sub.GetDirection(self, self.PosX, self.PosY, imp.Pl[0].PosX, imp.Pl[0].PosY)
                shooting_sub.SetVector(self, self.Rot, 1.5)
                self.st = 1
            else:
                self.PosX += self.VectorX
                self.PosY += self.VectorY
        
        elif self.Id0 == 1:         # 指定の方向
            if self.st == 0:
                self.Rot = math.radians(self.Id1 * (90/8))
                shooting_sub.SetVector(self, self.Rot, 0.6)
                self.st = 1
            else:
                self.PosX += self.VectorX
                self.PosY += self.VectorY

        elif self.Id0 == 2:         # 〇弾 指定の方向
            if self.st == 0:
                self.Rot = math.radians(self.Id1 * (90/8))
                shooting_sub.SetVector(self, self.Rot, 1.5)
                self.st = 1
            else:
                self.PosX += self.VectorX
                self.PosY += self.VectorY

        elif self.Id0 == 3:         # ボス弾大 前
            self.PosX += self.VectorX
            self.PosY += self.VectorY


        # 画面内チェック
        self.ScreenTime += 1
        if self.ScreenTime >= imp.SCREEN_TIME:
            if imp.CheckScreenIn(self) == False:
                self.Death = 1

    # 描画
    def Draw(self):
        x = self.PosX + self.PosAdjX
        y = self.PosY + self.PosAdjY
        if self.Id0 == 0:
            if pyxel.frame_count & 0x08:
                pyxel.blt(x, y, 0, 28, 0, 4, 4, 0)
            else:
                pyxel.blt(x, y, 0, 28, 0, 4, 4, 0)
        elif self.Id0 == 1:
            if self.Id1 == 0:
                pyxel.blt(x, y, 0, 8*0, 8*4, 8, 8, 0)
            elif self.Id1 == 1:
                pyxel.blt(x, y, 0, 8*1, 8*4, 8, 8, 0)
            elif self.Id1 == 2:
                pyxel.blt(x, y, 0, 8*2, 8*4, 8, 8, 0)
            elif self.Id1 == 3:
                pyxel.blt(x, y, 0, 8*3, 8*4, 8, 8, 0)
            elif self.Id1 == 4:
                pyxel.blt(x, y, 0, 8*4, 8*4, 8, 8, 0)
            elif self.Id1 == 5:
                pyxel.blt(x, y, 0, 8*5, 8*4, 8, 8, 0)
            elif self.Id1 == 6:
                pyxel.blt(x, y, 0, 8*6, 8*4, 8, 8, 0)
            elif self.Id1 == 7:
                pyxel.blt(x, y, 0, 8*7, 8*4, 8, 8, 0)
            elif self.Id1 == 8:
                pyxel.blt(x, y, 0, 8*8, 8*4, 8, 8, 0)
            elif self.Id1 == 9:
                pyxel.blt(x, y, 0, 8*7, 8*4, -8, 8, 0)
            elif self.Id1 == 10:
                pyxel.blt(x, y, 0, 8*6, 8*4, -8, 8, 0)
            elif self.Id1 == 11:
                pyxel.blt(x, y, 0, 8*5, 8*4, -8, 8, 0)
            elif self.Id1 == 12:
                pyxel.blt(x, y, 0, 8*4, 8*4, -8, 8, 0)
            elif self.Id1 == 13:
                pyxel.blt(x, y, 0, 8*3, 8*4, -8, 8, 0)
            elif self.Id1 == 14:
                pyxel.blt(x, y, 0, 8*2, 8*4, -8, 8, 0)
            elif self.Id1 == 15:
                pyxel.blt(x, y, 0, 8*1, 8*4, -8, 8, 0)
            elif self.Id1 == 16:
                pyxel.blt(x, y, 0, 8*0, 8*4, -8, -8, 0)
            elif self.Id1 == 17:
                pyxel.blt(x, y, 0, 8*1, 8*4, -8, -8, 0)
            elif self.Id1 == 18:
                pyxel.blt(x, y, 0, 8*2, 8*4, -8, -8, 0)
            elif self.Id1 == 19:
                pyxel.blt(x, y, 0, 8*3, 8*4, -8, -8, 0)
            elif self.Id1 == 20:
                pyxel.blt(x, y, 0, 8*4, 8*4, -8, -8, 0)
            elif self.Id1 == 21:
                pyxel.blt(x, y, 0, 8*5, 8*4, -8, -8, 0)
            elif self.Id1 == 22:
                pyxel.blt(x, y, 0, 8*6, 8*4, -8, -8, 0)
            elif self.Id1 == 23:
                pyxel.blt(x, y, 0, 8*7, 8*4, -8, -8, 0)
            elif self.Id1 == 24:
                pyxel.blt(x, y, 0, 8*8, 8*4, 8, -8, 0)
            elif self.Id1 == 25:
                pyxel.blt(x, y, 0, 8*7, 8*4, 8, -8, 0)
            elif self.Id1 == 26:
                pyxel.blt(x, y, 0, 8*6, 8*4, 8, -8, 0)
            elif self.Id1 == 27:
                pyxel.blt(x, y, 0, 8*5, 8*4, 8, -8, 0)
            elif self.Id1 == 28:
                pyxel.blt(x, y, 0, 8*4, 8*4, 8, -8, 0)
            elif self.Id1 == 29:
                pyxel.blt(x, y, 0, 8*3, 8*4, 8, -8, 0)
            elif self.Id1 == 30:
                pyxel.blt(x, y, 0, 8*2, 8*4, 8, -8, 0)
            elif self.Id1 == 31:
                pyxel.blt(x, y, 0, 8*1, 8*4, 8, -8, 0)
        elif self.Id0 == 2:
            if pyxel.frame_count & 0x08:
                pyxel.blt(x, y, 0, 28, 0, 4, 4, 0)
            else:
                pyxel.blt(x, y, 0, 28, 0, 4, 4, 0)
        elif self.Id0 == 3:
            if pyxel.frame_count & 0x04:
                pyxel.blt(x, y, 0, 0, 8*15, 8, 16, 0)
            else:
                pyxel.blt(x, y, 0, 8, 8*15, 8, 16, 0)

        # 中心の表示
        shooting_sub.DebugDrawPosHitRect(self)

# --------------------------------------------------
