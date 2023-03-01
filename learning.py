import random
import pickle

connotations = pickle.load(open(r"savefiles\connotations.pkl", "rb"))
sentencedic = pickle.load(open(r"savefiles\sentencedic.pkl", "rb"))
sentencedict = pickle.load(open(r"savefiles\sentenceranking.pkl", "rb"))
dictionary = pickle.load(open(r"savefiles\dictionary.pkl", "rb"))
wordstuff = pickle.load(open(r"savefiles\wordstuff.pkl", "rb"))


#expdict = pickle.load(open(r"savefiles\expdict.pkl", "rb"))
#greeting, pronoun, noun, verb, adverb, question, adjective, preposition, conjunction, self, possesive, random, article, yesno, others

#"man":{"con":0,"uses":0}
#main:{"type":"p","uses":0}

shouldRun = True
pattern2 = {}

class Utils:
    def getpattern(x = wordstuff):
        pattern = {}
        for key in x:
            tempnum = 0
            pattern[key] = {"commonbefore":{},"commonafter":{}}
            if x[key]["before"] != '':
                for beforewords in x[key]["before"]:
                    tempnum = x[key]["before"][beforewords] + tempnum
                for beforewords in x[key]["before"]:
                    pattern[key]["commonbefore"][beforewords] = x[key]["before"][beforewords]/tempnum
        for key in x:
            tempnum = 0
            if x[key]["after"] != '':
                for afterwords in x[key]["after"]:
                    tempnum = x[key]["after"][afterwords] + tempnum
                for afterwords in x[key]["after"]:
                    pattern[key]["commonafter"][afterwords] = x[key]["after"][afterwords]/tempnum
        return pattern
    
    def getallknownwords():
        templist = []
        for key in dictionary:
            if key != "sortedlater" and key != "none":
                for word in dictionary[key]:
                    templist.append(word)
        return templist

    def placewords(word):
        for key in dictionary:
            if word in dictionary[key]:
                return key

    def choosewordfromcat(pos):
        return random.choice(list(dictionary[pos]))

    def decider(a=50,b=50):
        if "".join(random.choices(["Yes","No"], weights=[a,b], k=1)) == "Yes":
            return True
        else:
            return False

    def getcommonword(befaft,chckwrd,pos):
        if chckwrd in wordstuff:
            templist = []
            avg = []
            for key in wordstuff[chckwrd][befaft]:
                if key in dictionary[pos]:
                    avg.append(wordstuff[chckwrd][befaft][key])
            try: 
                avg = sum(avg)/len(avg)
            except ZeroDivisionError:
                return Utils.choosewordfromcat(pos)
            except Exception as e:
                print(e)
                return Utils.choosewordfromcat(pos)
            for key in wordstuff[chckwrd][befaft]:
                if key in dictionary[pos] and key != chckwrd:
                    if wordstuff[chckwrd][befaft][key] >= avg:
                        templist.append(key)
                    else:
                        continue
            if templist:
                choice = random.choice(templist)
                return choice
            else:
                return Utils.choosewordfromcat(pos)
        else:
            return Utils.choosewordfromcat(pos)

