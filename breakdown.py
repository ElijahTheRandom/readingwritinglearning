import pickle

connotations = pickle.load(open(r"savefiles\connotations.pkl", "rb"))
sentencedic = pickle.load(open(r"savefiles\sentencedic.pkl", "rb")) 
sentencedict = pickle.load(open(r"savefiles\sentenceranking.pkl", "rb"))
dictionary = pickle.load(open(r"savefiles\dictionary.pkl", "rb"))
wordstuff = pickle.load(open(r"savefiles\wordstuff.pkl", "rb"))

def setword(message):
    msg = message.lower().split(" ")
    for key in dictionary:
        if msg[1] in dictionary[key]:
            dictionary[key].remove(msg[1])
    if msg[2] in ["greeting", "pronoun", "noun", "verb", "adverb", "question", "adjective", "preposition", "conjunction", "self", "possesive", "random", "article", "yesno", "others", "none"]:
        dictionary[msg[2]].add(msg[1]) 
        print("Assigned {} to {}".format(msg[1], msg[2]))
    else:
        print("Format is: **setword *__word__* *__part of sentence__***\nThe parts of sentence available are: greeting, pronoun, noun, verb, adverb, question, adjective, preposition, conjunction, self, possesive, random, article, yesno, others, none")

class Utils:
    def placewords(word): #finds the what part of sentence a specific word is
        for key in dictionary:
            if word in dictionary[key]:
                return key

    def makereadable(item):
        for x in item:
            wordlist = []
            for y in item[x]:
                wordlist.append(f"{y} : {item[x][y]}")
            print(f"{x} = {wordlist}")

