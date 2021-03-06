import pyxel
import random
import math
import imp
import player
import enemy
import effect
import plitem
import enemy_set
import star

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
    # スターシーン
    imp.StarScnene = None

    # 初期化---------------------------------------
    def __init__(self):
#        pyxel.init(imp.WINDOW_W, imp.WINDOW_H, caption="Pyxel Shooting", scale=3, fps=60)
        pyxel.init(imp.WINDOW_W, imp.WINDOW_H, caption="Pyxel Shooting", scale=3, fps=60, palette=[0x000000, 0xc8cbd2, 0x000000, 0xa7a5a2, 0xe057cd, 0x335793, 0x099c9e, 0xffffff, 0xef337b, 0x1f2856, 0x000000, 0xffff00, 0x000000, 0x000000, 0x000000, 0x000000])
        pyxel.load("assets/my_resource.pyxres")

        pyxel.image(0).load(0, 0, "assets/img0.png")

        # メインScene タイトル　セット
        self.SetSubScene(SceneTitle())

        imp.StarScene = star.Star()
        
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

        # スター
        imp.StarScene.update()

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

            if imp._DEBUG_ == True:
                sc = imp.MainScene.__class__.__name__
                pyxel.text(0, 1, sc, 7)

        # サブシーン
        if imp.SubScene != None:
            imp.SubScene.draw()

            if imp._DEBUG_ == True:
                sc = imp.SubScene.__class__.__name__
                pyxel.text(0, 9, sc, 7)


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

    SelectPos = 0

    # 初期化---------------------------------------
    def __init__(self):
        imp.Game_Status = imp.GAME_STATUS_TITLE    # タイトルに戻る

        self.SelectPos = 0
        imp.StageNo = 1

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
        # タイトル画面
        # 上移動(上カーソルキー)
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD_1_UP):
            if self.SelectPos > 0:
                self.SelectPos -= 1

        # 下移動(下カーソルキー)
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD_1_DOWN):
            if self.SelectPos == 0:
                self.SelectPos += 1

        # 右移動(右カーソルキー) UP
        if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD_1_RIGHT):
            if imp.StageNo < imp.STAGE_NO_MAX:
                imp.StageNo += 1

        # 左移動(左カーソルキー) DOWN
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD_1_LEFT):
            if imp.StageNo > 1:
                imp.StageNo -= 1

        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD_1_A) or pyxel.btn(pyxel.GAMEPAD_1_B):
            if self.SelectPos == 1:
                imp.StageNo += 10               # テストステージは+10

            
            # メインシーン ゲームメイン セット
            imp.Score = 0         # スコア
            imp.PlItemNum = 0     # アイテム取得数
            imp.PlLevel = 0       # レベル
            imp.PlLevelUpEff = 0

            App.SetMainScene(self,SceneGameMain())

            # サブシーン Start セット
            App.SetSubScene(self,SceneStart())
        
    def draw(self):
        # タイトル画面
        pyxel.bltm(0, 0, 0, 8 * 9, 0, 32, 30)

#        ti = "TITLE"
#        pyxel.text(100, 100, ti, 7)

        st = ">"
        pyxel.text(100-10, 180 + (self.SelectPos * 10), st, 7)

        st = " START"
        pyxel.text(100, 180, st, 7)
        test = " TEST"
        pyxel.text(100, 190, test, 7)

        # ステージNoの表示
        no = "{:02}".format(imp.StageNo)
        pyxel.text(180, 180, no, 7)

