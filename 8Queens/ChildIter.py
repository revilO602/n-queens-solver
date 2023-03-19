# Class used to iterate over child states of parent state given to constructor
class ChildIter:

    def __init__(self, state, size):
        self.parent = state
        self.prev = state   # Previously generated state
        # Variable used to determine what column we're on and which direction we're generating
        # if status % 2 == 0 we are going down in the column else we are going up and status // 2 = column index
        self.status = 0
        self.max = size-1

    def __iter__(self):
        return self

    # Reset this column and update status
    def reset_column(self, next, pos):
        self.status += 1
        next[pos] = self.parent[pos]
        self.prev = next

    # Generates next child state based on previously generated child state and status
    def __next__(self):
        pos = self.status // 2
        next = self.prev.copy()
        if pos > self.max:
            raise StopIteration
        if self.status % 2 == 0:
            if next[pos] == 0:
                self.reset_column(next, pos)
                return self.__next__()
            else:
                next[pos] -= 1
        else:
            if next[pos] == self.max:
                self.reset_column(next, pos)
                return self.__next__()
            else:
                next[pos] += 1
        self.prev = next
        return next
