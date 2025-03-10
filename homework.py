import copy
import time
import numpy as np

def read_input(filename):
    with open(filename, "r") as file_content:
        file = file_content.readlines()
        player = file[0].strip()
        if player == "X": opponent = "O"
        else: opponent = "X"
        player_time, opponent_time = np.float64(file[1].split(" "))
        matrix = file[2:]
        board = {i+1: {j+1: value for j, value in enumerate(row.strip())} for i, row in enumerate(matrix)}
        # print(board)
        file_content.close()

    return player, opponent, player_time, opponent_time, board


def has_neighbor(board, row, col, player):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in directions:
        if (1 <= row + dr <= 12) and (1 <= col + dc <= 12) and board[row + dr][col + dc] == player:
            return True

    return False

def score(board, player, opponent, remaining_time):
    player_score = 0
    opponent_score = 0
    corner_weight = 5
    edge_weight = 2
    centre_weight = 1
    isolation_penalty = -10
    corners = [(1, 1), (1, 12), (12, 1), (12, 12)]
    edges = [(1, j) for j in range(2, 12)] + [(12, j) for j in range(2, 12)] + [(i, 1) for i in range(2, 12)] + [(i, 12) for i in range(2, 12)]
    for i in range(1, 13):
        for j in range(1, 13):
            if board[i][j] == player:
                if (i, j) in corners:
                    player_score += corner_weight
                elif (i, j) in edges:
                    player_score += edge_weight
                else:
                    player_score += centre_weight

                if not has_neighbor(board, i + 1, j + 1, player):
                    player_score += isolation_penalty

            elif board[i][j] == opponent:
                if (i, j) in corners:
                    opponent_score += corner_weight
                elif (i, j) in edges:
                    opponent_score += edge_weight
                else:
                    opponent_score += centre_weight

                if not has_neighbor(board, i + 1, j + 1, opponent):
                    opponent_score += isolation_penalty

    player_count = sum(list(row.values()).count(player) for row in board.values())
    opponent_count= sum(list(row.values()).count(opponent) for row in board.values())
    if player == "X":
        player_count = player_count + 1
    else:
        opponent_count = opponent_count + 1
    weight_score = player_score-opponent_score
    count_score = player_count-opponent_count
    return (2*weight_score) + count_score
    
def get_valid_moves(board, player, opponent):
    valid_moves = []

    for row, columns in board.items():
        for col, value in columns.items():
            if value == '.' and is_valid_move(board, player, opponent, row, col):
                valid_moves.append((row, col))

    return valid_moves

def is_valid_move(board, player, opponent, row, col):
    if board[row][col] != '.':
        return False
    for direction in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        if valid_direction(board, player, opponent, row, col, direction): return True
    return False

def valid_direction(board, player, opponent, row, col, direction):
    dr, dc = direction
    if (row + dr<1) or (row + dr>12): return False
    if (col + dc<1) or (col + dc>12): return False
    if board[row + dr][col + dc] != opponent: return False

    x_scan = (row + (2*dr))
    y_scan = (col + (2*dc))

    while (1 <= x_scan <= 12) and (1 <= y_scan <= 12):
            if board[x_scan][y_scan] == player:
                return True
            elif board[x_scan][y_scan] == '.':
                return False
            x_scan += dr
            y_scan += dc
    return False

def make_move(board, move, player, opponent):
    updated_board = copy.deepcopy(board)
    if move is not None:
        row, col = move
        updated_board[row][col] = player
        updated_board = flip_pieces(updated_board, player, opponent, row, col)
    return updated_board

def flip_pieces(board, player, opponent, row, col):
    for direction in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        if valid_direction(board, player, opponent, row, col, direction):
            dr, dc = direction
            x, y = row + dr, col + dc
            while board[x][y] == opponent:
                board[x][y] = player
                x += dr
                y += dc
    return board

def is_terminal(board, player, opponent):
    return not get_valid_moves(board, player, opponent)

def minimax(board, player, opponent, maximizing_player, alpha, beta, max_depth, remaining_time):
    global transposition_table
    board_str = str(board)
    if (max_depth == 0) or (is_terminal(board, player, opponent)):
        return score(board, player, opponent, remaining_time)
    
    if board_str in transposition_table:
        return transposition_table[board_str]
    
    valid_moves = get_valid_moves(board, player, opponent)

    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves:
            update_board = make_move(board, move, player, opponent)
            eval_score = minimax(update_board, player, opponent, False, alpha, beta, max_depth-1, remaining_time)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta<=alpha:
                break
        transposition_table[board_str] = max_eval
        return max_eval

    else:
        min_eval = float('inf')
        for move in valid_moves:
            update_board = make_move(board, move, player, opponent)
            eval_score = minimax(update_board, player, opponent, True, alpha, beta, max_depth-1, remaining_time)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha: 
                break 
        transposition_table[board_str] = min_eval
        return min_eval

def op_write(output):
    with open('output.txt', 'w') as f:
        column_mapping = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k', 12: 'l'}
        op = [f"{column_mapping[output[1]]}{output[0]}"]
        f.write(" ".join(op))
    return

def main(filename):
    global transposition_table
    start = time.time()
    player, opponent, player_time, opponent_time, board = read_input(filename)
    alpha, beta = float('-inf'), float('inf')

    remaining_time = player_time
        
    if remaining_time>=150: max_depth = 6
    elif 100<=remaining_time<150: max_depth = 5
    elif 50<=remaining_time<100: max_depth = 4
    elif 30<=remaining_time<50: max_depth = 3
    elif 5<=remaining_time<30: max_depth = 2
    elif remaining_time<5: max_depth = 1

    valid_moves = get_valid_moves(board, player, opponent)
    if valid_moves:
        best_score = float("-inf")
        best_move = None
        for move in valid_moves:
            updated_board = make_move(board, move, player, opponent)
            move_score = minimax(updated_board, player, opponent, True, alpha, beta, max_depth, remaining_time)
            if move_score > best_score:
                best_move = move
                best_score = move_score
        board = make_move(board, best_move, player, opponent)

    #print(f"Best Move : {best_move}")
    #print(f"Winner: {best_score}")
    op_write(best_move)
    print(time.time() - start)

if __name__ == "__main__":
    transposition_table = {}
    main("input.txt")