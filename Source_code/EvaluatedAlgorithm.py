
from EvaluationData import EvaluationData

class EvaluatedAlgorithm:
    
    def __init__(self, algorithm, name):
        self.algorithm = algorithm
        self.name = name
    
    def GetName(self):
        return self.name
    
    def GetAlgorithm(self):
        return self.algorithm
    
    
