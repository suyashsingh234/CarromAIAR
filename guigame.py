from carrom import Carrom
from pygame import Rect
import pygame
from start_menu import start_window, create_button
from ai import ai
class args:
    player1=1
    player2=2
    width=700
    max_angle=80
    max_speed=40
    dt=0.1
    decelerate=0.3
    e=0.9
    num_updates=10
    fps=60

args = args()

width = int(args.width)
dt = float(args.dt)
decelerate = float(args.decelerate)
e = float(args.e)
num_updates = int(args.num_updates)

max_angle = float(args.max_angle)
max_speed = float(args.max_speed)

fps = int(args.fps)

while True:
    player1, player2 = start_window(args.width,args.fps)
    print(player1)
    print(player2)
    """ Printing game constraints """
    print("Parameters are width:", width, "dt:", dt, "decelerate:", decelerate, "e:", e, "max_angle:", max_angle,
          "max_speed:", max_speed, "num_updates:", num_updates, "fps:", fps, "player1:", player1, "player2:", player2)

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
                print(carrom_.striker.position.x)
                carrom_.striker.position.x -= 4 if not pressed[pygame.K_LSHIFT] else 0.5
            if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
                print(carrom_.striker.position.x)
                carrom_.striker.position.x += 4 if not pressed[pygame.K_LSHIFT] else 0.5

            if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
                print(striker_speed)
                striker_speed -= max_speed * 0.05 if not pressed[pygame.K_LSHIFT] else max_speed * 0.005
            if pressed[pygame.K_w] or pressed[pygame.K_UP]:
                print(striker_speed)
                striker_speed += max_speed * 0.05 if not pressed[pygame.K_LSHIFT] else max_speed * 0.005

            if pressed[pygame.K_q]:
                print(striker_angle)
                striker_angle += max_angle * 0.05 if not pressed[pygame.K_LSHIFT] else max_angle * 0.005
            if pressed[pygame.K_e]:
                print(striker_angle)
                striker_angle -= max_angle * 0.05 if not pressed[pygame.K_LSHIFT] else max_angle * 0.005

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
        if players[carrom.player_turn] == "ai" :
            """ Just refresh the board """
            carrom.draw(win)
            carrom.board.show_notification(win, "AI thinking")
            pygame.display.flip()
            handle_events()
            """ let the ai make the decision for the striker """
            ai(carrom, max_angle, max_speed, decelerate, e, dt)
            """ just indicate to the user, the ai's decision """
            carrom.draw(win)
            carrom.board.draw_striker_arrow_pointer(win, carrom.striker, max_speed)
            carrom.board.show_notification(win, "AI decided")
            pygame.display.flip()
            handle_events()
            """wait for some time """
            pygame.time.delay(100)
        else :
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