import csv
import json
import operator
import random
import sys
import time

"""
GURPS is a trademark of Steve Jackson Games, and its rules and art are copyrighted 
by Steve Jackson Games. All rights are reserved by Steve Jackson Games. This game aid is 
the original creation of John Murray and is released for free distribution, and not for 
resale, under the permissions granted in the 
<a href="http://www.sjgames.com/general/online_policy.html">Steve Jackson Games Online 
Policy</a>.
"""

class Skill():
    def __init__(self, name, atributeStr, atributeVal,  difficulty=0, points=1):
        """
            Default to 0 (easy) and 1 point spent
        """

        # Error checking
        assert(type(atributeStr) == type(str()))
        assert(type(atributeVal) == type(int()))
        assert(type(points) == type(int()))
        assert(points>0)

        self.Name=name
        self.AtributeString = atributeStr
        self.AtributeValue = atributeVal

        if(type(difficulty) == type(int())):
            self.Difficulty = difficulty
        else:
            if(difficulty=="E"):
                self.Difficulty=0
            elif(difficulty=="A"):
                self.Difficulty=1
            elif(difficulty=="H"):
                self.Difficulty=2
            elif(difficulty=="VH"):
                self.Difficulty=3



        self.Points = points
        self.CalcSkillMod()


    def CalcSkillMod(self):
        assert(self.Points > 0)
        if(self.Points < 4):
            self.SkillMod = int(self.Points / 2) 
        else:
            self.SkillMod = int(self.Points/4) + 1
        if( self.Difficulty == 0 ):
             pass
        elif( self.Difficulty == 1 ):
             self.SkillMod -= 1
        elif( self.Difficulty == 2 ):
             self.SkillMod -= 2
        elif( self.Difficulty == 3 ):
             self.SkillMod -= 3
        else:
            print("INVALID DIFFiCULTY!")
            assert(False)

    def SetAtrib(self, atributeStr, atributeVal):
        self.AtributeString = atributeStr
        self.AtributeValue = atributeVal

    def ModPoints(self, deltaPoints):
        self.Points += deltaPoints
        self.CalcSkillMod()
    
    def SetPoints(self, newPoints):
        self.Points = newPoints
        self.CalcSkillMod()

    def Check(self, mods=0):
        dieRoll = list()
        for i in range(3):
            dieRoll.append(random.randint(1,6))
        return  (self.SkillMod + self.AtributeValue) - sum(dieRoll) + mods

    def Print(self):
        print("%s-%d (%+d)" %(self.Name, self.SkillMod + self.AtributeValue, self.SkillMod))

    def GetPrint(self):
        return "%s-%d (%+d)" %(self.Name, self.SkillMod + self.AtributeValue, self.SkillMod)


