import sys
import pygame as pg
import random
import math


WIDTH, HEIGHT = 1600, 900


#メイン関数
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900,400
    
    #問1
    enn = pg.Surface((20, 20)) # 20x20の四角形を作成する
    pg.draw.circle(enn, (255, 0, 0), (10, 10), 10) # 20x20の四角形に内接する半径10の円を描く
    enn.set_colorkey((0, 0, 0))# 透明色を設定する(黒色)
    x, y = random.randint(0,1600), random.randint(0,900) # 0～1600の範囲の乱数をx座標に、0～900の範囲の乱数をy座標に設定する
    enn_rct = enn.get_rect()# ennの矩形を取得する
    enn_rct.center = x, y# ennの矩形の中心座標を(x, y)に設定する
    clock = pg.time.Clock()
    tmr = 0# タイマーを初期化する
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])
        
        
        screen.blit(kk_img, [900, 400])
        pg.display.update()
        tmr += 1
        clock.tick(10)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()