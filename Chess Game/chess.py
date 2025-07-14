import pygame
import chess
import chess.engine
import sys
from pathlib import Path

# === CONFIG ===
WIDTH, HEIGHT = 480, 480
SQUARE_SIZE = WIDTH // 8
STOCKFISH_PATH = Path(__file__).with_name("stockfish-windows-x86-64-avx2.exe")  # update if renamed

WHITE_SQ = (245, 245, 220)
BROWN_SQ = (139, 69, 19)

# === INIT ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()

# === LOAD PIECE IMAGES ===
pieces_images: dict[str, pygame.Surface] = {}
for color in ('w', 'b'):
    for p in ('p', 'r', 'n', 'b', 'q', 'k'):
        key = color + p
        img = pygame.image.load(f"assets/{key}.png").convert_alpha()
        pieces_images[key] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))

# === HELPERS ===
def square_to_screen(square: chess.Square) -> tuple[int, int]:
    """Convert 0–63 square index to top‑left (x,y) pixel for blitting."""
    row, col = divmod(square, 8)
    return col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE  # flip vertically

def screen_to_square(pos: tuple[int, int]) -> chess.Square:
    """Convert mouse (x,y) pixels to chess square index."""
    x, y = pos
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)

def maybe_promote(move: chess.Move, board: chess.Board) -> chess.Move:
    """If the move is a pawn reaching last rank, add queen promotion flag."""
    if board.piece_type_at(move.from_square) == chess.PAWN and (
        chess.square_rank(move.to_square) in (0, 7)
    ):
        return chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)
    return move

def draw(board: chess.Board) -> None:
    # board squares
    for r in range(8):
        for c in range(8):
            color = WHITE_SQ if (r + c) % 2 == 0 else BROWN_SQ
            pygame.draw.rect(screen, color, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    # pieces
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            key = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().lower()
            screen.blit(pieces_images[key], square_to_screen(square))

# === GAME MODES ===
def play_vs_ai():
    board = chess.Board()
    with chess.engine.SimpleEngine.popen_uci(str(STOCKFISH_PATH)) as engine:
        selected = None
        running = True
        while running:
            draw(board)
            pygame.display.flip()

            if board.is_game_over():
                print("Game over:", board.result())
                pygame.time.wait(2000)
                break

            # ---- Human (White) ----
            if board.turn == chess.WHITE:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        sq = screen_to_square(event.pos)
                        if selected is None:
                            if board.piece_at(sq) and board.color_at(sq) == chess.WHITE:
                                selected = sq
                        else:
                            move = chess.Move(selected, sq)
                            move = maybe_promote(move, board)
                            if move in board.legal_moves:
                                board.push(move)
                            selected = None

            # ---- Engine (Black) ----
            else:
                result = engine.play(board, chess.engine.Limit(time=0.3))
                board.push(result.move)

            clock.tick(60)

def play_local():
    board = chess.Board()
    selected = None
    running = True
    while running:
        draw(board)
        pygame.display.flip()

        if board.is_game_over():
            print("Game over:", board.result())
            pygame.time.wait(2000)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                sq = screen_to_square(event.pos)
                if selected is None:
                    if board.piece_at(sq) and board.color_at(sq) == board.turn:
                        selected = sq
                else:
                    move = chess.Move(selected, sq)
                    move = maybe_promote(move, board)
                    if move in board.legal_moves:
                        board.push(move)
                    selected = None

        clock.tick(60)

# === MENU ===
def menu():
    print("\n♟️  CHESS GAME")
    print("1. Play vs Computer")
    print("2. Play Local 2‑Player")
    choice = input("Enter choice (1/2): ").strip()
    if choice == "1":
        play_vs_ai()
    elif choice == "2":
        play_local()
    else:
        print("Invalid choice.")

# === MAIN ===
if __name__ == "__main__":
    try:
        menu()
    finally:
        pygame.quit()
        sys.exit()