class SentenceBasics:
    def save_words(message):
        if message.author.id == 333724648900657155:
            pickle.dump(dictionary, open(r"savefiles\dictionary.pkl", "wb"))

    def create_sentence(message):
        avg = []
        for key in sentencedict:
            avg.append(sentencedict[key])
        avg = sum(avg)/len(avg) #creates an average of sentence structure integers

        createsent = random.choice(list(sentencedic["sentences"]))
        while sentencedict[createsent] <= avg and len(createsent) < 2:
            createsent = random.choice(list(sentencedic["sentences"]))
        createsent = str(createsent).replace(" ", ",").replace("[","").replace("]","").split(",")
        newsentence = []
        counter = 0
        for pos in createsent:
            templist = []
            dontHave = False
            avg = []
            if counter > 0:
                if newsentence[counter-1] in wordstuff:
                    for key in wordstuff[newsentence[counter-1]]["after"]:
                        avg.append(wordstuff[newsentence[counter-1]]["after"][key])
                    try: 
                        avg = sum(avg)/len(avg)
                    except:
                        pass
                    for key in wordstuff[newsentence[counter-1]]["after"]:
                        if wordstuff[newsentence[counter-1]]["after"][key] >= avg:
                            templist.append(key)
                        else:
                            continue
                if not templist:
                    dontHave = True
                if (newsentence[counter-1] in wordstuff) and dontHave != True:
                    newsentence.append(random.choice(templist))
            if counter == 0 or dontHave == True:
                newsentence.append(Utils.choosewordfromcat(pos))
            counter = counter + 1
        newsentence = " ".join(newsentence)
        return newsentence

    def exp_create_sentence(message):
        #subject predicate object
        #article adjective adjective subject adverb predicate (1 preposition noun) (2 noun) (3 verb ending in ing) random*
        subject = Utils.choosewordfromcat("noun")
        predicate = Utils.choosewordfromcat("verb")
        
        newsentence = [subject, predicate, "object"]
        structure = ["subject","predicate","object"]

        word = False
        afterpredword = False

        if Utils.decider() == True:
            newsentence.insert(0, Utils.choosewordfromcat("article"))
            structure.insert(0, "article")

        while Utils.decider() == True:
            if word:
                word = Utils.getcommonword("before", word, "adjective")
            else:
                word = Utils.getcommonword("before", subject, "adjective")
            word = Utils.getcommonword("before", subject, "adjective")
            newsentence.insert(structure.index("subject"), word)
            structure.insert(structure.index("subject"), "adjective")
        
        while Utils.decider() == True:
            if afterpredword:
                afterpredword = Utils.getcommonword("before", word, "adverb")
            else:
                afterpredword = Utils.getcommonword("before", predicate, "adverb")
            #afterpredword = Utils.getcommonword("before", predicate, "adverb")
            word = afterpredword
            newsentence.insert(structure.index("predicate"), afterpredword)
            structure.insert(structure.index("predicate"), "adverb")
        
        option = random.randint(1,2)
        if option == 1:
            word = Utils.getcommonword("after", predicate, "preposition")
            newsentence.insert(structure.index("object"), word)
            structure.insert(structure.index("object"), "preposition")
            if Utils.decider() == True:
                word = Utils.getcommonword("after", word, "article")
                newsentence.insert(structure.index("object"), word)
                structure.insert(structure.index("object"), "article")
            while Utils.decider() == True:
                if word:
                    word = Utils.getcommonword("after", word, "adjective")
                else:
                    word = Utils.getcommonword("after", predicate, "adjective")
                #word = Utils.getcommonword("after", word, "adjective")
                newsentence.insert(structure.index("object"), word)
                structure.insert(structure.index("object"), "adjective")
            word = Utils.getcommonword("after", word, "noun")
            newsentence.insert(structure.index("object"), word)
            structure.insert(structure.index("object"), "noun")
        elif option == 2:
            if Utils.decider() == True:
                word = Utils.getcommonword("after", predicate, "article")
                newsentence.insert(structure.index("object"), Utils.choosewordfromcat("article"))
                structure.insert(structure.index("object"), "article")
            while Utils.decider() == True:
                if word:
                    word = Utils.getcommonword("after", word, "adjective")
                else:
                    word = Utils.getcommonword("after", predicate, "adjective")
                #word = Utils.getcommonword("after", word, "adjective")
                newsentence.insert(structure.index("object"), word)
                structure.insert(structure.index("object"), "adjective")
            if word:
                word = Utils.getcommonword("after", word, "noun")
            else:
                word = Utils.getcommonword("after", predicate, "noun")
            newsentence.insert(structure.index("object"), word)
            structure.insert(structure.index("object"), "noun")
        if Utils.decider(10,90) == True:
            newsentence.insert(structure.index("object"), Utils.choosewordfromcat("random"))
            structure.insert(structure.index("object"), "random")
        
        print(newsentence)
        del newsentence[-1]
        del structure[-1]

        newsentence = " ".join(newsentence)
        return newsentence


    def change_word(message):
        #noun, others, pronoun, sortedlater, article, adjective, yesno, verb, adverb, random, question, preposition, conjunction, greeting, self, possesive, none
        if message.author.id == 333724648900657155 or message.author.id == 284052161459912704:
            themsg2 = message.content.lower().split(" ")
            for key in dictionary:
                if themsg2[1] in dictionary[key]:
                    dictionary[key].remove(themsg2[1])   
                if themsg2[2] == key:
                    dictionary[key].add(themsg2[2]) 

