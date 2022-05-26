# Raviv Haham, 208387951
# Peleg Haham, 208387969

from GeneticAlgorithmModels.basicGeneticAlg import GeneticAlgorithm

# the basic genetic algorithm class
class generalGeneticAlgorithm(GeneticAlgorithm):

    # overload the "evaluation" function as it should be implemented in the basic genetic algorithm case
    def evaluation(self):
        # return the fitness grade for the solutions in the current generationNumber array
       return self.getEvaluation()
