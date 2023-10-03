import sys
import pygame as pg
import random
import math

WIDTH, HEIGHT = 1600, 900

def gamengai(rect):
    xx = rect.left >= 0 and rect.right <= WIDTH
    yy = rect.top >= 0 and rect.bottom <= HEIGHT
    return xx, yy

def main():
    font = pg.font.Font(None, 36)  # フォントを設定
    start_time = pg.time.get_ticks()  # ゲーム開始時刻を記録
    font = pg.font.Font("japanese_font.ttf", 36)
    
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    
    
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900,400
    
    enn = pg.Surface((20, 20))
    pg.draw.circle(enn, (255, 0, 0), (10, 10), 10)
    enn.set_colorkey((0, 0, 0))
    x, y = random.randint(0,1600), random.randint(0,900)
    vx,vy = +5, +5
    enn_rct = enn.get_rect()
    enn_rct.center = x, y
    clock = pg.time.Clock()
    tmr = 0
    
    accs = [a for a in range(1, 11)] # 加速度のリスト
    enn_imgs = [] # 爆弾のコスチュームのリスト
    for r in range(1, 11):
        enn_img = pg.Surface((20*r, 20*r), pg.SRCALPHA)
        pg.draw.circle(enn_img, (255, 0, 0), (10*r, 10*r), 10*r)
        enn_imgs.append(enn_img)
        
    key_zi = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
        }
    cos_zi = {
        (0, 5): (pg.transform.flip(kk_img, True, False), -90),
        (5, 5): (pg.transform.flip(kk_img, True, False), -45),
        (5, 0): (pg.transform.flip(kk_img, True, False), 0),
        (5, -5): (pg.transform.flip(kk_img, True, False), 45),
        (0, -5): (pg.transform.flip(kk_img, True, False), 90),
        (-5, 5): (kk_img, 45),
        (-5, -5): (kk_img, -45),
        (-5, 0): (kk_img, 0)
    }
    
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])
        
        # こうかとんを動かす
        key_lst = pg.key.get_pressed()
        total = [0, 0]
        newkk = kk_img
        
        for k, m in key_zi.items():
            if key_lst[k]:
                total[0] += m[0]
                total[1] += m[1]
        kk_rct.move_ip(total)
        
        # こうかとんの向きを変える
        for kk, mm in cos_zi.items():
            if total[0] == kk[0] and total[1] == kk[1]:
                newkk = pg.transform.rotozoom(mm[0], mm[1], 1.0)
        screen.blit(newkk, [kk_rct.x, kk_rct.y])
        
        # こうかとんと爆弾が画面外に出たか判定
        kk_in = gamengai(kk_rct)
        if not kk_in[0]:
            kk_rct.x = max(0, min(kk_rct.x, WIDTH - kk_rct.width))
        if not kk_in[1]:
            kk_rct.y = max(0, min(kk_rct.y, HEIGHT - kk_rct.height))

        enn_in = gamengai(enn_rct)
        if not enn_in[0]:
            vx = -vx
        if not enn_in[1]:
            vy = -vy
        
        # 爆弾がこうかとんに近づく
        kyori = (kk_rct.centerx-enn_rct.centerx, kk_rct.centery-enn_rct.centery) # 爆弾から見たベクトル
        norm = math.sqrt(kyori[0]**2 + kyori[1]**2) 
        if norm < 500:
        # 距離が500未満の場合、現在の方向に一定の慣性を持って進行し続ける
            avx, avy = vx, vy  # 慣性を調整するための係数を調整
        else:
        # 距離が500以上の場合、従来通りキャラクターを追跡する
            vctr = (kyori[0] / norm * math.sqrt(50), kyori[1] / norm * math.sqrt(50)) # ベクトルを√50になるように正規化
            avx, avy = vctr[0] * accs[min(tmr // 500, 9)], vctr[1] * accs[min(tmr // 500, 9)]
            vx, vy = vctr[0], vctr[1]
            
        enn_img = enn_imgs[min(tmr//500, 9)] # 時間とともに爆弾を拡大
        screen.blit(enn_img, [enn_rct.x, enn_rct.y])
        
        
        # 経過時間を計算（ミリ秒単位）
        elapsed_time = pg.time.get_ticks() - start_time

        # 経過時間を秒単位に変換
        seconds = elapsed_time // 1000

        # テキストを作成
        time_text = f"タイム: {seconds} 秒"
        
        # テキストを描画
        text_surface = font.render(time_text, True, (0, 0, 0))
        screen.blit(text_surface, (10, 10))  # 位置を調整して描画
          
        # こうかとんと爆弾がぶつかったら終了  
        if kk_rct.colliderect(enn_rct):
            return
        
        enn_rct.move_ip(avx, avy)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        
        

        

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()