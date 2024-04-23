import os
import random
import sys
import time
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


def rotate_img(obj_img : pg.Surface) -> dict[tuple[int, int] : pg.Surface]:
    """
    引数:こうかとんSurface
    戻り値:移動量の入ったtupleがkey
    回転されたpg.Surfaceがvalue
    """
    rotation = {
        (-5, 0) : pg.transform.rotozoom(obj_img, 0, 1.0),
        (-5, 5) : pg.transform.rotozoom(obj_img, 45, 1.0),
        (0, 5) : pg.transform.rotozoom(obj_img, 90, 1.0),
        (5, 5) : pg.transform.rotozoom(obj_img, 135, 1.0),
        (5, 0) : pg.transform.rotozoom(obj_img, 180, 1.0),
        (5, -5) : pg.transform.rotozoom(obj_img, 225, 1.0),
        (0, -5) : pg.transform.rotozoom(obj_img, 270, 1.0),
        (-5, -5) : pg.transform.rotozoom(obj_img, 315, 1.0)
    }
    return rotation


def bomb_zoom(obj_img : pg.Surface) -> tuple[pg.Surface]:
    """
    引数:爆弾Surface
    戻り値:Surfaceの入ったタプル
    len==10で拡大率の昇順で並んでいる
    """
    obj_imgs = []
    for r in range(1, 11):
        obj_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(obj_img, (255, 0, 0), (10*r, 10*r), 10*r)
        obj_img.set_colorkey((0, 0, 0))
        obj_imgs.append(obj_img)
    return tuple(obj_imgs)


def bomb_acc() -> tuple:
    """
    引数:なし
    戻り値:(1, 2, ... 9, 10)
    """
    accs = [a for a in range(1, 11)]
    return tuple(accs)


def game_over(screen : pg.Surface):
    black_screen_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_screen_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    black_screen_img.set_alpha(150)

    kk_img = pg.image.load("fig/8.png")
    kk_img2 = pg.image.load("fig/8.png")
    kk_rct = kk_img.get_rect()
    kk_rct2 = kk_img.get_rect()
    kk_rct.center = WIDTH/2 - 200, HEIGHT/2
    kk_rct2.center = WIDTH/2 + 200, HEIGHT/2

    fonto = pg.font.Font(None, 80)
    txt_img = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt_img.get_rect()
    txt_rct.center = WIDTH/2, HEIGHT/2

    screen.blit(black_screen_img, (0, 0))
    screen.blit(txt_img, txt_rct)
    screen.blit(kk_img, kk_rct)
    screen.blit(kk_img2, kk_rct2)
    pg.display.update()
    time.sleep(5)


def homing(kk : pg.Rect, bb : pg.Rect) -> tuple[float, float]:
    """
    """
    kk_x, kk_y = kk.center
    bb_x, bb_y = bb.center
    dif_x = kk_x - bb_x
    dif_y = kk_y - bb_y
    #print(dif_x, dif_y)
    normalizer = ((dif_x**2 + dif_y**2) / 50**(1/2))**(1/2)
    norm_dif_x = dif_x / normalizer
    norm_dif_y = dif_y / normalizer
    # if((dif_x**2 + dif_y**2)**(1/2) < 300):
    #     norm_dif_x += -1
    #     norm_dif_y += -1
    print((norm_dif_x**2 + norm_dif_y**2)**(1/2))
    return (norm_dif_x, norm_dif_y)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    bomb_img = pg.Surface((20, 20))
    pg.draw.circle(bomb_img, (255, 0, 0), (10, 10), 10)
    bomb_img.set_colorkey((0, 0, 0))
    bomb_rct = bomb_img.get_rect()
    bomb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5

    clock = pg.time.Clock()
    tmr = 0

    # 移動量辞書 {押下キー : (x変化量, y変化量)}
    DIF = {
        pg.K_UP : (0, -5),
        pg.K_DOWN : (0, 5),
        pg.K_LEFT : (-5, 0),
        pg.K_RIGHT : (5, 0)
    }

    # 回転辞書を取得
    ROT = rotate_img(kk_img)
    
    # 加速度リストを取得
    bomb_accs = bomb_acc()

    # 拡大爆弾Surfaceリストを取得
    bomb_imgs = bomb_zoom(bomb_img)

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
        
        # 爆弾の大きさを更新
        bomb_img = bomb_imgs[min(tmr//300, 9)]

        # 爆弾の境界判定と移動
        bomb_in_x, bomb_in_y = check_bound(bomb_rct)
        if not bomb_in_x:
            vx *= -1
        if not bomb_in_y:
            vy *= -1
        
        # 爆弾の向き変更
        vx, vy = homing(kk_rct, bomb_rct)

        # 爆弾の加速
        avx = vx*bomb_accs[min(tmr//250, 9)]
        avy = vy*bomb_accs[min(tmr//300, 9)]
        bomb_rct.move_ip(avx, avy)

        # こうかとんと爆弾の衝突判定
        if kk_rct.colliderect(bomb_rct):
            game_over(screen)
            return
        
        # こうかとんの向きを変える
        if tuple(sum_mv) in ROT:
            kk_img = ROT[tuple(sum_mv)]

        screen.blit(kk_img, kk_rct)
        screen.blit(bomb_img, bomb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