class Response:
    def checksentence(self):
        self.sentencestructure = []
        check = False
        for word in self.message:
            check = False
            for key in dictionary:
                if word in dictionary[key]:
                    self.sentencestructure.append(key)
                    check = True
            if check == False:
                self.sentencestructure.append("unknown")
                unknownword = word 
                return unknownword #in the future dont end the loop here, find the POS
        return self.sentencestructure

    def getpreposition(self): #ISSUES: can't handle multiple uses of the same preposition 12/19/22
        prepositions = []
        thenoun = 0
        for prep in self.importantpos["preposition"]:
            msg2 = self.message[self.message.index(prep):] #shortens sentence to the preposition to the rest of the sentence
            for word in msg2:
                if word in dictionary["noun"]:
                    thenoun = word #gets the closest noun
                    break
            if thenoun != 0:
                prepositions.append([self.message.index(prep), self.message.index(thenoun), " ".join(msg2[:(msg2.index(thenoun)+1)]).split(" ")])
                thenoun = 0
        self.importantpos["preposition"] = prepositions

        return self.importantpos

    def getsubject(self):
        subjectloc = []
        verbloc = []
        for sub in self.importantpos["subject"]:
            subjectloc.append(self.message.index(sub)) #gets the location of the potential subjects
        for verb in self.importantpos["mainverb"]:
            verbloc.append(self.message.index(verb)) #gets location of potential mainverbs
        verbloc = min(verbloc)
        for nums in subjectloc:
            if nums > verbloc: #if potential subject is after verb, remove it
                subjectloc.remove(nums)
        self.importantpos["subject"] = [self.message[min(subjectloc, key=lambda x:abs(x-verbloc))], min(subjectloc, key=lambda x:abs(x-verbloc))]  #gets the noun/pronoun/self closest to the verb
        self.importantpos["mainverb"] = [self.message[verbloc],verbloc]
        
        return self.importantpos

    def sentencedeconstruct(self):
        sentencedeconstruct = {}
        counter = 0
        for word in self.message:
            sentencedeconstruct[word] = {"pos":Utils.placewords(word), "position":counter}
            counter = counter + 1

        for key in sentencedeconstruct:
            if sentencedeconstruct[key]["pos"] == "noun":
                if sentencedeconstruct[key]["position"] == 0:
                    pass
                else:
                    breaktime = False
                    counters = 1
                    while counters <= sentencedeconstruct[key]["position"]:
                        for items in self.importantpos['preposition']:
                            if (sentencedeconstruct[key]["position"]-counters) == max((i for i in items if isinstance(i, int))):
                                breaktime = True
                        if breaktime == True:
                            breaktime = False
                            break
                        elif self.sentencestructure[sentencedeconstruct[key]["position"]-counters] == "article":
                            print("It's an article")
                        elif self.sentencestructure[sentencedeconstruct[key]["position"]-counters] == "adjective":
                            print("It's an adjective")
                        elif self.sentencestructure[sentencedeconstruct[key]["position"]-counters] == "noun":
                            print("It's a noun")
                        else:
                            break
                        counters = counters + 1
                        sentencedeconstruct[key]["phrase"] = self.message[sentencedeconstruct[key]["position"]-counters+1:sentencedeconstruct[key]["position"]+1]

            if sentencedeconstruct[key]["pos"] == "verb":
                if sentencedeconstruct[key]["position"] == 0:
                    pass
                else:
                    counters = 1
                    while counters <= sentencedeconstruct[key]["position"]:
                        if self.sentencestructure[sentencedeconstruct[key]["position"]-counters] == "verb":
                            print("It's a helping verb")
                        elif self.sentencestructure[sentencedeconstruct[key]["position"]-counters] == "adverb":
                            print("It's an adverb")

                        else:
                            break
                        counters = counters + 1
                        sentencedeconstruct[key]["phrase"] = self.message[sentencedeconstruct[key]["position"]-counters+1:sentencedeconstruct[key]["position"]+1]
        
        Utils.makereadable(sentencedeconstruct)
        return sentencedeconstruct

    def __init__(self, message, ctx=None):
        self.importantpos = {"subject":[],"mainverb":[],"preposition":[]}
        self.message = str(message.lower()).replace(",","").replace(" ", ",").replace("~","").replace("$","").replace("%","").replace("^","").replace("&","").replace("*","").replace("(","").replace(")","").replace("-","").replace("_","").replace("+","").replace("=","").replace("<","").replace(">","").replace("/","").replace("{","").replace("}","").replace("[","").replace("]","").replace(":","").replace(";","").replace("|","").replace("~","").replace("`","").replace('"', "").replace("?", "").replace(".", "").replace("!","").replace("#","").split(",")
        
        if ctx:
            self.sentencestructure = ctx
        else:
            self.sentencestructure = Response.checksentence(self)

        if isinstance(self.sentencestructure, str):
            print("I do not know the word '{}'! Please use the **setword** command to add it!".format(self.sentencestructure))
            return
        
        for word in self.message:
            if word in dictionary["noun"]:
                self.importantpos["subject"].append(word)
            if word in dictionary["pronoun"]:
                self.importantpos["subject"].append(word)
            if word in dictionary["self"]:
                self.importantpos["subject"].append(word)
            if word in dictionary["others"]:
                self.importantpos["subject"].append(word)
            if word in dictionary["verb"]:
                self.importantpos["mainverb"].append(word)
            if word in dictionary["preposition"]:
                self.importantpos["preposition"].append(word)

        self.importantpos = Response.getpreposition(self)

        if self.importantpos["preposition"]: #if there is a preposition, do code
            for lists in self.importantpos["preposition"]: #if a noun/verb inside a preposition, remove it from being a potential subject or mainverb
                for theprepwords in lists[2]:
                    for potentialsubjects in self.importantpos["subject"]:
                        if potentialsubjects == theprepwords:
                            self.importantpos["subject"].remove(potentialsubjects)
                    for potentialmainverbs in self.importantpos["mainverb"]:
                        if potentialmainverbs == theprepwords:
                            self.importantpos["mainverb"].remove(potentialmainverbs)
        
        try:
            self.importantpos = Response.getsubject(self)
        except Exception as e:
            print(e)
            return
        
        self.deconstructed = Response.sentencedeconstruct(self)


def theinput(yamsg,constr=None):
    message = yamsg
    if message.startswith("setword"):
        setword(message)
    else:
        if constr:
            retrieveinfo = Response(message, constr)
        else:
            retrieveinfo = Response(message)
        info = [retrieveinfo.deconstructed, retrieveinfo.importantpos]
        return info
        
