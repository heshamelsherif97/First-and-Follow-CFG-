import re, argparse

class terminal:
    def __init__(self, name):
        self.name = name
        self.productions = []
        self.first = []
        self.firstTerminals = []
        self.follow = []
        self.hasEpsilon = False
        self.followList = []
        self.duplications = []

class Grammar:
    def __init__(self, parsed):
        self.terminals = []
        self.names = []
        self.grammarVariables = []
        self.handleParse(parsed)
        for i in self.terminals:
            self.names.append(i.name)
        self.intializeEpsilons()
        # self.getEpsilonExist()
        self.getFirst()
        self.filterFirst()
        self.getFollow()
        self.printResult()

    def filterFirst(self):
        for i in self.terminals:
            if i.hasEpsilon:
                i.first.append("epsilon")
                i.first = sorted(list(set(i.first)))
            if not i.hasEpsilon:
                if "epsilon" in i.first:
                    i.first.remove("epsilon")
                    i.first = sorted(list(set(i.first)))

    def printResult(self):
        output_file = open("task_5_1_result.txt", "w+")
        for i in self.terminals:
            firstString = i.name + " : " + " ".join(str(x) for x in i.first) + " : " + " ".join(str(x) for x in i.follow)
            output_file.write(firstString + "\n")

    def getFirst(self):
        for i in self.terminals:
            first = []
            for j in i.productions:
                if j[0] not in self.names:
                    first.append(j[0])
                else:
                    for t in j:
                        if t in self.names:
                            i.firstTerminals.append(t)
                            if not self.canEpsilon(t):
                                break
                        else:
                            first.append(t)
                            break
            i.first = first
        for i in self.terminals:
            for j in i.firstTerminals:
                if set(self.getFirstProd2(j)) not in set(i.firstTerminals) and self.getFirstProd2(j):
                    i.firstTerminals += self.getFirstProd2(j)
                    i.firstTerminals = list(set(i.firstTerminals))
        for i in self.terminals:
            for j in i.firstTerminals:
                i.first += self.getFirstProd(j)
        for i in self.terminals:
            i.first = sorted(list(set(i.first)))
        

    def getFollow(self):
        self.terminals[0].follow.append("$")
        for i in self.terminals:
            for j in i.productions:
                if j != "epsilon":
                    self.handleFollw(j, i.name)
        self.filterList()

        # for i in self.terminals:
        #     print(i.name)
        #     print(i.followList)
        #     print("----")
        while(not self.allHandeled()):
            for i in self.terminals:
                j = 0
                while j < len(i.followList):
                    if self.isHandled(i.followList[j]):
                        i.follow += self.getTerminal(i.followList[j]).follow
                        i.followList.remove(i.followList[j])
                    elif self.equalityCheck(i.followList, self.getTerminal(i.followList[j]).followList, i.name, i.followList[j]):
                        i.follow += self.getTerminal(i.followList[j]).follow
                        i.followList.remove(i.followList[j])
                    elif i.name in self.getTerminal(i.followList[j]).followList:
                        i.duplications += i.followList[j]
                        self.getTerminal(i.followList[j]).duplications += i.name
                        i.followList.remove(i.followList[j])
                    else:
                        j += 1
        self.handleDuplicates()
        self.filterFollow()    

    def handleDuplicates(self):
        for i in self.terminals:
            for j in i.duplications:
                i.duplications += self.getTerminal(j).duplications
                i.duplications = sorted(list(set(i.duplications)))
        for i in self.terminals:
            for j in i.duplications:
                i.follow += self.getTerminal(j).follow
                self.getTerminal(j).follow += i.follow

    def equalityCheck(self, i, j, name1, name2):
        if len(i) == len(j):
            if len(i) == 1:
                if i[0] == name2 and j[0] == name1:
                    return True
        return False

    def filterList(self):
        for i in self.terminals:
            i.followList = sorted(list(set(i.followList)))
        for i in self.terminals:
            for j in i.followList:
                if i.name == j:
                    i.followList.remove(j)


    def filterFollow(self):
        for i in self.terminals:
            i.follow = sorted(list(set(i.follow)))
            if 'epsilon' in i.follow:
                i.follow.remove('epsilon') 
   
    def isHandled(self, name):
        for i in self.terminals:
            if i.name == name:
                if i.followList:
                    return False
        return True

    def allHandeled(self):
        check = True
        for i in self.terminals:
            if i.followList:
                check = False
        return check


    def handleFollw(self, x, name):
        i = 0
        while i<len(x):
            if x[i] in self.names:
                if i == len(x)-1:
                    self.addItem(x[i], name, False)
                else:
                    j = i+1
                    while j < len(x):
                        if x[j] not in self.names:
                            self.addItem(x[i], x[j], True)
                            break
                        else:
                            self.getTerminal(x[i]).follow+=self.getTerminal(x[j]).first
                            if not self.getTerminal(x[j]).hasEpsilon:
                                break
                            else:
                                if j == len(x)-1:
                                    self.addItem(x[i], name, False)
                        j += 1
            i+=1

    def addItem(self, name, element, flag):
        for i in self.terminals:
            if i.name == name:
                if flag:
                    i.follow.append(element)
                else:
                    i.followList.append(element)

    def getTerminal(self, name):
        for i in self.terminals:
            if i.name==name:
                return i
        return ""

    def canEpsilon(self, name):
        for i in self.terminals:
            if i.name == name:
                if i.hasEpsilon:
                    return True
                else:
                    for j in i.productions:
                        check2 = True
                        if ["epsilon"] in j:
                            break
                        for t in j:
                            if t in self.names:
                                if not self.canEpsilon(t):
                                    check2 = False
                                    break
                            else:
                                check2 = False
                                break
                        if check2:
                            i.hasEpsilon = True
                            return True
        return False
                    
    def getFirstProd(self, name):
        for i in self.terminals:
            if i.name == name:
                return i.first
        return []

    def getFirstProd2(self, name):
        for i in self.terminals:
            if i.name == name:
                return i.firstTerminals
        return []

    def handleParse(self, parse):
        for i in parse:
            name = i.split(" ")
            x = terminal(name[0])
            self.grammarVariables.append(name[0])
            name.pop(0)
            name.pop(0)
            newList = []
            for j in name:
                if j == "|":
                    x.productions.append(newList)
                    newList = []
                else:
                    newList.append(j) 
            if newList:
                x.productions.append(newList)    
            self.terminals.append(x)      

    def intializeEpsilons(self):
        for i in self.terminals:
            for t in i.productions:
                if t == ["epsilon"]:
                    i.hasEpsilon = True
        for i in self.terminals:
            i.hasEpsilon = self.canEpsilon(i.name)

def parseInput(x):
    newList = []
    for i in x:
        new = i.replace("\n", "")
        newList.append(new)
    return newList


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    print(args.file)
    lines = []
    with open(args.file, "r") as f:
        for line in f:
            lines.append(line)
    parsed = parseInput(lines)
    Grammar(parsed)