class CharSheet():
    
    def __init__(self,default=10):
        self.name   = "DEFAULT"
        self.ST     = default
        self.DX     = default
        self.IQ     = default
        self.HT     = default
        self.HP     = self.ST
        self.WILL   = self.IQ
        self.PER    = self.IQ
        self.FP     = self.HT
        self.Skills = dict()

        self.Height=0
        self.Weight=0
        self.Points=0+(default-10)*(10+20+20+10)
    
    def Roll(self,template,statPoints=0,skillPoints=0):
        self.Height = random.gauss(1.778,0.15)

        self.GenerateName()

        with open(template,'rb') as f:
            settingsData=json.load(f)

        dataAttributes = settingsData['Attributes']

        dataSkills = settingsData['Skills']

        runningTotalAttributes = 0
        for i in dataAttributes:
            oldData = dataAttributes[i]["weight"]
            dataAttributes[i]["weight"] = dataAttributes[i]["weight"] + runningTotalAttributes
            runningTotalAttributes += oldData

        runningTotalSkills = 0
        for i in dataSkills:
            oldData = dataSkills[i]["weight"]
            dataSkills[i]["weight"] = dataSkills[i]["weight"] + runningTotalSkills
            runningTotalSkills += oldData
        
        startPoints  = (self.ST - 10)*10
        startPoints += (self.DX - 10)*20
        startPoints += (self.IQ - 10)*20
        startPoints += (self.HT - 10)*10
        startPoints += (self.HP - self.ST)*2
        startPoints += (self.WILL - self.IQ)*5
        startPoints += (self.PER - self.IQ)*5
        startPoints += (self.FP - self.HT)*3
        
        while(startPoints < statPoints):
            # Spend points on stuff!
            # Select a weighted 
            selection = random.randint(0,runningTotalAttributes)
            
            for i in dataAttributes:
                if(selection <= dataAttributes[i]["weight"]):
                    selection = i
                    break


            if(selection == "ST"):
                self.ST+=1
                self.HP+=1
                self.Points+=10
                statPoints -=10

            elif(selection == "DX"):
                self.DX+=1
                self.Points+=20
                statPoints -=20

            elif(selection == "IQ"):
                self.IQ+=1
                self.WILL+=1
                self.PER+=1
                self.Points+=20
                statPoints -=20

            elif(selection == "HT"):
                self.HT+=1
                self.FP+=1
                self.Points+=10
                statPoints -=10

            elif(selection == "HP" and self.HP+1 <= self.ST*1.3):
                # Limited to +/- 30% of ST
                self.HP+=1
                self.Points+=2
                statPoints -=2

            elif(selection == "WILL" and self.WILL <=20):
                self.WILL+=1
                self.Points+=5
                statPoints -=5

            elif(selection == "PER" and self.PER <= 20):
                self.PER+=1
                self.Points+=5
                statPoints -=5

            elif(selection == "FP" and self.FP+1 <= self.HT*1.3):
                self.FP+=1
                self.Points+=3
                statPoints -=3

        startPoints = 0
        while(startPoints < skillPoints):
            selection = random.randint(0,runningTotalSkills)
            
            for i in dataSkills:
                if(selection <= dataSkills[i]["weight"]):
                    selection = i
                    break

            # Update skill or add a new one
            if(selection in self.Skills):
                self.Skills[selection].ModPoints(1)
            else:
                #__init__(self, name, atributeStr, atributeVal,  difficulty=0, points=1):
                self.Skills[selection]=Skill(   i,
                                                str(dataSkills[i]["attribute"]),
                                                getattr(self,dataSkills[i]["attribute"]),
                                                dataSkills[i]["diff"]
                                            )
            self.Points+=1
            skillPoints -=1

        # Update Skills
        for i in self.Skills:
            tempAttribute = self.Skills[i].AtributeString
            self.Skills[i].SetAtrib(tempAttribute,getattr(self,tempAttribute))

    def __str__(self):
        return self.name

    def Print(self):
        print("Name:",self.name)
        print("     ST: %3d" % (self.ST))
        print("     DX: %3d" % (self.DX))
        print("     IQ: %3d" % (self.IQ))
        print("     HT: %3d" % (self.HT))
        print("     HP: %3d" % (self.HP))
        print("   WILL: %3d" % (self.WILL))
        print("    PER: %3d" % (self.PER))
        print("     FP: %3d" % (self.FP))
        print(" Points: %3d" % (self.Points))
        print(" Skills:")      
        sortedSkills = sorted(iter(self.Skills.items()), key=operator.itemgetter(0))
        for i in sortedSkills:
            print(" ",i[1].GetPrint())   

    def PrintWiki(self):
        print("!!!",self.name)
        wikiName = self.name.replace(' ',"_").replace(',','')
        print("((Colony:NPC:Farmer:%s|SubPage))"%(wikiName))
        print("||ST| %3d" % (self.ST))
        print("DX| %3d" % (self.DX))
        print("IQ| %3d" % (self.IQ))
        print("HT| %3d" % (self.HT))
        print("HP| %3d" % (self.HP))
        print("WILL| %3d" % (self.WILL))
        print("PER| %3d" % (self.PER))
        print("FP| %3d" % (self.FP))
        print("Points| %3d||" % (self.Points))
        print("*Skills:")      
        sortedSkills = sorted(iter(self.Skills.items()), key=operator.itemgetter(0))
        for i in sortedSkills:
            print("**",i[1].GetPrint())


    def GenerateName(self,gender="male"):
        self.name = self.ParseNameFile('data/lastnames.csv') + ", " + self.ParseNameFile('data/firstnames.csv',gender)

    def ParseNameFile(self,namesFile,gender="male"):
        with open(namesFile,'r') as namesFile:
            nameReader = csv.reader(namesFile)
            firstNamesMale = list()
            firstNamesFemale = list()

            # Skip the header
            next(nameReader)
            for i in nameReader:
                firstNamesMale.append(i[1:3])
                if(gender=="female"):
                    firstNamesFemale.append(i[3:5])

        # Convert counts to ints    
        if(gender=="male"):
            for i in firstNamesMale:
                i[1]=int(i[1])
        elif(gender=="female"): 
            for i in firstNamesFemale:
                i[1]=int(i[1])

        # Prep ints for random selection
        if(gender=="male"):
            runningTotalMale=0
            for i in firstNamesMale:
                oldData = i[1]
                i[1]=i[1]+runningTotalMale
                runningTotalMale+=oldData
        if(gender=="female"):
            runningTotalFemale=0
            for i in firstNamesFemale:
                oldData = i[1]
                i[1]=i[1]+runningTotalFemale
                runningTotalFemale+=oldData

        # Randomly select one of the weight targets
        if(gender=="male"):
            selecton = random.randint(0,runningTotalMale)
            for i in firstNamesMale:
                if selecton <= i[1]:
                    return i[0].title()
        elif(gender=="female"):
            selecton = random.randint(0,runningTotalFemale)
            for i in firstNamesFemale:
                if selecton <= i[1]:
                    return i[0].title()


x = list()
for i in range(10):
    x.append(CharSheet(5))
    x[i].Roll('data/templates/workerTemplate.json',50,100)


x = sorted(x, key=operator.attrgetter('name'))

for i in x:
    i.PrintWiki()
    # i.Print()
    print()
