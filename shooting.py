import pyxel
import random
import math
import imp
import player
import enemy
import effect
import plitem

# --------------------------------------------------
# 敵のセット位置
STAGE_EM_POS = [            # 時間, X, Y, id0, id1, item

#    [ 100,  128-40,   0,  enemy.EnemyWide,  0, 1,],    # 撃ってもどる
#    [ 150,  128-40,   0,  enemy.EnemyWide,  0, 1,],    # 撃ってもどる
#    [ 200,  128-40,   0,  enemy.EnemyWide,  0, 1,],    # 撃ってもどる

#    [ 400,  128-00,   0,  enemy.EnemyWide,  1, 1,],    # 3Way撃って戻る

#    [ 500,  128-00,   0,  enemy.EnemyWide,  2, 1,],    # 全方向撃って戻る

#    [ 600,  128-60,   0,  enemy.EnemyWide,  3, 0,],    # まっすぐ

#    [ 700,  128-20,   0,  enemy.EnemyNorm,  0, 0,],    # カーブ

#    [1000,  128-20,   0,  enemy.EnemyBoss,  0, 0,],    # ボス


# 敵のセット位置
#STAGE_EM_POS = [            # 時間, X, Y, id0, id1, item


#    [ 100, 128,   0, EMBOSS,  0, 0,],   # Boss

    [ 150,  128-40,   0,  enemy.EnemyWide,  0, 1,],    # 撃ってもどる

    [ 200,  128-60,   0,  enemy.EnemyWide,  0, 0,],    # まっすぐ
    [ 240,  128-60,   0,  enemy.EnemyWide,  0, 0,],
    [ 280,  128-60,   0,  enemy.EnemyWide,  0, 1,],

    [ 500,  128+60,   0,  enemy.EnemyWide,  0, 0,],
    [ 540,  128+60,   0,  enemy.EnemyWide,  0, 0,],
    [ 580,  128+60,   0,  enemy.EnemyWide,  0, 1,],

    [ 760,  128-20,   0,  enemy.EnemyNorm,  0, 0,],    # カーブ
    [ 780,  128-40,   0,  enemy.EnemyNorm,  0, 0,],
    [ 800,  128-60,   0,  enemy.EnemyNorm,  0, 1,],

    [1000,  128+20,   0,  enemy.EnemyNorm,  0, 0,],
    [1020,  128+40,   0,  enemy.EnemyNorm,  0, 0,],
    [1040,  128+60,   0,  enemy.EnemyNorm,  0, 1,],

    [1300,  128-40,   0,  enemy.EnemyNorm,  0, 0,],    # カーブ
    [1340,  128-60,   0,  enemy.EnemyNorm,  0, 0,],
    [1380,  128-80,   0,  enemy.EnemyNorm,  0, 1,],

    [1600,  128+40,   0,  enemy.EnemyNorm,  0, 1,],
    [1640,  128+60,   0,  enemy.EnemyNorm,  0, 1,],
    [1680,  128+80,   0,  enemy.EnemyNorm,  0, 1,],

    [1750,  128-40,   0,  enemy.EnemyWide,  0, 1,],    # 撃ってもどる
    [1800,  128+40,   0,  enemy.EnemyWide,  0, 1,],

    [1900,  128-00,   0,  enemy.EnemyWide,  2, 1,],    # 全方向撃って戻る
    [2300,  128-40,   0,  enemy.EnemyWide,  2, 1,],    # 全方向撃って戻る
    [2700,  128+40,   0,  enemy.EnemyWide,  2, 1,],    # 全方向撃って戻る

    [3500,  128,      0,  enemy.EnemyBoss,  0, 0,],    # Boss

]

# ==================================================
class App:

    # ゲームの状態
    imp.Game_Status = imp.GAME_STATUS_TITLE

    imp.TilePosX = 0
    imp.TilePosY = -256 * (8 - 1)

    # メインシーン
    imp.MainScnene = None
    # サブシーン
    imp.SubScnene = None

    # 初期化---------------------------------------
    def __init__(self):
        pyxel.init(imp.WINDOW_W, imp.WINDOW_H, caption="Pyxel Shooting", scale=3, fps=60)
        pyxel.load("assets/my_resource.pyxres")

        # メインScene タイトル　セット
        self.SetSubScene(SceneTitle())

        pyxel.run(self.update, self.draw)

    # メイン---------------------------------------
    def update(self):
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # メインシーン
        if imp.MainScene != None:
            imp.MainScene.update()

        # サブシーン
        if imp.SubScene != None:
            imp.SubScene.update()

