class Data:
    def __init__(self, element, amount):
        self.element = element
        self.amount = amount
    def __str__(self):
        return self.element + ": " + str(self.amount)
    def __repr__(self):
        return self.__str__()

list = [None] * 100
print(list)
list.append(Data("Vienas", 1))
print(list)