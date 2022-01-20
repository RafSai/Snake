import pygame
import random
import sys


def food_pixel(x_coord, y_coord): # Функция для хавки
    pygame.draw.rect(screen, food_color, (4 + x_coord * 20, 5 + y_coord * 20, 20, 20))


def snake_pixels(x_coord, y_coord):  # Упрощение визуализации змейки
    pygame.draw.rect(screen, (100, 0, 255), (4 + x_coord * 20, 5 + y_coord * 20, 20, 20))


# Первый список - голова, далее - тело.
snake_body = [[5, 5], [4, 5], [3, 5]]
# Спавн первой еды
food_coords = [random.randint(1, 19), random.randint(1, 19)]
timer = pygame.time.Clock()

# Все начальные данные
bg_1 = (50, 200, 50)
bg_2 = (50, 100, 50)

bg_hell_1 = (255, 69, 0)
bg_hell_2 = (255, 140, 0)

sc_bg = (150, 150, 0)

food_color = (255, 0, 50)

doom_right = pygame.image.load('doom_1.png')
doom_left = pygame.image.load('doom_2.png')

file = open('score.txt', 'r')
max_score = file.read()
file.close()
# Начальное направление движения
move_x = 1
move_y = 0
tick_val = 4
# Состояния игры
in_hell = False
portal_ready = False
start_screen = True
end_screen = False
# Очки
score = 0

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load('doom_music.mp3')
    size = width, height = 425, 500
    screen = pygame.display.set_mode(size)
    running = True
    f1 = pygame.font.Font(None, 24)
    start_text = f1.render('Нажми Пробел чтобы начать легендарную змейку', True, (255, 255, 255))
    f2 = pygame.font.Font(None, 100)
    start_text_record = f2.render(f'Рекорд: {max_score}', True, (255, 255, 255))
    f3 = pygame.font.Font(None, 20)
    end_text = f3.render(f'Вы проиграли. Ваш результат: {score} ESC для выхода',
                         True, (255, 255, 255))
    f4 = pygame.font.Font(None, 50)
    score_text = f4.render(f'Очки: {score}', True, (255, 255, 255))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                if int(max_score) < score:
                    file.write(str(score))
            if event.type == pygame.KEYDOWN: # Реализация управления на WASD с фиксом невозможных вариантов передвижения
                if event.key == pygame.K_w and move_y == 0:  # Вверх (Нельзя когда ползешь вниз)
                    move_x = 0
                    move_y = -1
                if event.key == pygame.K_a and move_x == 0:  # Влево (Нельзя когда ползешь вправо)
                    move_x = -1
                    move_y = 0
                if event.key == pygame.K_s and move_y == 0:  # Вправо (Нельзя когда ползешь вправо)
                    move_x = 0
                    move_y = 1
                if event.key == pygame.K_d and move_x == 0:  # Вниз (Нельзя когда ползешь вверх)
                    move_x = 1
                    move_y = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if start_screen:
            pygame.display.set_caption("Змейка")
            screen.fill((0, 0, 0))
            screen.blit(start_text, (5, 5))
            screen.blit(start_text_record, (5, 350))
            pygame.display.flip()
        elif end_screen:
            screen.fill((0, 0, 0))
            screen.blit(end_text, (5, 5))
            pygame.display.flip()
        else:
            screen.fill(sc_bg)

            col = True
            for y in range(1, 20):  # Генерация поля
                for x in range(1, 20):
                    if col:
                        pygame.draw.rect(screen, bg_1, (4 + x * 20, 5 + y * 20, 20, 20))
                        col = False
                    else:
                        pygame.draw.rect(screen, bg_2, (4 + x * 20, 5 + y * 20, 20, 20))
                        col = True
        # snake_body[0][0] - координата x головы
        # snake_body[0][1] - координата y головы

        # Передвижение змеи
            snake_pixels(snake_body[0][0] + move_x, snake_body[0][1] + move_y)
            snake_body.insert(0, [snake_body[0][0] + move_x, snake_body[0][1] + move_y])
            snake_body.pop()

        # Выход змеи за границу
            if (snake_body[0][0] > 19 or snake_body[0][0] < 1) or (snake_body[0][1] > 19 or snake_body[0][1] < 1):
                end_screen = True
        # Если змея наткнулась сама на себя
            if snake_body[0] in snake_body[1:]:
                end_screen = True

        # Реализация еды
            if food_coords == [snake_body[0][0], snake_body[0][1]]:
                snake_body.append(food_coords)  # Добавление длинны змее, после взятия еды.
                score = score + 1
            if score >= 15 and in_hell is False:
                food_coords = [-5, -5]
                portal_ready = True
            while food_coords in snake_body:  # Цикл для того, чтобы еда не появлялась на занятых клетках.
                food_coords = [random.randint(1, 19), random.randint(1, 19)]
            while food_coords in [[x, y] for x in range(6, 15) for y in range(6, 15)] and in_hell:
                food_coords = [random.randint(1, 19), random.randint(1, 19)]
            food_pixel(food_coords[0], food_coords[1])
            if portal_ready:
                pygame.draw.rect(screen, (255, 0, 0), (4 + 17 * 20, 5 + 8 * 20, 40, 80))  # Цвета портала
                pygame.draw.rect(screen, (0, 0, 0), (4 + 16 * 20, 5 + 7 * 20, 80, 100), 20)
                # Хитбокс портала создан генератором для оптимизации кода
                if [snake_body[0][0], snake_body[0][1]] in [[x, y] for x in range(17, 19) for y in range(8, 11)]:
                    portal_ready = False
                    snake_body = [[3, 1], [2, 1], [1, 1]]
                    move_x = 1
                    move_y = 0
                    in_hell = True
                    score = 666
                    food_coords = [2, 1]
                    pygame.mixer.music.play(-1)
            if in_hell:
                bg_1 = bg_hell_1
                bg_2 = bg_hell_2
                sc_bg = (255, 0, 0)
                tick_val = 8
                food_color = (255, 255, 255)
                pygame.draw.rect(screen, (0, 0, 0), (4 + 6 * 20, 5 + 6 * 20, 180, 180))
                if snake_body[0][0] > 10:
                    screen.blit(doom_right, (124, 125))
                else:
                    screen.blit(doom_left, (124, 125))
                if snake_body[0] in [[x, y] for x in range(6, 15) for y in range(6, 15)]:
                    end_screen = True
            end_text = f3.render(f'Вы проиграли. Ваш результат: {score} ESC для выхода',
                                 True, (255, 255, 255))
            score_text = f4.render(f'Очки: {score}', True, (255, 255, 255))
            screen.blit(score_text, (5, 440))
            if int(max_score) < score:
                file = open('score.txt', 'w')
                file.write(str(score))
                file.close()
            timer.tick(tick_val)
            for coords in snake_body:  # Отрисовка изменений всей змеи
                snake_pixels(coords[0], coords[1])
            pygame.display.flip()

    pygame.quit()