from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import mss
import subprocess
import time
import copy
import pyautogui
from utils import find_empty, is_valid, solve_sudoku, returnUnfilledPositions


model = YOLO("./train/weights/last.pt")
digit_recognizer = tf.saved_model.load("digit_recognizer")

# Only takes the image from the left
def returnBoard():
    # Step 1: Capture the screen
    monitor = mss.mss().monitors[0]
    monitor["width"] = monitor["width"]//2
    image = np.array(mss.mss().grab(monitor))[:, :, :3].astype(np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pred = model(image, verbose=False)
    if len(pred[0].boxes.data) > 0:
        pred = model(image, verbose=False)[0].boxes.data[0]
        x1, y1, x2, y2 = tuple(map(int, pred[:4]))
        patch = image[y1:y2, x1:x2, :]
        return patch, x1, y1
    return False


def extractPatches(board):
    height, width, _ = board.shape
    stride_height = height//9
    stride_width = width//9
    patches = []
    for i in range(9):
        for j in range(9):
            patch = cv2.resize(board[i*stride_height:(i+1)*stride_height, j*stride_width:(j+1)*stride_width, :], (50, 50))
            patches.append(patch)
    return patches, stride_height, stride_width

def constructBoard(patches):
    board = []
    for i in range(len(patches)//9):
        row_i = tf.convert_to_tensor(patches[i*9:(i+1)*9], dtype=tf.float32)
        row_i = digit_recognizer(row_i).numpy().argmax(1)
        board.append(row_i)
    return board

### Inference
boardImg, offsetX, offsetY = returnBoard()
patches, stride_height, stride_width = extractPatches(boardImg)
boardNums = constructBoard(patches)
solvedBoard = copy.deepcopy(boardNums)
solvedFlag = solve_sudoku(solvedBoard)
mousePositions, values = returnUnfilledPositions(boardNums, solvedBoard, stride_height, stride_width, offsetX, offsetY)
for p, v in zip(mousePositions, values):
#     time.sleep(0.1)
    subprocess.call(["xdotool", "mousemove", str(p[1]), str(p[0])])
    subprocess.call(["xdotool", "click", "1"])
    pyautogui.press(str(v))
    