#                    print(n)

#            no = 0                  # リストの何番目かを数える
#            for n in App.EmBullet:
#                no += 1
#                if n.Death != 0:
#                    del App.EmBullet[no - 1]        # リストから削除する




    # 画面描画
    def draw(self):
        # 画面クリア
        pyxel.cls(13)

        # メインシーン
        if imp.MainScene != None:
            imp.MainScene.draw()

        # サブシーン
        if imp.SubScene != None:
            imp.SubScene.draw()

#  ------------------------------------------
    def SetMainScene(self, mainscene):
        if imp.MainScene != None:
            del imp.MainScene
        imp.MainScene = mainscene

#  ------------------------------------------
    def SetSubScene(self, subscene):
        if imp.SubScene != None:
            del imp.SubScene
        imp.SubScene = subscene

# ==================================================
# Scene タイトル
class SceneTitle:

    # 初期化---------------------------------------
    def __init__(self):
        pass

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
        # タイトル画面
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD_1_A) or pyxel.btn(pyxel.GAMEPAD_1_B):
            imp.Game_Status = imp.GAME_STATUS_MAIN

            # メインシーン ゲームメイン セット
            App.SetMainScene(self,SceneGameMain())

            # サブシーン Start セット
            App.SetSubScene(self,SceneStart())
        
    def draw(self):
        # タイトル画面
        pyxel.bltm(0, 0, 0, 8 * 9, 0, 32, 30)

        st = "TITLE"
        pyxel.text(100, 100, st, 7)


