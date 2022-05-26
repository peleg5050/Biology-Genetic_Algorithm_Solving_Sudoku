# Raviv Haham, 208387951
# Peleg Haham, 208387969

import pygame
import sys

# The screen pygame class
class PyGui:
    pygame.display.set_caption('Futoshiki')
    # set isPause value to false so the game will run
    isPause = False
    # set the size of each cell to be 40
    cellSize = 40
    backgroundColor = (236, 126, 22)

    # initialize the pygame screen board
    def __init__(self, numOfRows, numOfColumns):
        self.numOfRows = numOfRows
        self.numOfColumns = numOfColumns
        pygame.init()
        size = (self.width, self.height) = (self.numOfColumns * self.cellSize) + 200, (self.numOfRows * self.cellSize) + 200
        self.screen = pygame.display.set_mode(size)


    # if the user press on the pause button we want to stop the genetic algorithm in this current iteration and set
    # isPause to true
    def stopFunc(self):
        while (self.isPause):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isPause = False

    # print the futoshiki screen and all the other information
    def printBestMatrix(self, bestSolution, generationNumber, bestScore, averageScore, worstScore, maxScore):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.isPause = True
                    self.stopFunc()

        # set the background color screen
        self.screen.fill(self.backgroundColor)
        # set the font and the color of the text
        textFont = pygame.font.SysFont('comicsansms', 20)
        textColor = pygame.Color('blue')
        # create a txtSurface for each row and write the text
        txtSurface = textFont.render("Generation: " + str(generationNumber), True, textColor)
        self.screen.blit(txtSurface, (self.screen.get_height() / 2 - 30, 5))
        # set the font and the color of the text
        textFont = pygame.font.SysFont('Helvetica', 17)
        textColor = pygame.Color('black')
        txtSurface = textFont.render("Best: " + str(bestScore) + " (out of " + str(maxScore) + " )", True, textColor)
        self.screen.blit(txtSurface, (15, 10))
        txtSurface = textFont.render("Average: " + str(averageScore), True, textColor)
        self.screen.blit(txtSurface, (15, 30))
        txtSurface = textFont.render("Worst: " + str(worstScore), True, textColor)
        self.screen.blit(txtSurface, (15, 50))

        # draw all the board
        for i in range(self.numOfColumns):
            for j in range(self.numOfRows):
                # set the location of the number of each cell
                cellXLocation = i * self.cellSize + 150
                cellYLocation = j * self.cellSize + 150
                # set the font and the color of the text
                textFont = pygame.font.Font(None, 25)
                textColor = pygame.Color('black')
                txtSurface = textFont.render(str(bestSolution[j][i]), True, textColor)
                self.screen.blit(txtSurface, (cellXLocation + 12, cellYLocation + 12))
                pygame.draw.line(self.screen, (20, 20, 20), (cellXLocation, cellYLocation), (cellXLocation, cellYLocation + self.cellSize))
                pygame.draw.line(self.screen, (20, 20, 20), (cellXLocation, cellYLocation), (cellXLocation + self.cellSize, cellYLocation))
            pygame.draw.line(self.screen, (20, 20, 20), (cellXLocation + self.cellSize, cellYLocation + self.cellSize), (cellXLocation + self.cellSize , cellYLocation - (self.numOfRows - 1) * self.cellSize))
            pygame.draw.line(self.screen, (20, 20, 20), (cellXLocation, cellYLocation + self.cellSize), (cellXLocation + self.cellSize, cellYLocation + self.cellSize))
        pygame.display.update()