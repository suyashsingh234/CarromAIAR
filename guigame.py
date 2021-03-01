from carrom import Carrom
from pygame import Rect
import pygame
import argparse
from create_button import create_button

parser = argparse.ArgumentParser()
parser.add_argument('--player1', '-1')
parser.add_argument('--player2', '-2')
parser.add_argument('--width', '-w', type=int, default=700, help="carrom window width")
parser.add_argument("--max_angle", type=float, default=80, help="maximum striker angle")
parser.add_argument("--max_speed", type=float, default=40, help="maximum striker speed")
parser.add_argument("--dt", type=float, default=0.1, help="simulation interval")
parser.add_argument("--decelerate", type=float, default=0.3, help="deceleration due to friction")
parser.add_argument("--e", type=float, default=0.9, help="co-efficient of restitution for collisions")
parser.add_argument("--num_updates", type=int, default=10, help="number of updates before drawing to screen")
parser.add_argument("--num_random_choices", type=int, default=40, help="number of search points for random ai")
parser.add_argument("--no_start_menu", action="store_true", help="disable start menu")
parser.add_argument("--fps", type=int, default=60, help="frames per second")
args = parser.parse_args()

width = int(args.width)
dt = float(args.dt)
decelerate = float(args.decelerate)
e = float(args.e)
num_updates = int(args.num_updates)

max_angle = float(args.max_angle)
max_speed = float(args.max_speed)

fps = int(args.fps)

while True:
    player1, player2 = args.player1, args.player2

    pygame.init()
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("PyCarrom: WHITE(%s) vs BLACK(%s)" % (player1, player2))

    carrom = Carrom(Rect(0, 0, width, width))
    players = [player1, player2]
    clock = pygame.time.Clock()


    def handle_events():
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                pygame.quit()
                quit()


    def handle_user_input(win_, carrom_, permit_rotation=False):
        get_user_input = True
        striker_speed = 0
        striker_angle = 0
        coins_orientation = 60

        x_limits = carrom_.board.get_striker_x_limits()

        while get_user_input:
            clock.tick(fps)
            for event_ in pygame.event.get():
                if event_.type == pygame.QUIT:
                    pygame.quit()

            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
                carrom_.striker.position.x -= 4 if not pressed[pygame.K_LSHIFT] else 0.5
            if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
                carrom_.striker.position.x += 4 if not pressed[pygame.K_LSHIFT] else 0.5

            if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
                striker_speed -= max_speed * 0.05 if not pressed[pygame.K_LSHIFT] else max_speed * 0.005
            if pressed[pygame.K_w] or pressed[pygame.K_UP]:
                striker_speed += max_speed * 0.05 if not pressed[pygame.K_LSHIFT] else max_speed * 0.005

            if pressed[pygame.K_q]:
                striker_angle += max_angle * 0.05 if not pressed[pygame.K_LSHIFT] else max_angle * 0.005
            if pressed[pygame.K_e]:
                striker_angle -= max_angle * 0.05 if not pressed[pygame.K_LSHIFT] else max_angle * 0.005

            if pressed[pygame.K_r] and permit_rotation:
                coins_orientation += 1 if not pressed[pygame.K_LSHIFT] else -1
                carrom_.rotate_carrom_men(coins_orientation)

            carrom_.striker.position.x = min(x_limits[1], max(x_limits[0], carrom_.striker.position.x))
            striker_speed = min(max_speed, max(striker_speed, 0))
            striker_angle = min(max_angle, max(-max_angle, striker_angle))
            carrom_.striker.velocity.from_polar(
                (striker_speed, -90-striker_angle if carrom_.player_turn == 0 else 90+striker_angle))

            if pressed[pygame.K_SPACE]:
                get_user_input = False

            carrom_.draw(win_)
            carrom_.board.show_notification(win_, "WHITE'S TURN" if carrom.player_turn == 0 else "BLACK'S TURN")
            carrom_.board.draw_striker_arrow_pointer(win_, carrom_.striker, max_speed)
            pygame.display.update()


    while not carrom.game_over:
        carrom.striker.position = carrom.board.get_striker_position(carrom.player_turn)
        handle_user_input(win, carrom)
        pygame.time.delay(100)

        i = 0
        while carrom.check_moving():
            carrom.update(dt, decelerate, e)
            if carrom.check_moving():
                i += 1
                if i % num_updates == 0:
                    clock.tick(60)
                    carrom.draw(win)
                    carrom.board.show_notification(win, "SIMULATING..")
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()

        carrom.apply_rules()

    carrom.draw(win)
    carrom.board.show_notification(win, "GAME OVER..")
    font = pygame.font.Font('freesansbold.ttf', carrom.board.frame_width)
    winner = carrom.get_player(carrom.winner)
    print("Game Over, won by", winner, players[carrom.winner])
    """ Indicate the winner """
    text = font.render("WINNER " + winner, True, (0, 0, 255))
    text_rect = text.get_rect()
    text_rect.center = carrom.board.board.center
    win.blit(text, text_rect)

    restart_button = create_button(width*3//10, width//10, "RESTART", False)
    restart_button_rect = Rect(width*1//10, width*7//10, width*3//10, width//10)
    quit_button = create_button(width*3//10, width//10, "QUIT", False)
    quit_button_rect = Rect(width*6//10, width*7//10, width*3//10, width//10)
    win.blit(restart_button, restart_button_rect)
    win.blit(quit_button, quit_button_rect)
    pygame.display.update()

    while True:
        clock.tick(10)
        handle_events()
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if restart_button_rect.collidepoint(*mouse_pos):
                break
            if quit_button_rect.collidepoint(*mouse_pos):
                pygame.quit()
                quit()














