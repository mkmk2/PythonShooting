import pyxel
import random
import math
import imp
import player
import enemy
import effect
import plitem

# --------------------------------------------------
# ==================================================
class App:

    # スコア
    Score = 0
    # ゲームの状態
    imp.Game_Status = imp.GAME_STATUS_TITLE
    GameOverTime = 0
    Stage_Pos = 0

    imp.TilePosX = 0
    imp.TilePosY = -256 * (8 - 1)


    # 初期化---------------------------------------
    def __init__(self):
        pyxel.init(imp.WINDOW_W, imp.WINDOW_H, caption="Pyxel Shooting", scale=3, fps=60)
        pyxel.load("assets/my_resource.pyxres")

        pyxel.run(self.update, self.draw)

    # メイン---------------------------------------
    def update(self):
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if imp.Game_Status == imp.GAME_STATUS_TITLE:
            # タイトル画面
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD_1_A) or pyxel.btn(pyxel.GAMEPAD_1_B):
                imp.Game_Status = imp.GAME_STATUS_MAIN

                imp.Pl.append(player.Player(30, 40, 0, 100, 0))

                self.Stage_Pos = 0              # ステージ
                self.Score = 0                  # スコア
                self.GameOverTime = 0           # ゲームオーバーの表示時間
                imp.TilePosX = 0
                imp.TilePosY = -256 * (8 - 1)

        elif imp.Game_Status == imp.GAME_STATUS_MAIN or imp.Game_Status == imp.GAME_STATUS_GAMEOVER or imp.Game_Status == imp.GAME_STATUS_STAGECLEAR:
            # ゲームオーバーになったらスクロール(敵セット)止める
            if imp.Game_Status == imp.GAME_STATUS_MAIN:
                self.Stage_Pos += 1
            else:
                self.GameOverTime += 1          # ゲームオーバーの表示時間
                if self.GameOverTime >= 60 * 5:
                    imp.Game_Status = imp.GAME_STATUS_TITLE    # タイトルに戻る
                    # 全てのオブジェクトを消す
                    self.DeathAllObject()

            if imp.Game_Status != imp.GAME_STATUS_TITLE:
                self.SetStageEnemy()

                # プレイヤー
                for n in imp.Pl:
                    n.PlayerMove()

                # 敵
                for n in imp.Em:
                    n.EnemyMove()

                # プレイヤーの弾
                for n in imp.PlBullet:
                    n.PlayerBulletMove()

                # 敵の弾
                for n in imp.EmBullet:
                    n.EnemyBulletMove()

                # エフェクト
                for n in imp.Eff:
                    n.EffectMove()

                # アイテム
                for n in imp.Itm:
                    n.PlItemMove()

                # 当たり判定 ---------------------------------
                # プレイヤーの弾と敵
                for plat in imp.PlBullet:
                    for embd in imp.Em:
                        self.CheckColli(plat, embd)

                # 敵の弾とプレイヤー
                for emb in imp.EmBullet:
                    for p in imp.Pl:
                        self.CheckColli(emb, p)

                # プレイヤーがアイテムをとる
                for p in imp.Pl:
                    for i in imp.Itm:
                        self.CheckColliPlItm(p, i)

                # プレイヤーが死んだらゲームオーバーへ
                if imp.Game_Status != imp.GAME_STATUS_GAMEOVER:       # ゲームオーバーでないとき
                    for p in imp.Pl:
                        if p.Death == 1:
                            imp.Game_Status = imp.GAME_STATUS_GAMEOVER       # ゲームオーバー

                            imp.Eff.append(effect.Effect(128 - (8 * 4) - 4, 100, 4, 0, 0))       # GameOver

                # ボスが死んだらステージクリアへ
                if imp.Game_Status == imp.GAME_STATUS_MAIN:       # ゲーム中のみ
                    for e in imp.Em:
                        if e.Id0 == imp.EMBOSS:
                            if e.Death == 1:
                                imp.Game_Status = imp.GAME_STATUS_STAGECLEAR       # ステージクリア

                                imp.Eff.append(effect.Effect(128, 100, 5, 0, 0))       # StageClear

            # オブジェクトを消す ---------------------------------
            # プレイヤーを消す
            for n,p in enumerate(imp.Pl):
                if p.Death != 0:
                    del imp.Pl[n]     # リストから削除する

            # プレイヤーの弾を消す
            for n,p in enumerate(imp.PlBullet):
                if p.Death != 0:
                    del imp.PlBullet[n]     # リストから削除する

            # 敵を消す
            for n,e in enumerate(imp.Em):
                if e.Death != 0:
                    del imp.Em[n]        # リストから削除する

            # 敵の弾を消す
            for n,e in enumerate(imp.EmBullet):
                if e.Death != 0:
                    del imp.EmBullet[n]        # リストから削除する

            # エフェクトを消す
            for n,e in enumerate(imp.Eff):
                if e.Death != 0:
                    del imp.Eff[n]        # リストから削除する

            # アイテムを消す
            for n,e in enumerate(imp.Itm):
                if e.Death != 0:
                    del imp.Itm[n]        # リストから削除する

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

        # タイル描画
        if imp.Game_Status == imp.GAME_STATUS_TITLE:
            # タイトル画面
            pyxel.bltm(0, 0, 0, 8 * 9, 0, 32, 30)
        else:
            # ゲーム画面
            pyxel.bltm(imp.TilePosX - 64, imp.TilePosY, 0, 32-8, 0, 32+16, 1024)
            if imp.Game_Status == imp.GAME_STATUS_MAIN or imp.Game_Status == imp.GAME_STATUS_STAGECLEAR:
                imp.TilePosY += 0.1
                if imp.TilePosY > 0:
                    imp.TilePosY = 0


        if imp.Game_Status == imp.GAME_STATUS_MAIN or imp.Game_Status == imp.GAME_STATUS_GAMEOVER or imp.Game_Status == imp.GAME_STATUS_STAGECLEAR:
            # プレイヤー
            for n in imp.Pl:
                n.Draw()

            # プレイヤーの弾
            for n in imp.PlBullet:
                n.Draw()

            # 敵
            for n in imp.Em:
                n.Draw()

            # 敵の弾
            for n in imp.EmBullet:
                n.Draw()

            # エフェクト
            for n in imp.Eff:
                n.Draw()

            # アイテム
            for n in imp.Itm:
                n.Draw()

            # スコアの表示
            sc = "{:04}".format(self.Score)
            pyxel.text(100, 10, sc, 7)

            # Itemゲージ
            for p in imp.Pl:
                for n in range(5):
                    if n >= p.ItemNum:
                        pyxel.blt(10 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 6, 8 * 1, 8, 8, 0)  # 空
                    else:
                        pyxel.blt(10 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 6, 8 * 2, 8, 8, 0)  # とった分
            # Lifeゲージ
            for p in imp.Pl:
                for n in range(5):
                    if n >= p.Life:
                        pyxel.blt(100 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 6, 8 * 1, 8, 8, 0)  # 空
                    else:
                        pyxel.blt(100 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 6, 8 * 2, 8, 8, 0)  # とった分
    #  ------------------------------------------
    def SetStageEnemy(self):
        # ステージの位置から敵をセットする
        for n,e in enumerate(imp.STAGE_EM_POS):
            if self.Stage_Pos == e[0]:
                imp.Em.append(enemy.Enemy(e[1], e[2], e[3], e[4], e[5]))

    #  ------------------------------------------
    def CheckColli(self, plat, embd):
        xx = abs(plat.PosX - embd.PosX)
        yy = abs(plat.PosY - embd.PosY)

        rx = (plat.HitRectX / 2) + (embd.HitRectX / 2)
        ry = (plat.HitRectY / 2) + (embd.HitRectY / 2)

        if xx < rx and yy < ry:
            plat.Death = 1          # 攻撃側は消える
            # エフェクト
            imp.Eff.append(effect.Effect(plat.PosX, plat.PosY, 0, 0, 0))

            embd.Life -= plat.HitPoint      # ダメージ計算
            if embd.Life <= 0:              # 0以下なら死ぬ
                embd.Life = 0
                App.Score += embd.Score     # Scoreを加算
                print("hit")
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
            
            print("item")
            p.ItemNum += 1              # 1個とる
            return True                 # 当たり

        return False                    # 外れ

    #  ------------------------------------------
    def DeathAllObject(self):
        # プレイヤーを消す
        for p in imp.Pl:
            p.Death = 1

        # プレイヤーの弾を消す
        for p in imp.PlBullet:
            p.Death = 1

        # 敵を消す
        for e in imp.Em:
            e.Death = 1

        # 敵の弾を消す
        for e in imp.EmBullet:
            e.Death = 1

        # エフェクトを消す
        for e in imp.Eff:
            e.Death = 1

        # アイテムを消す
        for e in imp.Itm:
            e.Death = 1

App()
