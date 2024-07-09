
def is_legal_pos(board, pos):
    """
    Check if a position is legal on the board.

    Args:
        board (list): A 2D list representing the maze or board.
        pos (tuple): A tuple (row, column) representing the position to check.

    Returns:
        bool: True if the position is legal (not an obstacle and within the board), False otherwise.
    """
    row, col = pos
    if 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] != 1:
        return True
    return False

