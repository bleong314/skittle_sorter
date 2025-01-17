from ultralytics import YOLO
# import torch
import cv2, cvzone
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from peg import Peg
from point import Point
import matplotlib.pyplot as plt

print('Import Success')

nice = Peg(Point(1, 2), True, True, 'black')

TOTAL_PEGS = 61 + 60
CONFIDENCE_THRESHOLD = 0.825
EMPTY = 'empty'
class_names = ['yellow', 'blue', EMPTY, 'purple', 'green', 'red', 'orange']

model = YOLO("best.pt")

# image_path = "data/test/images/IMG_2784.JPG" 
image_path = "../saved_images/image_1.jpg" 
image = cv2.imread(image_path)

print('Loading done')

# Perform object detection
result = model(image_path)[0]

print('Object detection done')

boxes = list(result.boxes)
detected_count = len(boxes)

assert detected_count >= TOTAL_PEGS, f'{detected_count}/{TOTAL_PEGS} not all pegs detected'

boxes.sort(key=lambda box: box.conf[0])

if detected_count > TOTAL_PEGS: 
    for _ in range(detected_count - TOTAL_PEGS): 
        boxes.pop(0)
    print(f'{detected_count - TOTAL_PEGS} extra detections removed')

low_confidence_boxes = list(filter(lambda box: box.conf[0] <= CONFIDENCE_THRESHOLD, boxes))


assert not low_confidence_boxes, f'Exists detections with confidence <= {CONFIDENCE_THRESHOLD}'









# internal_map = [ # 17 x 25
#     #                                                 c
#     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
#     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
#     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1,  0, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
#     [-1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1,  0, -1,  0, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
# ]

NUM_ROWS = 17
MAX_PEGS_PER_ROW = 25
CENTER_COL = 13

# val at ith = # pegs on ith row
PEGS_PER_ROW = [1, 2, 3, 4, 13, 12, 11, 10, 9, 10, 11, 12, 13, 4, 3, 2, 1]

def get_center(box): 
    x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
    center_x, center_y = (x2 - x1) / 2 + x1, (y2 - y1) / 2 + y1
    return center_x, center_y

boxes.sort(key=lambda b: get_center(b)[1])
board = []

def add_row(boxes, row_num, board): 
    row = [Peg(Point(i, row_num), False, None, 'white') for i in range(MAX_PEGS_PER_ROW)]
    boxes.sort(key=lambda b: get_center(b)[0])

    start_ind = CENTER_COL - len(boxes)

    for i in range(len(boxes)): 
        x = start_ind + (i * 2)
        is_empty = class_names[int(boxes[i].cls[0])] == EMPTY
        color = 'black' if is_empty else class_names[int(boxes[i].cls[0])]
        row[x] = Peg(Point(x, row_num), True, is_empty, color)

    board.append(row)

def invert_board(board): 
    board = reversed(board)
    for row in board: 
        for peg in row: 
            peg.position.y = abs(NUM_ROWS - 1 - peg.position.y)

for i in range(NUM_ROWS): 
    num_boxes_before = sum(PEGS_PER_ROW[:i])
    boxes_that_row = boxes[num_boxes_before : num_boxes_before + PEGS_PER_ROW[i]]
    add_row(boxes_that_row, i, board)

invert_board(board)

def display_board(self):
    colors = []
    x_coords = []
    y_coords = []
    for row in board: 
        for peg in row: 
            colors.append(peg.color)
            x_coords.append(peg.position.x)
            y_coords.append(peg.position.y)

    # Plot the points with their colors
    plt.scatter(x_coords, y_coords, c=colors)
    plt.xlabel('X-axis')
    plt.xticks(list(range(25)))
    plt.ylabel('Y-axis')
    plt.yticks(list(range(17)))
    plt.title('Checker Board Visualization')
    plt.grid()
    plt.show()

display_board(board)

# cv2.waitKey(0)



# print(sorted(list(confidences), reverse=True))
# print([box.conf[0] for box in boxes])
# boxes.sort(key=lambda box: float(box.conf[0]))
# print([box.conf[0] for box in boxes])
# print(list(map(lambda box: box.conf[0], boxes)))

# count = 0

# boxes = result.boxes
# print(f'\n{len(boxes)}/{TOTAL_PEGS} entities detected')
# print(f'Smallest confidence: {min(boxes, key=lambda box: box.conf[0]).conf[0]}\n')
# for box in boxes:

#     count += 1
#     x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
#     center_x, center_y = (x2 - x1) / 2 + x1, (y2 - y1) / 2 + y1
#     class_id = box.cls[0]
#     confidence = int(box.conf[0] * 100) / 100

#     # if count >= 100: 

#     if class_names[int(class_id)] == 'Blue': 

#         x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
#         center_x, center_y = (x2 - x1) / 2 + x1, (y2 - y1) / 2 + y1
#         class_id = box.cls[0]
#         confidence = int(box.conf[0] * 100) / 100

#         print(f'Ball {class_names[int(class_id)]} {count}: {(center_x, center_y)}. Confidence: {confidence}')

#         cvzone.cornerRect(image, bbox=(x1, y1, x2 - x1, y2 - y1))

#         # confidence = int(box.conf[0] * 100) / 100
#         # cvzone.putTextRect(image, str(confidence), (max(0, x1), max(20, y1 - 20)))

#         cvzone.putTextRect(image, f"{class_names[int(class_id)]}", (max(0, x1), max(20, y1 - 20)), scale=2, thickness=2)

#         cv2.imshow("Detection Results", image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()

# Display the result
# cv2.imshow("Detection Results", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()