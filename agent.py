from abc import ABC, abstractmethod

class Agent(ABC):
    @abstractmethod
    def move(self, board):
        """ Choose a move to make from a given board state """
        pass