import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900
delta = {
     pg.K_UP: (0, -5),
     pg.K_DOWN: (0, +5),
     pg.K_LEFT: (-5, 0),
     pg.K_RIGHT: (+5, 0)
 }


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数 rct：こうかとんor爆弾SurfaceのRect
    戻り値：横方向，縦方向はみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向はみ出し判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向はみ出し判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_ch = pg.image.load("ex02/fig/6.png")  #画像切り替え後の画像
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) 
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  #練習1  爆弾作成
    bb_rct.centery = random.randint(0, HEIGHT)
    clock = pg.time.Clock()
    vx, vy = +5, +5
    tmr = 0
    
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  #練習5  Game Over
            kk_img = kk_img_ch  #演習3  画像切り替え
            screen.fill((255,0,0))  #演習5  画面切り替え(赤色に)
            screen.blit(kk_img, kk_rct)
            pg.display.update()
            print("Game Over")
            return    
        key_lst = pg.key.get_pressed()  #練習3  キーが押されたら
        sum_mv =[0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:   
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        accs = [a for a in range(1,11)]        
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]   #演習3　加速させる
        vx, vy = +avx, +avy     

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):  #練習4  画面外に出ない
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  #練習2  爆弾の移動
        screen.blit(bb_img, bb_rct)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx*= -1
        if not tate:
            vy*= -1    
        bb_rct.move_ip(vx, vy)    
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()