import pygame
import sys
import random

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("中国象棋")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 加载棋盘和棋子图片
board_img = pygame.image.load("board.png")
pieces_img = pygame.image.load("pieces.png")

# 棋盘位置
board_pos = (50, 50)

# 棋子位置
pieces_pos = [
    # 红方棋子
    (50, 50), (150, 50), (250, 50), (350, 50), (450, 50), (550, 50), (650, 50), (750, 50),
    (50, 150), (150, 150), (250, 150), (350, 150), (450, 150), (550, 150), (650, 150), (750, 150),
    # 黑方棋子
    (50, 650), (150, 650), (250, 650), (350, 650), (450, 650), (550, 650), (650, 650), (750, 650),
    (50, 550), (150, 550), (250, 550), (350, 550), (450, 550), (550, 550), (650, 550), (750, 550)
]

# 当前选中的棋子
selected_piece = None

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, piece_pos in enumerate(pieces_pos):
                if piece_pos[0] < pos[0] < piece_pos[0] + 50 and piece_pos[1] < pos[1] < piece_pos[1] + 50:
                    selected_piece = i
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_piece is not None:
                pos = pygame.mouse.get_pos()
                pieces_pos[selected_piece] = (pos[0] // 100 * 100, pos[1] // 100 * 100)
                selected_piece = None

    # 绘制棋盘
    screen.fill(WHITE)
    screen.blit(board_img, board_pos)

    # 绘制棋子
    for pos in pieces_pos:
        screen.blit(pieces_img, pos)

    pygame.display.flip()

    # 简单的AI逻辑：随机移动一个棋子
    if not running:
        break
    ai_piece = random.choice(range(len(pieces_pos)))
    ai_move = (random.choice(range(0, 800, 100)), random.choice(range(0, 800, 100)))
    pieces_pos[ai_piece] = ai_move

pygame.quit()
sys.exit()