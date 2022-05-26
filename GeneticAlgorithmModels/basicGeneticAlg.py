# Raviv Haham, 208387951
# Peleg Haham, 208387969

import abc
from abc import ABC
from random import randint, random
import random
import numpy as np
from gui import PyGui


#Creates a new row with the valid values (1 to N) so that in the fixed places of the screen the given values will be there
def createValidLine(self, lineIndex):
    line = []
    valueOptions = np.arange(1, self.numOfColumns + 1)
    legalValueOptions = [x for x in valueOptions if x not in self.givenCellsArray[lineIndex][1]]
    valueOptions = legalValueOptions
    for j in range(self.numOfColumns):
        if j in self.givenCellsArray[lineIndex][0]:
            line.append(None)
        else:
            value = random.choice(valueOptions)
            line.append(value)
            valueOptions.remove(value)
    return line


# Creates a new bestSolution with the valid values (1 to N, N times) so that in the fixed places of the screen the given values will be there
def createRandMetrix(self):
    solutionToReturn = []
    valueOptions = np.arange(1, self.numOfColumns + 1)
    optionsArray = []
    for val in valueOptions:
        for newLine in range(self.numOfRows):
            optionsArray.append(val)

    for i in range(self.numOfRows):
        for valToDel in self.givenCellsArray[i][1]:
            optionsArray.remove(valToDel)

    for i in range(self.numOfRows):
        line = []
        for j in range(self.numOfColumns):
            if j in self.givenCellsArray[i][0]:
                line.append(None)
            else:
                value = random.choice(optionsArray)
                line.append(value)
                optionsArray.remove(value)
        solutionToReturn.append(line)
    return solutionToReturn


