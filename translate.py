import cv2
import numpy as np
import os
import settings
from settings import *
class Translator:
    def __init__(self):
        self.base = settings.return_value("base")
        self.height = settings.return_value("height")
        self.square_size = settings.return_value("square_size")
        self.transformed_image_name = settings.return_value("transformed_image_name")
        self.matrix = None

    def setMatrix(self,new_matrix):
        self.matrix = new_matrix

    def returnMatrix(self):
        return self.matrix
    def return_transformed_image_name(self):
        return self.transformed_image_name
    def getChessboardCorners(self, image):
        settings.set_value("latest_caption", "Finding Chessboard Corners...")
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
            corners = cv2.approxPolyDP(contours[0], 0.01 * cv2.arcLength(contours[0], True), True)
            cornerPoints = np.array(corners, dtype='float32')
            return cornerPoints
        except:
            cornerPoints = np.array([[0, 0], [self.base, 0], [self.base, self.base], [0, self.base]], dtype='float32')
            return cornerPoints

    def removeBorder(self, fileName):
        settings.set_value("latest_caption", "Removing Border...")
        img = cv2.imread(f'{fileName}.png')
        img = img[50:850, 50:850]
        cv2.imwrite(f'{fileName}.png', img)

    def perspectiveTransform(self, image, matrix, fileName):
        settings.set_value("latest_caption", "Perspective Warping...")
        new_image = cv2.warpPerspective(image, matrix, (self.base, self.height))
        cv2.imwrite(f'{fileName}.png', new_image)

    def calculateMatrix(self, corners):
        settings.set_value("latest_caption", "Calculating Matrix...")
        cornerPoints = corners
        new_cornerPoints = np.array([[0, 0], [self.base, 0], [self.base, self.height], [0, self.height]], dtype='float32')
        matrix = cv2.getPerspectiveTransform(cornerPoints, new_cornerPoints)
        return matrix

    def translate(self, image, matrix, fileName):
        settings.set_value("latest_caption", "Translating the Chessboard...")
        self.perspectiveTransform(image, matrix, fileName)
        self.removeBorder(fileName)
        self.splitSquares(fileName)

    def splitSquares(self, fileName):
        settings.set_value("latest_caption", "Splitting the chessboard squares...")
        img = cv2.imread(f"{fileName}.png")
        squares = []
        dir_name = os.getcwd() + "\squares"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for i in range(0, img.shape[0], self.square_size):
            row = []
            for j in range(0, img.shape[1], self.square_size):
                square = img[i:i + self.square_size, j:j + self.square_size]
                row.append(square)
                cv2.imwrite(os.path.join(dir_name, f'{cols[j//self.square_size]}_{i//self.square_size+1}.png'), square)
            squares.append(row)

translator = Translator()
