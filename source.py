# Individuali Užduotis IFF-6/2 Gediminas Milašius

# Contains 2 fields: Element of any type and an integer count
class Data:
    def __init__(self, element, count):
        self.element = element
        self.count = count
    def __str__(self):
        return self.element + ": " + str(self.count)
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
# ==== Methods for modifying array _data and field _count ====



# Main function
def main():
    print("HW")

# Run the program
main()