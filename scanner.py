import cv2 # OpenCV 4.4.0
import numpy as np
from imutils import perspective
from skimage.segmentation import clear_border
from network import SudokuCNN

# Inspiration for computer vision/digit extraction from tutorial on
# https://www.pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/

def extract_digit(cell:np.array, debug=False):
    # Apply automatic thresholding to cell and then clear any
    # connected borders that touch border of cell
    img_thresh = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    img_thresh = clear_border(img_thresh)
    
    if debug:
        cv2.imshow("Cell Thresh", img_thresh)
        cv2.waitKey(0)

    # Find contours in thresholded cell -> contour of number
    contours, _ = cv2.findContours(img_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If no contours were found -> empty cell
    if len(contours) == 0:
        return None
	
    # Find largest contour in  cell and create a mask for the contour
    c = max(contours, key=cv2.contourArea)
    mask = np.zeros(img_thresh.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)

    # Compute percentage of masked pixels relative to the total area of image
    (h, w) = img_thresh.shape
    percent_filled = cv2.countNonZero(mask) / float(w * h)
	
    # If masks fills less than 3% of cell area -> noise -> ignore
    if percent_filled < 0.03:
        return None
	
    # Apply the mask to the thresholded cell
    img_digit = cv2.bitwise_and(img_thresh, img_thresh, mask=mask)
	
    if debug:
        cv2.imshow("Digit", img_digit)
        cv2.waitKey(0)

    # Return the digit to the calling function
    return img_digit


def find_sudoku(image:str, debug=False):
    # Convert image to grayscale and add blur
    img = cv2.imread(image)
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.GaussianBlur(img_gray, (7, 7), 3)

    # Apply inverted binary adaptive thresholding 
    img_thresh = cv2.adaptiveThreshold(img_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    if debug:
	    cv2.imshow("Sudoku with Threshold Filter", img_thresh)
	    cv2.waitKey(0)

    # Find countours in thresholded image
    contours, _ = cv2.findContours(img_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True) # largest contour is first element

    # Find outer contour
    sudoku_contour = None
    for c in contours:
        # Approximation of contour
        perimeter = cv2.arcLength(c, True)
        approximation = cv2.approxPolyDP(c, 0.02*perimeter, True) # use perimeter of contour for approximation accuracy

        # Assume the first contour with 4 points to be the outline of the grid
        if len(approximation) == 4:
            sudoku_contour = approximation
            break

    # No outline found
    if sudoku_contour is None:
        raise Exception("Could not find Sudoku grid outline.")

    # Show debug output
    if debug:
        output = img.copy()
        cv2.drawContours(output, [sudoku_contour], -1, (0, 255, 0), 2)
        cv2.imshow("Sudoku Outline", output)
        cv2.waitKey(0)

    # Apply four point perspective transform to obtain a top-down perspective
    img_sudoku = perspective.four_point_transform(img, sudoku_contour.reshape(4, 2))
    img_gray = perspective.four_point_transform(img_gray, sudoku_contour.reshape(4, 2))

    if debug:
	    cv2.imshow("Sudoku Transform", img_sudoku)
	    cv2.waitKey(0)
	
    # Return a tuple of Sudoku in both RGB and grayscale
    return (img_sudoku, img_gray)

def show_cells(cells:list):
    n_cells = 0
    for r in range(9):
        for c in range(9):
            if not cells[c][r] is None:
                n_cells += 1
                cv2.imshow("Digit", cells[c][r])
                cv2.waitKey(0)
    print(n_cells)

def cells_to_board(cells:list) -> list:
    # Use neural network to predict digit
    # Create 2d array containing given numbers and 0 for empty fields
    
    # Load CNN model
    cnn = SudokuCNN("CNN/sudoku_cnn")

    sudoku = []
    for r in range(9):
        row = []
        for c in range(9):
            # Get image of digit
            digit = cells[r][c]

            if digit is None:
                row.append(0)
            else:
                row.append(cnn.predict(digit))
        sudoku.append(row)

    return sudoku
   

def convert_image_to_board(image:str):
    # Find Sudoku in image
    (sudoku, sudoku_gray) = find_sudoku(image, False)

    # Estimate cell width and height
    cell_width = sudoku.shape[1] // 9
    cell_height = sudoku.shape[0] // 9

    # Loop through cells and extract images
    cells = []
    for r in range(9):
        row = []
        for c in range(9):
            x_start = c * cell_width
            x_end = (c+1) * cell_width
            y_start = r * cell_height
            y_end = (r+1) * cell_height

            # Crop cell
            cell = sudoku_gray[y_start:y_end, x_start:x_end]
            digit = extract_digit(cell, False)
            row.append(digit)
        cells.append(row) 

    return cells_to_board(cells)