# ==================================================
# Scene ゲームメイン
class SceneGameMain:

    GameOverTime = 0
    Stage_Pos = 0

    # 初期化---------------------------------------
    def __init__(self):
        imp.Pl.append(player.Player(30, 40, 0, 100, 0))

        self.Stage_Pos = 0              # ステージ
        imp.Score = 0                  # スコア
        self.GameOverTime = 0           # ゲームオーバーの表示時間
        imp.TilePosX = 0
        imp.TilePosY = -256 * (8 - 1)

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
        if imp.Game_Status == imp.GAME_STATUS_MAIN or imp.Game_Status == imp.GAME_STATUS_GAMEOVER or imp.Game_Status == imp.GAME_STATUS_STAGECLEAR:
            # ゲームオーバーになったらスクロール(敵セット)止める
            if imp.Game_Status == imp.GAME_STATUS_MAIN:
                self.Stage_Pos += 1
            else:
                self.GameOverTime += 1          # ゲームオーバーの表示時間
                if self.GameOverTime >= 60 * 5:
                    imp.Game_Status = imp.GAME_STATUS_TITLE    # タイトルに戻る
                    # 全てのオブジェクトを消す
                    self.DeathAllObject()

                    imp.MainScene = None

                    # サブScene タイトル　セット
                    App.SetSubScene(self,SceneTitle())

            self.SetStageEnemy()

            # プレイヤー
            for p in imp.Pl:
                if p.ObjType == imp.OBJPL:
                    p.update()
                    p.Hit = 0

            # プレイヤーの弾
            for p in imp.Pl:
                if p.ObjType == imp.OBJPLB:
                    p.update()
                    p.Hit = 0

            # 敵
            for e in imp.Em:
                if e.ObjType == imp.OBJEM:
                    e.update()
                    e.Hit = 0

            # 敵の弾
            for e in imp.Em:
                if e.ObjType == imp.OBJEMB:
                    e.update()
                    e.Hit = 0

            # エフェクト
            for n in imp.Eff:
                n.update()

            # アイテム
            for n in imp.Itm:
                n.update()
                n.Hit = 0

            # 当たり判定 ---------------------------------
            # プレイヤーの弾と敵
            for p in imp.Pl:
                if p.ObjType == imp.OBJPLB:
                    for embd in imp.Em:
                        if embd.ObjType == imp.OBJEM:
                            self.CheckColli(p, embd)

            # 敵の弾とプレイヤー
            for em in imp.Em:
                if em.ObjType == imp.OBJEMB:
                    for p in imp.Pl:
                        if p.ObjType == imp.OBJPL:
                            self.CheckColli(em, p)

            # 敵とプレイヤー
            for em in imp.Em:
                if em.ObjType == imp.OBJEM:
                    for p in imp.Pl:
                        if p.ObjType == imp.OBJPL:
                            self.CheckColliBody(em, p)

            # プレイヤーがアイテムをとる
            for p in imp.Pl:
                if p.ObjType == imp.OBJPL:
                    for i in imp.Itm:
                        self.CheckColliPlItm(p, i)

            # プレイヤーが死んだらゲームオーバーへ
            if imp.Game_Status != imp.GAME_STATUS_GAMEOVER:       # ゲームオーバーでないとき
                for p in imp.Pl:
                    if p.ObjType == imp.OBJPL:
                        if p.Death == 1:
                            imp.Game_Status = imp.GAME_STATUS_GAMEOVER       # ゲームオーバー

                            # サブシーン ゲームオーバー セット
                            App.SetSubScene(self,SceneGameOver())

            # ボスが死んだらステージクリアへ
            if imp.Game_Status == imp.GAME_STATUS_MAIN:       # ゲーム中のみ
                for e in imp.Em:
                    if e.__class__.__name__ == "EnemyBoss":
                        if e.Death == 1:
                            imp.Game_Status = imp.GAME_STATUS_STAGECLEAR       # ステージクリア

                            # サブシーン ゲームクリアー　セット
                            App.SetSubScene(self,SceneGameClear())

            # オブジェクトを消す ---------------------------------
            # プレイヤー・プレイヤーの弾を消す
            for n,p in enumerate(imp.Pl):
                if p.Death != 0:
                    del imp.Pl[n]     # リストから削除する

            # 敵を消す
            for n,e in enumerate(imp.Em):
                if e.Death != 0:
                    del imp.Em[n]        # リストから削除する

            # エフェクトを消す
            for n,e in enumerate(imp.Eff):
                if e.Death != 0:
                    del imp.Eff[n]        # リストから削除する

            # アイテムを消す
            for n,e in enumerate(imp.Itm):
                if e.Death != 0:
                    del imp.Itm[n]        # リストから削除する
        
    def draw(self):
        # タイル描画
        # ゲーム画面
        pyxel.bltm(imp.TilePosX - 64, imp.TilePosY, 0, 32-8, 0, 32+16, 1024)
        if imp.Game_Status == imp.GAME_STATUS_MAIN or imp.Game_Status == imp.GAME_STATUS_STAGECLEAR:
            imp.TilePosY += 0.1
            if imp.TilePosY > 0:
                imp.TilePosY = 0


        if imp.Game_Status == imp.GAME_STATUS_MAIN or imp.Game_Status == imp.GAME_STATUS_GAMEOVER or imp.Game_Status == imp.GAME_STATUS_STAGECLEAR:
            # プレイヤー
            for p in imp.Pl:
                if p.ObjType == imp.OBJPL:
                    p.draw()

            # プレイヤーの弾
            for p in imp.Pl:
                if p.ObjType == imp.OBJPLB:
                    p.draw()

            # 敵
            for e in imp.Em:
                if e.ObjType == imp.OBJEM:
                    e.draw()

            # 敵の弾
            for e in imp.Em:
                if e.ObjType == imp.OBJEMB:
                    e.draw()

            # エフェクト
            for n in imp.Eff:
                n.draw()

            # アイテム
            for n in imp.Itm:
                n.draw()

            # スコアの表示
            sc = "{:04}".format(imp.Score)
            pyxel.text(100, 10, sc, 7)

            # ゲージ
            for p in imp.Pl:
                if p.ObjType == imp.OBJPL:
                    # Itemゲージ
                    for n in range(5):
                        if n >= p.ItemNum:
                            pyxel.blt(100 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 6, 8 * 1, 8, 8, 0)  # 空
                        else:
                            pyxel.blt(100 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 6, 8 * 2, 8, 8, 0)  # とった分
                    # Lifeゲージ
                    for n in range(5):
                        if n >= p.Life:
                            pyxel.blt(10 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 7, 8 * 1, 8, 8, 0)  # 空
                        else:
                            pyxel.blt(10 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 7, 8 * 2, 8, 8, 0)  # とった分

    #  ------------------------------------------
    def SetStageEnemy(self):
        # ステージの位置から敵をセットする
        for n,e in enumerate(STAGE_EM_POS):
            if self.Stage_Pos == e[0]:

                t = e[3]
                imp.Em.append(t(e[1], e[2], e[3], e[4], e[5]))

    #  ------------------------------------------
    def CheckColli(self, plat, embd):       # plat 攻撃側　　embd ダメージ側
        if plat.HitSt == 0:
            if embd.HitSt == 0:
                xx = abs(plat.PosX - embd.PosX)
                yy = abs(plat.PosY - embd.PosY)

                rx = (plat.HitRectX / 2) + (embd.HitRectX / 2)
                ry = (plat.HitRectY / 2) + (embd.HitRectY / 2)

                if xx < rx and yy < ry:
                    plat.Death = 1          # 攻撃側は消える
                    # エフェクト
                    imp.Eff.append(effect.Effect(plat.PosX, plat.PosY, 0, 0, 0))

                    plat.Hit = 1
                    embd.Hit = 1
                    embd.Life -= plat.HitPoint      # ダメージ計算
                    if embd.Life <= 0:              # 0以下なら死ぬ
                        embd.Life = 0
                        if imp._DEBUG_ == True:
                            print("hit")
                        return True                 # 当たり

        return False                    # 外れ

    #  ------------------------------------------
    def CheckColliBody(self, at, bd):       # at 攻撃側　　bd ダメージ側
        if at.HitSt == 0:
            if bd.HitSt == 0:
                xx = abs(at.PosX - bd.PosX)
                yy = abs(at.PosY - bd.PosY)

                rx = (at.HitRectX / 2) + (bd.HitRectX / 2)
                ry = (at.HitRectY / 2) + (bd.HitRectY / 2)

                if xx < rx and yy < ry:
                    if at.__class__.__name__ != "EnemyBoss":    # ボス以外
                        at.Death = 1          # 攻撃側は消える
                    # エフェクト
                    imp.Eff.append(effect.Effect(at.PosX, at.PosY, 0, 0, 0))
                    if imp._DEBUG_ == True:
                        print("hit body:" + bd.__class__.__name__)

                    at.Hit = 1
                    bd.Hit = 1
                    bd.Life -= 1                  # ダメージ計算
                    if bd.Life <= 0:              # 0以下なら死ぬ
                        bd.Life = 0
                        return True                 # 当たり

        return False                    # 外れ

    #  ------------------------------------------
    def CheckColliPlItm(self, p, i):
        xx = abs(p.PosX - i.PosX)
        yy = abs(p.PosY - i.PosY)

        rx = p.HitRectX + i.HitRectX
        ry = p.HitRectY + i.HitRectY

        if xx < rx and yy < ry:
            i.Death = 1
            
            if imp._DEBUG_ == True:
                print("item")
            p.ItemNum += 1              # 1個とる
            return True                 # 当たり

        return False                    # 外れ

    #  ------------------------------------------
    def DeathAllObject(self):
        # プレイヤー・プレイヤーの弾を消す
        for p in imp.Pl:
            p.Death = 1

        # 敵・敵の弾を消す
        for e in imp.Em:
            e.Death = 1

        # エフェクトを消す
        for e in imp.Eff:
            e.Death = 1

        # アイテムを消す
        for e in imp.Itm:
            e.Death = 1


