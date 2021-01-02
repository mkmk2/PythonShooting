import pyxel
import enemy

# --------------------------------------------------
# 敵のセット位置
# 1
STAGE_SET_1 = [
    # 時間, X, Y, class, id0, id1, item
    # まっすぐ
    [ 120,  128-30,   0,  enemy.EnemyNorm,  1, 0, 0,],
    [ 120,  128-60,   0,  enemy.EnemyNorm,  1, 0, 0,],

    [ 240,  128+30,   0,  enemy.EnemyNorm,  1, 0, 0,],
    [ 240,  128+60,   0,  enemy.EnemyNorm,  1, 0, 0,],

    [ 340,  128-30,   0,  enemy.EnemyNorm,  1, 0, 0,],
    [ 340,  128+30,   0,  enemy.EnemyNorm,  1, 0, 0,],
    [ 360,  128-60,   0,  enemy.EnemyNorm,  1, 0, 0,],
    [ 360,  128+60,   0,  enemy.EnemyNorm,  1, 0, 0,],
    [ 380,  128-80,   0,  enemy.EnemyNorm,  1, 0, 0,],
    [ 380,  128+80,   0,  enemy.EnemyNorm,  1, 0, 0,],

    # カーブ
    [ 500,  128-40,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [ 530,  128-40,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [ 560,  128-40,   0,  enemy.EnemyNorm,  0, 0, 1,],

    [ 660,  128+40,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [ 690,  128+40,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [ 710,  128+40,   0,  enemy.EnemyNorm,  0, 0, 1,],

    #ワイド
    [ 900,  128-60,   0,  enemy.EnemyWide,  0, 0, 0,],
    [ 930,  128-20,   0,  enemy.EnemyWide,  0, 0, 0,],
    [ 960,  128+60,   0,  enemy.EnemyWide,  0, 0, 0,],
    [ 990,  128+20,   0,  enemy.EnemyWide,  0, 0, 0,],

    # カーブ
    [1000,  128-40,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1030,  128-20,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1060,  128+40,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1090,  128-80,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1120,  128+80,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1150,  128-20,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1180,  128+00,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1210,  128+80,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1240,  128-40,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1260,  128-20,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1290,  128+30,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1310,  128+50,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1320,  128-20,   0,  enemy.EnemyMiss,  0, 0, 1,],    # ミサイル
    [1340,  128-20,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1360,  128-60,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1370,  128+20,   0,  enemy.EnemyMiss,  0, 0, 1,],    # ミサイル
    [1430,  128-40,   0,  enemy.EnemyMiss,  0, 0, 1,],    # ミサイル
    [1500,  128+40,   0,  enemy.EnemyMiss,  0, 0, 1,],    # ミサイル


    [3500,  128,      0,  enemy.EnemyBoss,  0, 0, 0,],    # Boss
]

STAGE_SET_2 = [
    # 時間, X, Y, class, id0, id1, item

    [ 200,  128-60,   0,  enemy.EnemyWide,  0, 0, 0,],    # まっすぐ
    [ 240,  128-60,   0,  enemy.EnemyWide,  0, 0, 0,],
    [ 280,  128-60,   0,  enemy.EnemyWide,  0, 0, 1,],

    [ 500,  128+60,   0,  enemy.EnemyWide,  0, 0, 0,],
    [ 540,  128+60,   0,  enemy.EnemyWide,  0, 0, 0,],
    [ 580,  128+60,   0,  enemy.EnemyWide,  0, 0, 1,],

    [ 760,  128-20,   0,  enemy.EnemyNorm,  0, 0, 0,],    # カーブ
    [ 780,  128-40,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [ 800,  128-60,   0,  enemy.EnemyNorm,  0, 0, 1,],

    [1000,  128+20,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1020,  128+40,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1040,  128+60,   0,  enemy.EnemyNorm,  0, 0, 1,],

    [1300,  128-40,   0,  enemy.EnemyNorm,  0, 0, 0,],    # カーブ
    [1340,  128-60,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [1380,  128-80,   0,  enemy.EnemyNorm,  0, 0, 1,],

    [1600,  128+40,   0,  enemy.EnemyNorm,  0, 0, 1,],
    [1640,  128+60,   0,  enemy.EnemyNorm,  0, 0, 1,],
    [1680,  128+80,   0,  enemy.EnemyNorm,  0, 0, 1,],

    [1750,  128-40,   0,  enemy.EnemyWide,  0, 0, 1,],    # 撃ってもどる
    [1800,  128+40,   0,  enemy.EnemyWide,  0, 0, 1,],

    [1900,  128-00,   0,  enemy.EnemyWide,  2, 0, 1,],    # 全方向撃って戻る
    [2300,  128-40,   0,  enemy.EnemyWide,  2, 0, 1,],    # 全方向撃って戻る
    [2700,  128+40,   0,  enemy.EnemyWide,  2, 0, 1,],    # 全方向撃って戻る


    [ 500,  128,      0,  enemy.EnemyBoss,  0, 0, 0,],    # Boss
]

STAGE_SET_3 = [
    # 時間, X, Y, class, id0, id1, item
    [ 150,  128-40,   0,  enemy.EnemyWide,  0, 0, 1,],    # 撃ってもどる

    [ 500,  128,      0,  enemy.EnemyBoss,  0, 0, 0,],    # Boss
]

STAGE_SET_4 = [
    # 時間, X, Y, class, id0, id1, item
    [ 150,  128-40,   0,  enemy.EnemyWide,  0, 0, 1,],    # 撃ってもどる

    [ 500,  128,      0,  enemy.EnemyBoss,  0, 0, 0,],    # Boss
]

STAGE_SET_TEST = [
    # 時間, X, Y, class, id0, id1, item
    [ 150,  128-40,   0,  enemy.EnemyMiss,  0, 0, 1,],    # ミサイル
#    [ 150,  128-40,   0,  enemy.EnemyWide,  0, 0, 1,],    # 撃ってもどる

    [ 500,  128,      0,  enemy.EnemyBoss,  0, 0, 0,],    # Boss
]

# ==================================================
