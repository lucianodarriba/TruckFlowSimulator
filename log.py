class Log():
    def __init__(self):
        self.logRecords = []

    def enterLogRegister(self, register):
        self.logRecords.append(register)

    def outputLog(self):
        for line in self.logRecords:
            print(line)