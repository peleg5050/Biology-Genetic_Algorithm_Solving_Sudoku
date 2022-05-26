# Raviv Haham, 208387951
# Peleg Haham, 208387969

from GeneticAlgorithmModels.darwinGeneticAlg import DarwinGeneticAlgorithm
from GeneticAlgorithmModels.lemarkGeneticAlg import LemarkGeneticAlgorithm
from GeneticAlgorithmModels.generalGeneticAlg import generalGeneticAlgorithm
import sys
import numpy as np
import matplotlib.pyplot as plt

def main():
    # get the path of the Futoshiki screen game
    filePath = sys.argv[1]

    # create element of the general genetic algorithm class
    geneticAlg = generalGeneticAlgorithm(filePath)
    # start running the genetic algorithm to this Futoshiki screen game
    generalAlgBestScoresArr, generalAlgAverageScoresArr = geneticAlg.playOneGeneration()

    # create element of the Darwin genetic algorithm class
    geneticAlg = DarwinGeneticAlgorithm(filePath)
    # start running the genetic algorithm to this Futoshiki screen game
    darwinAlgBestScoresArr, darwinAlgAverageScoresArr = geneticAlg.playOneGeneration()

    # create element of the Lemark genetic algorithm class
    geneticAlg = LemarkGeneticAlgorithm(filePath)
    # start running the genetic algorithm to this Futoshiki screen game
    lemarkAlgBestScoresArr, lemarkAlgAverageScoresArr = geneticAlg.playOneGeneration()


    # create a graph to all the genetic algorithms of all the scores of the best solution in each generation
    # per the number of generations and show it
    plt.figure("Best Score Per Generation Graph")
    allIterations = np.arange(1, 3000 + 1)
    plt.title("FUTOSHIKI 6x6 BOARD - EASY")
    plt.xlabel('Generation Number')
    plt.ylabel('Best Score')
    plt.plot(allIterations, np.array(generalAlgBestScoresArr), label="Regular Genetic Algorithm")
    plt.plot(allIterations, np.array(darwinAlgBestScoresArr), label="Darwin Genetic Algorithm")
    plt.plot(allIterations, np.array(lemarkAlgBestScoresArr), label="Lamarck Genetic Algorithm")
    plt.legend()
    plt.show()



    # create a graph to all the genetic algorithms of all the average score of all the solutions in each generation
    # per the number of generations and show it
    plt.figure("Average Score Per Generation Graph")
    allIterations = np.arange(1, 3000 + 1)
    plt.title("FUTOSHIKI 6x6 BOARD - EASY")
    plt.xlabel('Generation Number')
    plt.ylabel('Average Score')
    plt.plot(allIterations, np.array(generalAlgAverageScoresArr), label="Regular Genetic Algorithm")
    plt.plot(allIterations, np.array(darwinAlgAverageScoresArr), label="Darwin Genetic Algorithm")
    plt.plot(allIterations, np.array(lemarkAlgAverageScoresArr), label="Lamarck Genetic Algorithm")
    plt.legend()
    plt.show()




main()
