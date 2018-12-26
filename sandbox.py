from multiprocessing import Process, Queue

class Data:
    def __init__(self, element, amount):
        self.element = element
        self.amount = amount
    def __str__(self):
        return self.element + ": " + str(self.amount)
    def __repr__(self):
        return self.__str__()

def add(q):
    print("a")
    d = q.get()
    print("b")
    q.put(d)
    print("c")
    d = q.get()
    print("d")
    q.put(d)

if __name__ == '__main__':
    q = Queue()
    a = []
    print(1)
    p = Process(target = add, args = (q,))
    print(2)
    p.start()
    print(3)
    q.put(0)
    p.join()
    print(4)
    print(q.get())
    print(len(a))