class GeneticAlgorithm(ABC):
    def __init__(self, grid):
        self.numberOfSolutions = 300
        self.mutationCellChance = 30
        self.mutationChance = 70
        self.crossoverChance = 30

        self.numOfColumns, self.numOfRows, self.givenCells, self.givenCellsArray, self.greaterCells = self.getMetrixData(grid)
        self.maxScore = (2 * self.numOfRows * self.numOfColumns) + len(self.greaterCells)
        self.chooseRandomSolIndex = 0
        self.prevBestScore = -99999999
        self.generationNumber = 0
        self.stuck = 0
        self.model = 1
        self.topFive = [None, None, None, None, None]
        self.topOneHundred = []
        for i in range(20):
            self.topOneHundred.append(None)
        self.generationArr = self.initFirstGen()
        self.bestScore = -99999999
        self.worstScore = 99999999
        self.averageScore = 0.0
        self.sumAllScore = 0
        self.bestScoreIndex = -1
        self.allScoresArr = self.evaluation()

    # create the first generationNumber using the "createRandMetrix" function so the function produces solutions according
    # to the amount of the solutions we have chosen to have (self.numberOfSolutions),so the generationNumber is represented
    # by an array of matrices
    def initFirstGen(self):
        firstGen = []
        for index in range(self.numberOfSolutions):
            currentMetrix = createRandMetrix(self)
            # set the values in the fixed places of the screen, so the given values will be there
            for i, j, givenNum in self.givenCells:
                currentMetrix[int(i) - 1][int(j) - 1] = givenNum
            firstGen.append(currentMetrix)
        return firstGen

    # Extract all the data from the text file that describes the state of the screen and all the constraints
    def getMetrixData(self, file):
        givenCells = []
        greaterCells = []
        # open the file to read it's content
        with open(file, 'r') as f:
            MetrixSize = f.readline().strip("\n")
            colSize = rowSize = int(MetrixSize)
            givenCellsArray = []
            for i in range(colSize):
                # append all the indexes of the given cells values to the "givenCellsArray" array
                givenCellsArray.append(([], []))
            givenDigitsAmount = f.readline().strip("\n")
            for i in range(int(givenDigitsAmount)):
                line = f.readline().strip("\n")
                currentGivenCell = []
                for char in line.split(" "):
                    if char != "0" and char != "":
                        currentGivenCell.append(int(char))
                givenCells.append(currentGivenCell)
            greaterAmount = f.readline().strip("\n")
            for i in range(int(greaterAmount)):
                line = f.readline().strip("\n")
                # append all the indexes of the given cells that needs to meet the constraint of greater than to
                # the "givenCellsArray" array
                currentGreaterCell = []
                for char in line.split(" "):
                    if char != "0" and char != "":
                        currentGreaterCell.append(int(char))
                greaterCells.append(currentGreaterCell)

            for i, j, givenNum in givenCells:
                (givenCellsArray[int(i) - 1])[0].append(int(j) - 1)
                (givenCellsArray[int(i) - 1])[1].append(givenNum)
            return colSize, rowSize, givenCells, givenCellsArray, greaterCells


    # Create a createMutation to a row by replacing two valid cells (cells not given in the screen) in this row
    def getRowMutation(self, line, lineIndex):
        mutationRow = line
        valueOptions = np.arange(0, self.numOfColumns)
        # create list of all the valid indexes in this row
        legalValueOptions = [x for x in valueOptions if x not in self.givenCellsArray[lineIndex][0]]
        valueOptions = legalValueOptions
        if len(valueOptions) >= 1:
            # random two cells from the legal list and swap them
            firstIndex = random.choice(valueOptions)
            secondIndex = random.choice(valueOptions)
            temp = line[secondIndex]
            mutationRow[secondIndex] = line[firstIndex]
            mutationRow[firstIndex] = temp
        return mutationRow


    # Creating a mutation for the given matrix by drawing a new valid value for each non-permanent cell (only
    # for cells not given in the screen) in a probability that was set
    def createMutation(self, metrixSolution):
        mutationMetrix = []
        # run over all the cells
        for i in range(0, self.numOfRows):
            newLine = []
            for j in range(0, self.numOfColumns):
                # create the mutation to the current cell only if the cell was not given in the screen
                if j not in self.givenCellsArray[i][0]:
                    # create the mutation to the current cell in a probability of "self.mutationCellChance
                    chanceToMutation = randint(0, 100)
                    if chanceToMutation <= self.mutationCellChance:
                        newLine.append(randint(1, self.numOfColumns))
                    else:
                        newLine.append(metrixSolution[i][j])
                else:
                    newLine.append(metrixSolution[i][j])
            mutationMetrix.append(newLine)

        # Check if all the numbers in the different cells of the matrix are valid (so the matrix has all the digits
        # from 1 to N and each number appears N times), if this is not the case we make a correction (by selecting
        # unnecessary cells and put the missing digits in their place)
        countArray = []
        for i in range(self.numOfRows):
            countArray.append(self.numOfColumns)

        for i in range(self.numOfRows):
            for j in range(self.numOfColumns):
                countArray[mutationMetrix[i][j] - 1] -= 1
        # check which numbers are missing and which numbers are duplicated
        numbersToAdd = []
        numbersToDel = []
        for i in range(len(countArray)):
            if countArray[i] < 0:
                for num in range(-1 * countArray[i]):
                    numbersToDel.append(i + 1)
            elif countArray[i] > 0:
                for num in range(countArray[i]):
                    numbersToAdd.append(i + 1)

        # swap between the missing numbers and the duplicated numbers
        while len(numbersToAdd) > 0:
            for i in range(0, self.numOfRows):
                for j in range(0, self.numOfColumns):
                    if ((j not in self.givenCellsArray[i][0]) and (mutationMetrix[i][j] in numbersToDel)):
                        numbersToDel.remove(mutationMetrix[i][j])
                        mutationMetrix[i][j] = numbersToAdd[0]
                        numbersToAdd.remove(mutationMetrix[i][j])
        return mutationMetrix


    # Creating a crossover for two matrices (solutions) by grilling a number between 1 and N, then creating a new
    # bestSolution where all the rows up to the randomize row number are from the first bestSolution, and the rows from the
    # randomize row number are from the second bestSolution. at the end Check if all the numbers in the different cells
    # of the matrix are valid (so the matrix has all the digits from 1 to N and each number appears N times), if
    # this is not the case we make a correction (by selecting unnecessary cells and put the missing in their place)
    def createCrossover(self, matrixTuple):
        # rand a row (random a number between 0 to N-1)
        randomRow = randint(0, self.numOfRows - 1)
        crossoverMetrix = []
        for i in range(0, randomRow):
            # insert a deep copy of the rows (until the randomRow) from the first matrix
            crossoverMetrix.append(matrixTuple[0][i].copy())
        for j in range(randomRow, self.numOfRows):
            # insert a deep copy of the rows (from the randomRow) from the second matrix
            crossoverMetrix.append(matrixTuple[1][j].copy())

        # Check if all the numbers in the different cells of the matrix are valid (so the matrix has all the digits
        # from 1 to N and each number appears N times), if this is not the case we make a correction (by selecting
        # unnecessary cells and put the missing digits in their place)
        countArray = []
        for i in range(self.numOfRows):
            countArray.append(self.numOfColumns)

        for i in range(self.numOfRows):
            for j in range(self.numOfColumns):
                countArray[crossoverMetrix[i][j] - 1] -= 1

        # check which numbers are missing and which numbers are duplicated
        numbersToAdd = []
        numbersToDel = []
        for i in range(len(countArray)):
            if countArray[i] < 0:
                for num in range(-1 * countArray[i]):
                    numbersToDel.append(i + 1)
            elif countArray[i] > 0:
                for num in range(countArray[i]):
                    numbersToAdd.append(i + 1)

        # swap between the missing numbers and the duplicated numbers
        while len(numbersToAdd) > 0:
            for i in range(0, self.numOfRows):
                for j in range(0, self.numOfColumns):
                    if ((j not in self.givenCellsArray[i][0]) and (crossoverMetrix[i][j] in numbersToDel)):
                        numbersToDel.remove(crossoverMetrix[i][j])
                        crossoverMetrix[i][j] = numbersToAdd[0]
                        numbersToAdd.remove(crossoverMetrix[i][j])
        return crossoverMetrix



    # Randomize a matrix (bestSolution) from the previous generationNumber, so that a bestSolution with a higher score will be
    # choosen with a higher chance
    def getRandomMatrix(self):
        # keep random until a bestSolution will be chosen
        while True:
            # select the current bestSolution with chance of "the score of the bestSolution" divide the "max score"
            isSelected = np.random.choice([0, 1], p=[
                1 - (self.allScoresArr[self.chooseRandomSolIndex] / (self.maxScore - self.worstScore)),
                (self.allScoresArr[self.chooseRandomSolIndex] / (self.maxScore - self.worstScore))])
            if isSelected:
                choosenVal = self.chooseRandomSolIndex
                self.chooseRandomSolIndex = (self.chooseRandomSolIndex + 1) % self.numberOfSolutions
                return choosenVal
            self.chooseRandomSolIndex = (self.chooseRandomSolIndex + 1) % self.numberOfSolutions



    # Return the grade of the current matrix (bestSolution)
    def getGrade(self, solution):
        grade = 0
        # Runs over all the rows and checks how many different numbers there are, and adds this number to the grade
        for i in range(self.numOfRows):
            tempSet = set()
            for j in range(self.numOfColumns):
                tempSet.add(solution[i][j])
            grade += len(tempSet)
        # Runs over all the columns and checks how many different numbers there are, and adds this number to the grade
        for j in range(self.numOfColumns):
            tempSet = set()
            for i in range(self.numOfRows):
                tempSet.add(solution[i][j])
            grade += len(tempSet)
        # Checks all the inequality constraints (big equal constraints), raises a point to the grade if the constraint
        # is met, otherwise lowers a point
        for iBig, jBig, iSmall, jSmall in self.greaterCells:
            if solution[iBig - 1][jBig - 1] > solution[iSmall - 1][jSmall - 1]:
                grade += 1
            else:
                grade -= 1
        return grade


    # Returns the evaluation of the current generationNumber (by calling to "getGrade" functin for each bestSolution in
    # the generationNumber)
    def getEvaluation(self):
        allScoresArr = []
        self.sumAllScore = 0
        self.bestScoreIndex = -1
        indexOfSolution = 0
        # run over all the solutions of the current generationNumber
        for solution in self.generationArr:
            currentGrade = self.getGrade(solution)
            self.sumAllScore = self.sumAllScore + currentGrade
            allScoresArr.append(currentGrade)

            # Update the worst grade and the best grade for this generationNumber
            if self.bestScore < currentGrade:
                self.bestScore = currentGrade
                self.bestScoreIndex = indexOfSolution
            if self.worstScore > currentGrade:
                self.worstScore = currentGrade
            indexOfSolution += 1
        # calculate the average of all the grades of the solutions of this generationNumber
        self.averageScore = int(self.sumAllScore / self.numberOfSolutions)
        # save the top five and top 20 indexes that get the max grade
        self.topFive = np.argpartition(allScoresArr, -5)[-5:]
        self.topOneHundred = np.argpartition(allScoresArr, -20)[-20:]
        # normalized by the smallest grade (by the worst score)
        self.sumAllScore -= self.worstScore * self.numberOfSolutions
        for i in range(self.numberOfSolutions):
            allScoresArr[i] -= self.worstScore
        return allScoresArr


    # create a new generationNumber by using the old generationNumber
    def initNewGen(self, generation):
        newGen = []
        # if the grade was stuck for 100 generations or more, take all the best five solutions from the previous
        # generationNumber to the new generationNumber, otherwise take only the best bestSolution of the matrix
        if self.stuck < 100:
            for currentTopIndex in self.topFive:
                newGen.append(self.generationArr[currentTopIndex])
        else:
            newGen.append(self.generationArr[self.bestScoreIndex])

        # To address the problem of early convergence we have determined that after 600 generations,
        # every 150 generations we will add 100 new solutions (which have been crossOver with the 20 best
        # solutions) to the new generationNumber
        if generation >= 600:
            if generation % 150 == 0:
                for index in range(100):
                    currentMetrix = createRandMetrix(self)
                    for i, j, givenNum in self.givenCells:
                        currentMetrix[int(i) - 1][int(j) - 1] = givenNum
                    matrixTuple = [currentMetrix, self.generationArr[self.topOneHundred[index % 20]]]
                    new_sol = self.createCrossover(matrixTuple)
                    newGen.append(new_sol)

        # insert more solutions to the new generationNumber until the new generationNumber will contain
        # "self.numberOfSolutions" solutions
        while len(newGen) < self.numberOfSolutions:
            randIndex = self.getRandomMatrix()
            currentNewSolutio  = self.generationArr[randIndex]
            # create the crossover to the current cells in a probability of "self.crossoverChance"
            chanceToCrossover = randint(0, 100)
            if chanceToCrossover < self.crossoverChance:
                crossoverNewSolutio = self.generationArr[self.getRandomMatrix()]
                matrixTuple = [currentNewSolutio, crossoverNewSolutio]
                currentNewSolutio = self.createCrossover(matrixTuple)
            # create the mutation to the current cell in a probability of "self.mutationCellChance"
            chanceToMutation = randint(0, 100)
            if chanceToMutation < self.mutationChance:
                currentNewSolutio = self.createMutation(currentNewSolutio)
            newGen.append(currentNewSolutio)
        return newGen

    # Create a new generationNumber (based on the previous generationNumber) by using "self.initNewGen" function and
    # perform one game step
    def playOneGeneration(self):
        # create the Futoshiki game screen
        futoshikiBoard = PyGui(self.numOfRows, self.numOfColumns)
        # initialize the generationNumber number to 0
        self.generationNumber = 0
        # initialize arrays of the best scores and average scores per generation
        bestScoresArr = []
        averageScoresArr = []
        # we want to run until the self.bestScore will be equals to the self.maxScore (until we solve the current
        # Futoshiki game problem)
        while self.bestScore < self.maxScore:
            self.generationNumber += 1
            self.allScoresArr = self.evaluation()
            self.generationArr = self.initNewGen(self.generationNumber)

            # In the case of a solving acorrding the Darwin method we want to recalculate all the scores after we create
            # the ney generationNumber so all the changes will not be saved
            if (self.model == 2):
                self.allScoresArr = self.getEvaluation()

            # insert values for the arrays of the best scores and average scores per generation
            bestScoresArr.append(self.bestScore)
            averageScoresArr.append(self.averageScore)

            # print the futoshiki screen and all the other information
            futoshikiBoard.printBestMatrix(self.generationArr[self.bestScoreIndex], self.generationNumber, self.bestScore,
                                           self.averageScore, self.worstScore, self.maxScore)

            # count how many times the score is stuck
            if self.bestScore != self.prevBestScore:
                self.stuck == 0
                self.prevBestScore = self.bestScore
            else:
                self.stuck += 1

            # change the chance to do crossover and the chance to do mutation every 1200 generations so the genetic
            # algorithm won't be stuck on local max
            if self.generationNumber % 1200 < 20:
                self.crossoverChance = 60
                self.mutationChance = 60
                self.mutationCellChance = 50

            # change the chance to do crossover and the chance to do mutation (for 10 generations) if the score doesn't
            # change for 100 generations so the genetic algorithm won't be stuck on local max
            elif self.stuck >= 100:
                # self.crossoverChance = 70
                self.mutationCellChance = 40

                if self.stuck >= 110:
                    self.stuck = 0

            else:
                self.crossoverChance = 10
                self.mutationChance = 15
                self.mutationCellChance = 30

            # stop running after 3000 generations
            if self.generationNumber == 3000:
                return bestScoresArr, averageScoresArr

        # if the self.bestScore will be equals to the self.maxScoreit means we solve the current Futoshiki game problem
        # so we want to stop running the algorithm
        futoshikiBoard.isPause = True
        futoshikiBoard.stopFunc()
        return bestScoresArr, averageScoresArr

    @abc.abstractmethod
    def evaluation(self):
        raise NotImplementedError