class Understanding:
    def wordplacement(themsg, message):
        templist = []
        counter = 0
        if message.author.bot == False: #word:{}
            for word in themsg:
                if word in wordstuff:
                    if counter - 1 != -1: #checking to make sure that there is a word before 
                        if themsg[counter - 1] not in wordstuff[word]["before"]: #if the before word is not in the list of before words, add it
                            wordstuff[word]["before"][themsg[counter - 1]] = 1
                        elif themsg[counter - 1] in wordstuff[word]["before"]: #if the before word is in the list of before words, increase it by one
                            wordstuff[word]["before"][themsg[counter - 1]] = wordstuff[word]["before"][themsg[counter - 1]] + 1
                    if counter + 1 < len(themsg):
                        if themsg[counter + 1] not in wordstuff[word]["after"]: #if the after word is not in the list of after words, add it
                            wordstuff[word]["after"][themsg[counter + 1]] = 1
                        elif themsg[counter + 1] in wordstuff[word]["after"]: #if the after word is in the list of after words, increase it by one
                            wordstuff[word]["after"][themsg[counter + 1]] = wordstuff[word]["after"][themsg[counter + 1]] + 1
                for word2 in themsg:
                    if word == word2: #dont want the word you're testing to be added to the samesentence list
                        continue
                    if word2 in wordstuff[word]["samesentence"]: #adds every word in the sentence to the "samesentence" list
                        wordstuff[word]["samesentence"][word2] = wordstuff[word]["samesentence"][word2] + 1
                    if word2 not in wordstuff[word]["samesentence"]:
                        wordstuff[word]["samesentence"][word2] = 1
                else:
                    wordstuff[word] = {"before":{},"after":{},"samesentence":{}}
                counter = counter + 1
    
    def checkstructures(themsg, sentencestruct):
        avg = []
        for key in sentencedict:
            avg.append(sentencedict[key])
        avg = sum(avg)/len(avg) #creates an average of sentence structure integers

        sentencechecker = []
        if "unknown" in sentencestruct and sentencestruct.count("unknown") < 2:
            structuredict = list(sentencedic["sentences"]) #create a list from saved sentencestructures
            unknownposition = sentencestruct.index("unknown") #finds the location of the unknown
            for structs in structuredict:
                if len(sentencestruct) == 1: #if the sentence is one word long, it wont save
                    break
                tempsentencestruct = sentencestruct.copy() #a copy of the sentence struct list
                templiststructs = structs.split(" ") #a copy of the current structs list
                if len(tempsentencestruct) > len(templiststructs): #if the test is smaller than the actual sentence, continue
                    continue
                if templiststructs[unknownposition] == "article" or templiststructs[unknownposition] == "pronoun" or templiststructs[unknownposition] == "question" or templiststructs[unknownposition] == "none":
                    continue
                del tempsentencestruct[unknownposition] #delete unknown position
                del templiststructs[unknownposition] #delete unknown position
                if templiststructs == tempsentencestruct: #if the two lists minus the unknown position are equal
                    if sentencedict[structs] >= avg: #checks if this struct is used above averagely used structs
                        sentencechecker.append(structs)#adds to a list to check sentence rank for more accurate placement


            if len(sentencechecker) >= 1:
                sentenceranking = {} #creates a dictionary
                for structures in sentencechecker: #loops through the structures in the list of sentences
                    if structures not in sentencedict:
                        sentencedict[structures] = 1 #if not in the list, add to list and make it equal to one
                    sentenceranking[structures] = sentencedict[structures] # make sentenceranking a dictionary with only the rankings of the necessary structures
                partofsentence = str(max(sentenceranking, key=sentenceranking.get)).split(" ")[unknownposition] #finds the most used structure and gets the part of sentence
                return partofsentence

    def checksurroundings(themsg, unknownword, sentencestruct):
        global pattern2 #globals the variable pattern2
        global shouldRun
        if shouldRun == True: #makes sure that it only does this once per reload, otherwise big lag
            pattern = Utils.getpattern() #gets the averages and patterns of words that jarvis has seen
            listofwords = Utils.getallknownwords() #gets a list of all the words jarvis knows
            pattern2 = {}
            counter = 0
            for key in pattern: #loops through the words in the wordstuffs dict
                if key in listofwords: #if jarvis knows the word 
                    pattern2[key] = {"commonbefore":{},"commonafter":{}} #create a new dictionary entry with that word
                    for placement in pattern[key]: #checks the placements of the wordstuff dict word
                        for word in pattern[key][placement]: #loops through the words in the placements
                            if word in listofwords: #if the word in the placements is known by jarvis
                                pattern2[key][placement][word] = pattern[key][placement][word] #then the entry is equal
            shouldRun = False #after the first loop in reload, make this false so it does not loop every time
        
        tempnum = 0
        surrdict = {"commonbefore":{},"commonafter":{}}
        unknownpos = sentencestruct.index("unknown") #gets positioning of the unknown word

        if unknownpos - 1 != -1:
            if themsg[unknownpos - 1] not in pattern2: #if the word before the word we are checking is not known by jarvis, dont check it
                pass #come back to later
            elif themsg[unknownpos - 1] in pattern2: #if it is known by jarvis
                for key in pattern2[themsg[unknownpos - 1]]["commonafter"]:
                    tempnum = pattern2[themsg[unknownpos - 1]]["commonafter"][key] + tempnum 
                for key in pattern2[themsg[unknownpos - 1]]["commonafter"]:
                    surrdict["commonafter"][key] = pattern2[themsg[unknownpos - 1]]["commonafter"][key]/tempnum #get the average usage of each word in relation to the word being tested
                    
                    #####COME BACK TO THIS? MAYBE USE getpattern() INSTEAD OF REDOING THE AVERAGE STUFF?

        tempnum = 0

        if unknownpos + 1 < len(themsg):
            if themsg[unknownpos + 1] not in pattern2: #if the word after the word we are checking is not known by jarvis, dont check it
                pass #come back to later
            elif themsg[unknownpos + 1] in pattern2:
                for key in pattern2[themsg[unknownpos + 1]]["commonbefore"]:
                    tempnum = pattern2[themsg[unknownpos + 1]]["commonbefore"][key] + tempnum
                for key in pattern2[themsg[unknownpos + 1]]["commonbefore"]:
                    surrdict["commonbefore"][key] = pattern2[themsg[unknownpos + 1]]["commonbefore"][key]/tempnum #get the average usage of each word in relation to the word being tested

        
        multib = []
        templist = []
        for words in surrdict["commonbefore"]:
            templist.append(surrdict["commonbefore"][words]) #makes a list of numbers that correlate to words in beforewords
        check = False
        while check == False and templist != []:
            for words in surrdict["commonbefore"]: #for words in commonbefore
                if surrdict["commonbefore"][words] == max(templist): #if the number of the word is equal to the max of the list
                    posb = Utils.placewords(words) #gets the part of speech of the word
                    if posb != "article" and posb != "question" and posb != "none" and posb != "sortedlater" and posb != "pronoun":
                        multib.append(posb) #append this to a list just in case there are multiple words with the same int
                        check = True
                    else:
                        if len(templist) > 0:
                            try:
                                templist.remove(max(templist)) #if the word is any of the things above, remove that number from the list of numbers
                            except Exception as e:
                                print(e)
                                return
                        else:
                            return
                            
        #exactly the same stuff from above except its commonafter
        multia = []
        templist = []
        for words in surrdict["commonafter"]:
            templist.append(surrdict["commonafter"][words])
        check = False
        while check == False and templist != []:
            for words in surrdict["commonafter"]:
                if surrdict["commonafter"][words] == max(templist):
                    posa = Utils.placewords(words)
                    if posa != "article" and posa != "question" and posa != "none" and posa != "sortedlater" and posa != "pronoun":
                        multia.append(posa)
                        check = True
                    else:
                        if len(templist) > 0:
                            try:
                                templist.remove(max(templist)) #if the word is any of the things above, remove that number from the list of numbers
                            except Exception as e:
                                print(e)
                                return
                        else:
                            return
        test = list(set(multib).intersection(multia)) #get the intersection of the two lists of possible parts of speech
        if test: #makes sure there is an intersection
            if len(test) == 1: #checks if there is only one item in the list
                "".join(test) # turn it into a string
                return test #return it
            else:
                return test #return it as a list if more than 1
        elif multia and multib:
            return multia + multib #if no intersection, return both lists
        elif multia:
            return multia
        elif multib:
            return multib
        else:
            return None
        
    def sentencestructs(message, amsg):
        if "https://" in message.content.lower() or "http://" in message.content.lower(): #if there is a link in message, it will not save
            return 
        themsg = str(amsg).replace(",","").replace(" ", ",").replace("~","").replace("$","").replace("%","").replace("^","").replace("&","").replace("*","").replace("(","").replace(")","").replace("-","").replace("_","").replace("+","").replace("=","").replace("<","").replace(">","").replace("/","").replace("{","").replace("}","").replace("[","").replace("]","").replace(":","").replace(";","").replace("|","").replace("~","").replace("`","").replace('"', "").replace('…', "").replace("?", "").replace(".", "").replace("!","").replace("#","").split(",") #make the string into something readable by the program
        sentencestruct = []
        
        check = False
        for word in themsg: #loops through words in the message and assigns them to their respective categories
            check = False
            for key in dictionary:
                if word in dictionary[key]:
                    sentencestruct.append(key)
                    check = True
            if check == False:
                sentencestruct.append("unknown")
                unknownword = word

        if "unknown" not in sentencestruct and len(sentencestruct) > 0:
            sentences = " ".join(sentencestruct) #turns sentencestruct into a string
            if sentences not in sentencedic["sentences"] and ("sortedlater" not in sentences and "none" not in sentences and "unknown" not in sentences) and sentences != None and str(sentences) != '': #makes sure that certain unusable structures are not in the message being processed
                sentencedic["sentences"].add(sentences) #adds the structure to structure dictionary
                pickle.dump(sentencedic, open(r"savefiles\sentencedic.pkl", "wb")) #saves the sentencestructure file
            if sentences in sentencedic["sentences"] and sentences != None and str(sentences) != '':
                if sentences in sentencedict:
                    sentencedict[sentences]+=1 # rank adding
                else:
                    sentencedict[sentences]=1 # if no rank, add one
                pickle.dump(sentencedict, open(r"savefiles\sentenceranking.pkl", "wb")) #saves the sentence ranking file

        Understanding.wordplacement(themsg, message) #calls on the function wordplacement

        if "unknown" in sentencestruct and sentencestruct.count("unknown") < 2: #makes sure there is an unknown word in the sentence but not more than two
            guess1 = Understanding.checkstructures(themsg, sentencestruct, message) #starts the checkstructures function with the arguments of the message, the structure of it, the discord thing message, and the discord thing client
            guess2 = Understanding.checksurroundings(themsg, unknownword, sentencestruct) #calls on the checksurroundings function wuth the arguments of the message, the unknown word, and the structure of the message
            if guess1 == guess2 and guess1 and guess2: #if the two part of speech guesses are the same, then that's the concluded result
                if unknownword not in dictionary[guess1]:
                    dictionary[guess1].add(unknownword) #adds the part of sentence the unknown word is
            elif isinstance(guess2, list) and guess1: #checks if one of the before/after parts of speech matches up with the sentencestructure guess
                guesses = []
                guesses.append(guess1)
                test = "".join(list(set(guess2).intersection(guesses)))
                if test and unknownword not in dictionary[guess1]:
                    dictionary[guess1].add(unknownword) #adds the part of sentence the unknown word is
            elif isinstance(guess2, str) and guess1 != guess2:
                if unknownword not in dictionary[guess1]:
                    pass

    def jreload(message, messagelist):
        global shouldRun #globals a variable called shouldRun, this variable makes it only loop through wordstuff dictionary once
        for amsg in messagelist: #for message in list of messages
            Understanding.sentencestructs(message, amsg) #do the function sentencestuff (which is directly above this one)
        shouldRun = True #shouldRun is changed back to True so it will loop through the dict again next reload
        try:
            pickle.dump(wordstuff, open(r"savefiles\wordstuff.pkl", "wb")) # dump wordstuff after the whole list is done
        except:
            pass