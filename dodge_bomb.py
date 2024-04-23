import os
import random
import sys
import pygame as pg


# WIDTH, HEIGHT = 1600, 900
WIDTH, HEIGHT = 1024, 576
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct : pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRect または 爆弾Rect
    戻り値:タプル (x方向判定結果, y方向判定結果)
    画面内ならTrue, 画面外ならFalse
    """
    in_x, in_y = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        in_x = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        in_y = False
    return in_x, in_y


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    bomb_sfc = pg.Surface((20, 20))
    pg.draw.circle(bomb_sfc, (255, 0, 0), (10, 10), 10)
    bomb_sfc.set_colorkey((0, 0, 0))
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5

    clock = pg.time.Clock()
    tmr = 0
    #移動量辞書 {押下キー : (x変化量, y変化量)}
    DIF = {
        pg.K_UP : (0, -5),
        pg.K_DOWN : (0, 5),
        pg.K_LEFT : (-5, 0),
        pg.K_RIGHT : (5, 0)
    }

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        # こうかとんの境界判定と移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, (dx, dy) in DIF.items():
            if(key_lst[key]):
                sum_mv[0] += dx
                sum_mv[1] += dy
        kk_rct.move_ip(sum_mv)
        kk_in = check_bound(kk_rct)
        if kk_in != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # 爆弾の境界判定と移動
        bomb_in_x, bomb_in_y = check_bound(bomb_rct)
        if not bomb_in_x:
            vx *= -1
        if not bomb_in_y:
            vy *= -1
        bomb_rct.move_ip(vx, vy)

        screen.blit(kk_img, kk_rct)
        screen.blit(bomb_sfc, bomb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
