space = '_'
DIGITS = '123456789'
INEQUAL_SYMBOLS = '<>^v'
SIZE = 4 # size of the board

def inequalities() -> list:
    with open('grid.txt','r') as fp:
        ineq = fp.readlines()
    nest_list = [list(i) for i  in ineq]
    # print(nest_list)
    greater_than = [(nest_list.index(i), i.index('>')) for i in nest_list if '>' in i]
    greater_than_v = [(nest_list.index(i), i.index('v')) for i in nest_list if 'v' in i]
    less_than = [(nest_list.index(i), i.index('<')) for i in nest_list if '<' in i]
    less_than_exp = [(nest_list.index(i), i.index('^')) for i in nest_list if '^' in i]
    return greater_than, greater_than_v, less_than, less_than_exp

def values_in_board() -> list:
    with open('grid.txt','r') as fp:
        vals = fp.readlines()
    nest_list = [list(i) for i  in vals]
    values = [(nest_list.index(i), i.index(j), j) for i in nest_list for j in i if j in DIGITS] 
    return values

def initial_board(size: int, greater_than: list, greater_than_v: list, less_than: list, less_than_exp: list, values: list) -> list:
    board = [["" for i in range(size + (size -1))] for i in range(size + (size -1))]
    for each in greater_than:
        board[each[0]][each[1]] = '>'
    for each in greater_than_v:
        board[each[0]][each[1]] = 'v'
    for each in less_than:
        board[each[0]][each[1]] = '<'
    for each in less_than_exp:
        board[each[0]][each[1]] = '^'
    for each in values:
        board[each[0]][each[1]] = each[2]
    return board

def setup_board(board: list) -> list:
    size = (2*SIZE) - 1
    for i in range(0, size, 2):
        for j in range(0, size, 2):
            if not board[i][j]:
                board[i][j] = '1234'
    return board

def update_grid(board: list, row: int, col: int, value: str) -> list:
    for i in range(len(board[row])):
        if len(board[row][i]) > 1 and value in board[row][i]:
            board[row][i] = board[row][i].replace(value,"")
    for i in range(len(board[row])):
        if len(board[i][col]) > 1 and value in board[i][col]:
            board[i][col] = board[i][col].replace(value,"")
    return board


def update_cell(board: list, i: int, j: int) -> list:
    if j <= len(board[0])-2:
        print(j)
        if len(board[i][j]) == 2:
            print('board val = 2')
            board[i][j] = set(board[i][j]).pop()
        elif board[i][j+1] and (board[i][j+1] in INEQUAL_SYMBOLS):
            if board[i][j+1] == '<':
                while max(board[i][j]) and max(board[i][j+2]) and (max(board[i][j]) >= max(board[i][j+2])):
                    board[i][j] = board[i][j].replace(max(board[i][j]),"")
                while min(board[i][j]) and min(board[i][j+2]) and (min(board[i][j]) >= min(board[i][j+2])):
                    board[i][j+2] = board[i][j+2].replace(min(board[i][j+2]),"")
            if board[i][j+1] == '>':
                while max(board[i][j]) and max(board[i][j+2]) and (max(board[i][j]) <= max(board[i][j+2])):
                    board[i][j+2] = board[i][j+2].replace(max(board[i][j+2]),"")
                while min(board[i][j]) and min(board[i][j+2]) and (min(board[i][j]) <= min(board[i][j+2])):
                    board[i][j] = board[i][j].replace(min(board[i][j]),"")
        elif board[j+1][i] and (board[j+1][i] in INEQUAL_SYMBOLS):
            if board[j+1][i] == '^':
                while max(board[j][i]) and max(board[j+2][i]) and (max(board[j][i]) >= max(board[j+2][i])):
                    board[j][i] = board[j][i].replace(max(board[j][i]),"")
                while min(board[j][i]) and min(board[j+2][i]) and (min(board[j][i]) >= min(board[j+2][i])):
                    board[j+2][i] = board[j+2][i].replace(min(board[j+2][i]),"")
            if board[i][j+1] == 'v':
                while max(board[j][i]) and max(board[j+2][i]) and (max(board[j][i]) <= max(board[j+2][i])):
                    board[j+2][i] = board[j+2][i].replace(max(board[j+2][i]),"")
                while min(board[j][i]) and min(board[j+1][i]) and (min(board[j][i]) <= min(board[j+2][i])):
                    board[j][i] = board[j][i].replace(min(board[j][i]),"")
        elif not board[i][j+1]:
            a = set(board[i][j]).intersection(set(board[i][j+2])).difference(set(list(range(1,SIZE+1))))
    else:
        if len(board[i][j]) == 1:
            print('board val = 1')
        elif len(board[i][j]) == 2:
            print('board val = 2')
            board[i][j] = set(board[i][j]).pop()
        else:
            pass
    return board

def iterate_board(board: list) -> list:
    for i in range(0, len(board[0])):
        for j in range(0, len(board[0])):
            if board[i][j] and ([var for var in board[i][j] if var in DIGITS]):
                if len(board[i][j]) == 1:
                    board = update_grid(board, i, j, board[i][j])
                else:
                    board = update_cell(board, i, j)
    return board

def is_completed(board: list) -> bool:
    total_values = len(''.join([''.join([cell for cell in row if list(filter(lambda x : x in DIGITS, cell))]) for row in board]))
    if total_values == SIZE*SIZE:
        return True
    else:
        return False


greater_than,greater_than_v, less_than, less_than_exp = inequalities()

values = values_in_board()

board = initial_board(SIZE, greater_than, greater_than_v, less_than, less_than_exp, values)

board = setup_board(board)

h = 0
while not is_completed(board):
    board = iterate_board(board)
    for i in board:
        print(i)
