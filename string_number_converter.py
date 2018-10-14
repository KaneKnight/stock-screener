class StringNumberConverter():
    def __init__(self, numberAsString):
        self.numberAsString = numberAsString

    def convert(self):
        number = self.numberAsString[0:-1]
        letter = self.numberAsString[-1]
        if letter == "B":
            return float(number) * 1000
        if letter == "M":
            return float(number)