# ==================================================
# Scene スタート
class SceneStart:

    # 初期化---------------------------------------
    def __init__(self):
        self.WaitTime = 60 * 3

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
        self.WaitTime -= 1
        if self.WaitTime <= 0:
            imp.SubScene = None
        
    def draw(self):
        # タイトル画面
        st = "START"
        pyxel.text(100, 100, st, 7)

# ==================================================
# Scene ゲームオーバー
class SceneGameOver:

    # 初期化---------------------------------------
    def __init__(self):
        self.PosX = 128 - (8 * 4) - 4
        self.PosY = 100
        self.WaitTime = 60 * 5

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
        self.WaitTime -= 1
        if self.WaitTime <= 0:
            imp.SubScene = None
        
    def draw(self):
        # GAME OVER
        pyxel.blt(self.PosX,      self.PosY, 0, 0,    8*18, 8*4, 16, 0)
        pyxel.blt(self.PosX + 40, self.PosY, 0, 8*4,  8*18, 8*4, 16, 0)

# ==================================================
# Scene ゲームクリアー
class SceneGameClear:
    # 初期化---------------------------------------
    def __init__(self):
        self.PosX = 128 - (8 * 4) - 4
        self.PosY = 100
        self.WaitTime = 60 * 5

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
        self.WaitTime -= 1
        if self.WaitTime <= 0:
            imp.SubScene = None
        
    def draw(self):
        # STAGE CLEAR
        pyxel.blt(self.PosX - (8 * 4),      self.PosY, 0, 8*8,  8*18, 8*8, 16, 0)

# ==================================================

App()

# ==================================================
