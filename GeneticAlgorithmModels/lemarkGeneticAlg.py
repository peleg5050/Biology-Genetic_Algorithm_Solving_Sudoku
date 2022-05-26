# Raviv Haham, 208387951
# Peleg Haham, 208387969

from GeneticAlgorithmModels.basicGeneticAlg import GeneticAlgorithm

# the Lemark algorithm class- each bestSolution undergoes optimization and its fitness is determined only after the
# optimization, and the next generationNumber is created according to the original bestSolution after the optimization.
class LemarkGeneticAlgorithm(GeneticAlgorithm):

    # Create optimization for the current bestSolution
    def optimizeSolution(self, currentSolution):
        # Create a deep copy for the current bestSolution
        copySol = []
        for i in range(0, self.numOfRows):
            copySol.append(currentSolution[i].copy())

        # we allow only amount of num rows optimization to do
        amountOptimizationsLeft = self.numOfRows
        # Create an array of all cells that do not meet the constraint of inequality
        indexToReplace = []
        for iBig, jBig, iSmall, jSmall in self.greaterCells:
            if currentSolution[iBig - 1][jBig - 1] <= currentSolution[iSmall - 1][jSmall - 1]:
                indexToReplace.append((iBig, jBig, iSmall, jSmall))

        index = 0
        while amountOptimizationsLeft > 0:
            # Attempt to replace two cells that did not meet the constraint of inequality out of the array of all
            # cells that did not meet the constraint of inequality
            if (len(indexToReplace) > 0) and (index < len(indexToReplace)):
                iBig = indexToReplace[index][0] - 1
                jBig = indexToReplace[index][1] - 1
                iSmall = indexToReplace[index][2] - 1
                jSmall = indexToReplace[index][3] - 1
                # The exchange between the cells is performed only if none of them is a fixed cell
                if (jBig not in self.givenCellsArray[iBig][0]) and (jSmall not in self.givenCellsArray[iSmall][0]):
                    gradeWithoutOptimize = self.getGrade(copySol)
                    temp = copySol[iBig][jBig]
                    copySol[iBig][jBig] = copySol[iSmall][jSmall]
                    copySol[iSmall][jSmall] = temp
                    gradeWithOptimize = self.getGrade(copySol)
                    # Check if the optimization didn't improve the grade of the bestSolution
                    if gradeWithOptimize < gradeWithoutOptimize:
                        temp = copySol[iBig][jBig]
                        copySol[iBig][jBig] = copySol[iSmall][jSmall]
                        copySol[iSmall][jSmall] = temp
                    else:
                        # if we made the swipe we want to count it as a change therefore we will lower the
                        # "amountOptimizationsLeft" counter by 1
                        amountOptimizationsLeft -= 1
                    index += 1
            amountOptimizationsLeft = 0
        return copySol

    # create the optimization for all the solutions in the current generationNumber array
    def optimizeGeneration(self):
        optimizeGenerationArr = []
        # run over all the solutions in the current generationNumber array and call to   function
        for currentSolution in self.generationArr:
            optimizeSolution = self.optimizeSolution(currentSolution)
            optimizeGenerationArr.append(optimizeSolution)
        return optimizeGenerationArr

    # overload the "evaluation" function as it should be implemented in the Lemark algorithm case
    def evaluation(self):
        # set the "self.model" value to 3, to sign that this is the Lemark algorithm case
        self.model = 3
        # create the optimization for the solutions in the current generationNumber array,and replace the previous generationNumber
        self.generationArr = self.optimizeGeneration()
        # return the fitness grade after all the optimizations for the solutions in the current generationNumber array
        return self.getEvaluation()