# ==================================================
# Scene ゲームメイン
class SceneGameMain:

    Stage_Pos = 0

    # 初期化---------------------------------------
    def __init__(self):

        imp.Game_Status = imp.GAME_STATUS_MAIN

        # 敵セットのテーブル
        if imp.StageNo < 10:
            if imp.StageNo == 1:
                imp.StageSetTbl = enemy_set.STAGE_SET_1
            elif imp.StageNo == 2:
                imp.StageSetTbl = enemy_set.STAGE_SET_2
            elif imp.StageNo == 3:
                imp.StageSetTbl = enemy_set.STAGE_SET_3
            else:
                imp.StageSetTbl = enemy_set.STAGE_SET_4
        else:
            imp.StageSetTbl = enemy_set.STAGE_SET_TEST

        self.Stage_Pos = 0              # ステージ

        # プレイヤーのセット
        imp.Pl.append(player.Player(30, 40, 0, 100, 0))

        imp.TilePosX = 0
        imp.TilePosY = -256 * (8 - 1)

    def __del__(self):
        # 全てのオブジェクトを消す
        self.DeathAllObject()

    # メイン---------------------------------------
    def update(self):
        # ゲームオーバーになったらスクロール(敵セット)止める
        if imp.Game_Status == imp.GAME_STATUS_MAIN:
            self.Stage_Pos += 1

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
                        # サブシーン ゲームオーバー セット
                        App.SetSubScene(self,SceneGameOver())

        # ボスが死んだらステージクリアへ
        if imp.Game_Status == imp.GAME_STATUS_MAIN:       # ゲーム中のみ
            for e in imp.Em:
                if e.__class__.__name__ == "EnemyBoss":
                    if e.Death == 1:

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

        # スター
        imp.StarScene.draw()

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
            sc = "{:5}".format(imp.Score)
            pyxel.text(220, 230, sc, 7)

            # ゲージ
            for p in imp.Pl:
                if p.ObjType == imp.OBJPL:
                    # Itemゲージ
                    if imp.PlLevelUpEff == 0:
                        for n in range(imp.PL_ITEM_LEVEL_UP):
                            if n >= imp.PlItemNum:
                                pyxel.blt(((imp.WINDOW_W / 2) - ((imp.PL_ITEM_LEVEL_UP / 2) * 8)) + 8 * n, imp.WINDOW_H - 12, 0, 8 * 6, 8 * 1, 8, 8, 0)  # 空
                            else:
                                pyxel.blt(((imp.WINDOW_W / 2) - ((imp.PL_ITEM_LEVEL_UP / 2) * 8)) + 8 * n, imp.WINDOW_H - 12, 0, 8 * 6, 8 * 2, 8, 8, 0)  # とった分
                    else:
        # ステージの位置から敵をセットする
                    # 点滅
                        imp.PlLevelUpEff -= 1
                        if pyxel.frame_count & 0x02:
                            for n in range(imp.PL_ITEM_LEVEL_UP):
                                pyxel.blt(((imp.WINDOW_W / 2) - ((imp.PL_ITEM_LEVEL_UP / 2) * 8)) + 8 * n, imp.WINDOW_H - 12, 0, 8 * 6, 8 * 2, 8, 8, 0)  # とった分

                    # Lifeゲージ
                    for n in range(3):
                        if n >= p.Life:
                            pyxel.blt(10 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 7, 8 * 1, 8, 8, 0)  # 空
                        else:
                            pyxel.blt(10 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 7, 8 * 2, 8, 8, 0)  # とった分
            # スクロールPos
            if imp._DEBUG_ == True:
                pos = "{:5}".format(self.Stage_Pos)
                pyxel.text(220, 200, pos, 7)


    #  ------------------------------------------
    def SetStageEnemy(self):
        l = len(imp.StageSetTbl)                # ステージTbl数
        n = 0                                   # 頭からの順番
        pos = 0

        while l > 0:
            e = imp.StageSetTbl[n]
            pos += e[0]
            if self.Stage_Pos == pos:          # 等しい時のみ敵セットする
                while self.Stage_Pos == pos:   # 同じPosを繰り返しセット
                    t = e[3]
                    imp.Em.append(t(e[1], e[2], e[4], e[5], e[6]))

                    n += 1                      # 次のTblへ
                    e = imp.StageSetTbl[n]
                    pos += e[0]
                break
            l -= 1                              # 次のTblへ
            n += 1

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
            imp.PlItemNum += 1          # 1個とる
            return True                 # 当たり

        return False                    # 外れ

    #  ------------------------------------------
    def DeathAllObject(self):
        # プレイヤー・プレイヤーの弾を消す
        imp.Pl.clear()

        # 敵を消す
        imp.Em.clear()

        # エフェクトを消す
        imp.Eff.clear()

        # アイテムを消す
        imp.Itm.clear()

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
        imp.Game_Status = imp.GAME_STATUS_GAMEOVER       # ゲームオーバー

        self.PosX = 128 - (8 * 4) - 4
        self.PosY = 100
        self.WaitTime = 60 * 5

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
        self.WaitTime -= 1
        if self.WaitTime <= 0:
            # メイン ゲームシーンのデリート
            App.SetMainScene(self,None)
            # サブScene タイトル　セット
            App.SetSubScene(self,SceneTitle())
        
    def draw(self):
        # GAME OVER
        pyxel.blt(self.PosX,      self.PosY, 0, 0,    8*18, 8*4, 16, 0)
        pyxel.blt(self.PosX + 40, self.PosY, 0, 8*4,  8*18, 8*4, 16, 0)

# ==================================================
# Scene ゲームクリアー
class SceneGameClear:
    # 初期化---------------------------------------
    def __init__(self):
        imp.Game_Status = imp.GAME_STATUS_STAGECLEAR       # ステージクリア

        self.PosX = 128 - (8 * 2.5)
        self.PosY = 100
        self.WaitTime = 60 * 5

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
        self.WaitTime -= 1
        if self.WaitTime <= 0:
            # メイン ゲームシーンのデリート
            App.SetMainScene(self,None)
            # サブScene タイトル　セット
            App.SetSubScene(self,SceneNextStage())
        
    def draw(self):
        # STAGE CLEAR
        pyxel.blt(self.PosX - (8 * 2.5),      self.PosY, 0, 8*9,  8*18, 8*5, 16, 0)

# ==================================================
# Scene 次のステージへ送る
class SceneNextStage:
    # 初期化---------------------------------------
    def __init__(self):
        imp.Game_Status = imp.GAME_STATUS_NEXTSTAGE       # 次のステージ

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
            # メインシーン ゲームメイン セット
            imp.StageNo += 1
            if imp.StageNo > imp.STAGE_NO_MAX:
                # メイン ゲームシーンのデリート
                App.SetMainScene(self,None)
                # サブシーン Start セット
                App.SetSubScene(self,SceneTitle())
            else:
                # 次のステージ
                App.SetMainScene(self,SceneGameMain())

                # サブシーン Start セット
                App.SetSubScene(self,SceneStart())

    def draw(self):
        pass


App()

# ==================================================
