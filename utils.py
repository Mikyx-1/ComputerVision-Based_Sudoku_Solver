## Solve Sudoku utils

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
            
def is_valid(board, num, pos):
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check 3x3 box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True
def solve_sudoku(board):
    find = find_empty(board)
    if not find: return True

    row, col = find
    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False


def returnUnfilledPositions(boardNums, solvedBoard, stride_height, stride_width, offsetX, offsetY):
    
    mousePositions = []
    values = []
    for i in range(9):
        for j in range(9):
            if boardNums[i][j] == 0:
                x1 = i*stride_height
                y1 = j*stride_width
                x2 = (i+1)*stride_height
                y2 = (j+1)*stride_width
                values.append(solvedBoard[i][j]) 
                mousePositions.append(( offsetY + (x1+x2)//2, offsetX + (y1+y2)//2))
    return mousePositions, values