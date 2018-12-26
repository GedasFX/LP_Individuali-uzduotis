# Individuali Užduotis IFF-6/2 Gediminas Milašius

from multiprocessing import Process, Queue

# Contains 2 fields: Element of any type and an integer count
class Data:
    def __init__(self, element, count):
        self.element = element
        self.count = count
    def __str__(self):
        return self.element + ": " + str(self.count)
    def __repr__(self):
        return self.__str__()

# Identifies data to be written or read and provides the element
class Pass:
    def __init__(self, element, read):
        self.element = element
        self.read = read
    def __str__(self):
        return "Remove " + self.element
    def __repr__(self):
        return self.__str__()

# ==== Methods for modifying data array ====
class DataMonitor:
    def __init__(self):
        self.data = [None] * 100
        self.count = 0

    def __str__(self):
        return str(self.data[:self.count])

    # Adds an element to data array
    def add(self, element):
        for i in range(100):
            # If element is below search criteria
            if self.data[i] != None and self.data[i].element < element:
                continue
            
            # Spot found? Check if item exists.
            if self.data[i] == None or self.data[i].element == element:
                # If item is at the end of the list
                if self.data[i] == None:
                    self.data[i] = Data(element, 0)
                    self.count = self.count + 1
                # Element exists, add to it.
                self.data[i].count = self.data[i].count + 1
            # Element needs to squeezed in
            elif self.data[i].element > element:
                for j in range(self.count, i, -1):
                    self.data[j] = self.data[j - 1]

                self.data[i] = Data(element, 1)
                self.count = self.count + 1
            break
        return True

    # Removes an element from data array
    def remove(self, element):
        for i in range(100):
            # If element below search criteria
            if self.data[i] != None and self.data[i].element < element:
                continue

            # End of list or element doesn't exist
            if self.data[i] == None or self.data[i].element > element:
                return False

            # Element found. Remove
            if self.data[i].count > 1:
                self.data[i].count = self.data[i].count - 1
            else:
                # Shift all elements left.
                for j in range(i, self.count):
                    self.data[j] = self.data[j + 1]

                self.data[self.count] = None
                self.count = self.count - 1
            return True

        # Array is full and/or element doesn't exist
        return False
# ==== Methods for modifying data array ====

# Read the file and output it as 3d array: [W/R index][Group Index][Element Index]
def readFile(path):
    result = [[], []]
    file = open(path, "r")
    # Defines if group is writing (0) or reading (1). K = W/R index
    for k in range(2):
        # Iterate trough all groups for reading/writing. I = Group ID
        for i in range(int(file.readline())):
            result[k].append([])
            # Iterate through all elements of a particular group. J = Element ID
            for _ in range(int(file.readline())):
                line = file.readline().split(' ')
                result[k][i].append(Data(line[0], int(line[1])))
    file.close()
    return result

# ==== Parallel processes ====
# Manager process. Has access to the data structure. Is given the amount of processes to do the job
def manager(qData, qLog, qRes, cWorkers):
    completedCnt    = 0     # Worker processes, which have finished work
    unfinishedBuf   = []    # Overflow buffer to be dealt with after all elements have been added.
    data = DataMonitor()
    # While changes are possible
    while completedCnt < cWorkers:
        el = qData.get()
        if el is None:
            completedCnt = completedCnt + 1
            continue

        if el.read:
            if data.remove(el.element):
                qLog.put("Successfully removed \"" + el.element + "\".")
            else:       
                unfinishedBuf.append(el.element)
                qLog.put("Failed to remove \"" + el.element + "\". Will retry later.")
        else:
            data.add(el.element)
            qLog.put("Successfully added \"" + el.element + "\".")
    # At this point no new elements can be added to the array, only removed.
    # Program can continue exectution in serial as input is ignored.
    for element in unfinishedBuf:
        if data.remove(element):
            qLog.put("Successfully removed \"" + element + "\".")
        else:
            qLog.put("Invalid input file. Duplicate \"" + element + "\" detected. Element will be ignored")

    # Array is final, return to main thread
    qRes.put(data.count) # Elements in array remaining
    for el in data.data:
        if el is None:
            break
        qRes.put(el)
    qLog.put(None) # Stop logger

# Logger process. Logs manager actions
def logger(q):
    while True:
        line = q.get()
        if line == None:
            break
        else:
            print(line)

# Worker process. Writes/Reads messages to the manager process. Has initial data to provide. Type defines the type: False - writer, True - reader
def worker(q, dat, read):
    for entry in dat:
        for _ in range(entry.count):
            q.put(Pass(entry.element, read))
    q.put(None)
# ==== Parallel processes ====

# Starts processes with correct initial conditions
def startProcesses(processes, rawData, qData):
    processes[0].start()
    processes[1].start()

    for group in rawData[0]:
        processes[2].append(Process(target = worker, args = (qData, group, False))) # Writers
    for group in rawData[1]:
        processes[3].append(Process(target = worker, args = (qData, group, True))) # Readers

    for process in processes[3]:
        process.start()
    for process in processes[2]:
        process.start()

# Main function
if __name__ == "__main__":
    rawData = readFile("IFF-6-2_MilasiusG_IP_dat_14.txt")
    # Data transfer queues. Many2One qData
    qData = Queue()
    qResult = Queue()
    qLog = Queue()

    # Create and start processes
    processes = [ # Manager process [0], logger process [1], an array of write processes [2], and an array of read ones [3] + len(rawData[1])
        Process(target = manager, args = (qData, qLog, qResult, len(rawData[0]) + len(rawData[1]),)), # Ambiguous variable = worker count
        Process(target = logger, args = (qLog,)), [], []
    ] 
    startProcesses(processes, rawData, qData)

    # Get final result of the data streams
    resArr = []
    count = qResult.get() # First result is quantity
    for i in range(count):
        resArr.append(qResult.get())