import pygame
import pygame_menu
import sys
import random

# Инициализация Pygame
pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Размеры и свойства окна
WIDTH, HEIGHT = 425, 420  # Увеличенные размеры для 5x5 поля
FPS = 30

# Создание игрового поля
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-нолики")

# Инициализация доски
board = [[' ' for _ in range(5)] for _ in range(5)]

font_large = pygame.font.Font(None, 60)  # Уменьшенный размер шрифта для умещения в клетку
font_medium = pygame.font.Font(None, 30)


def draw_board(board):

    """
    Функция отрисовки игрового поля
    :param board: текущее состояние игрового поля
    :return: None
    """

    screen.fill(WHITE)

    cell_width = WIDTH // 5
    cell_height = HEIGHT // 5

    # Рисуем сетку
    for i in range(1, 5):
        pygame.draw.line(screen, BLACK, (i * cell_width, 0), (i * cell_width, HEIGHT), 4)
        pygame.draw.line(screen, BLACK, (0, i * cell_height), (WIDTH, i * cell_height), 4)

    for row in range(5):
        for col in range(5):
            if board[row][col] == 'X':
                text = font_large.render('X', True, BLUE)
            elif board[row][col] == 'O':
                text = font_large.render('O', True, RED)
            else:
                continue
            text_rect = text.get_rect(center=(col * cell_width + cell_width // 2, row * cell_height + cell_height // 2))
            screen.blit(text, text_rect)


def show_winner(winner):

    """
    Функция вывода победителя
    :param winner: символ победителя ('X' или 'O')
    :return: None
    """

    winner_text = font_medium.render(f"Игрок {winner} победил!", True, BLACK)
    winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(winner_text, winner_rect)


def check_winner(board):

    """
    Функция определения победителя
    :param board: текущее состояние игрового поля
    :return: str
    """

    for i in range(5):
        if board[i][0] == board[i][1] == board[i][2] == board[i][3] == board[i][4] != ' ':
            return board[i][0]

        if board[0][i] == board[1][i] == board[2][i] == board[3][i] == board[4][i] != ' ':
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] == board[3][3] == board[4][4] != ' ':
        return board[0][0]

    if board[0][4] == board[1][3] == board[2][2] == board[3][1] == board[4][0] != ' ':
        return board[0][4]

    return None


def is_board_full(board):

    """
    Функция проверки ничьи
    :param board: текущее состояние игрового поля
    :return: bool
    """

    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def evaluate_board(board):

    """
    Функция оценки доски для минимакса
    :param board: текущее состояние игрового поля
    :return: int
    """

    winner = check_winner(board)
    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif is_board_full(board):
        return 0
    else:
        return None


def minimax(board, depth, is_maximizing):

    """
    Функция минимакса для поиска лучшего хода
    :param board: текущее состояние игрового поля
    :param depth: int
    :param is_maximizing:
    :return:
    """

    score = evaluate_board(board)

    if score is not None:
        return score

    if depth >= 3:  # Ограничим глубину рекурсии
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for i in range(5):
            for j in range(5):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(5):
            for j in range(5):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval


def ai_move(board):

    """
    Функция для хода ИИ
    :param board: текущее состояние игрового поля
    :return: int
    """

    best_score = float('-inf')
    best_move = None

    for i in range(5):
        for j in range(5):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_score = minimax(board, 0, False)
                board[i][j] = ' '

                if move_score > best_score:
                    best_score = move_score
                    best_move = (i, j)

    return best_move


def game_single_player_with_smart_ai():

    """
    Функция игры с одним игроком и улучшенным ИИ
    :return: None
    """

    global board
    board = [[' ' for _ in range(5)] for _ in range(5)]  # Сброс игрового поля
    running = True
    current_player = 'X'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif current_player == 'X' and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // (WIDTH // 5)
                row = y // (HEIGHT // 5)

                if board[row][col] == ' ':
                    board[row][col] = current_player

                    winner = check_winner(board)
                    if winner:
                        show_winner(winner)
                        running = False
                    elif is_board_full(board):
                        print("Ничья!")
                        running = False

                    current_player = 'O'

            elif current_player == 'O':
                # Ход ИИ
                move = ai_move(board)
                if move:
                    board[move[0]][move[1]] = current_player

                    winner = check_winner(board)
                    if winner:
                        show_winner(winner)
                        running = False
                    elif is_board_full(board):
                        print("Ничья!")
                        running = False

                    current_player = 'X'

        draw_board(board)
        pygame.display.flip()


def start_single_player_with_smart_ai():

    """
    Функция запуска игры с одним игроком и ИИ
    :return: None
    """

    game_single_player_with_smart_ai()


def start_two_players():

    """
    Функция запуска игры с двумя игроками
    :return: None
    """

    global board
    board = [[' ' for _ in range(5)] for _ in range(5)]  # Сброс игрового поля
    running = True
    current_player = 'X'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // (WIDTH // 5)
                row = y // (HEIGHT // 5)

                if board[row][col] == ' ':
                    board[row][col] = current_player

                    winner = check_winner(board)
                    if winner:
                        show_winner(winner)
                        running = False
                    elif is_board_full(board):
                        print("Ничья!")
                        running = False

                    current_player = 'O' if current_player == 'X' else 'X'

        draw_board(board)
        pygame.display.flip()


# Создание стиля для меню
menu_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
menu_theme.title_background_color = (44, 62, 80)  # Цвет фона заголовка
menu_theme.title_font_color = (255, 255, 255)  # Цвет текста заголовка
menu_theme.widget_font_color = (44, 62, 80)  # Цвет текста виджетов
menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD  # Шрифт для виджетов

# Создание главного меню
main_menu = pygame_menu.Menu("Крестики-нолики", WIDTH, HEIGHT, theme=menu_theme)

# Добавление кнопок в главное меню
main_menu.add.button("Один игрок (с ИИ)", start_single_player_with_smart_ai)
main_menu.add.button("Два игрока", start_two_players)
main_menu.add.button("Выход", pygame_menu.events.EXIT)

if __name__ == "__main__":
    main_menu.mainloop(screen)