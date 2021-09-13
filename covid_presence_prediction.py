import time
import os
from functools import reduce
import pandas as pd
import pprint


cond =[]

class Classifier():
    data = None
    class_attr = None
    priori = {}
    cp = {}
    hypothesis = None


    def __init__(self,filename=None, class_attr=None ):
        self.data = pd.read_csv(filename, sep=',', header =(0))
        self.class_attr = class_attr

    '''
        probability(class) =    How many  times it appears in cloumn
                             __________________________________________
                                  count of all class attribute
    '''
    def calculate_priori(self):
        class_values = list(set(self.data[self.class_attr]))
        class_data =  list(self.data[self.class_attr])
        for i in class_values:
            self.priori[i]  = class_data.count(i)/float(len(class_data))

    '''
        Here we calculate the individual probabilites 
        P(outcome|evidence) =   P(Likelihood of Evidence) x Prior prob of outcome
                               ___________________________________________
                                                    P(Evidence)
    '''
    def get_cp(self, attr, attr_type, class_value):
        data_attr = list(self.data[attr])
        class_data = list(self.data[self.class_attr])
        total =1
        for i in range(0, len(data_attr)):
            if class_data[i] == class_value and data_attr[i] == attr_type:
                total+=1
        return total/float(class_data.count(class_value))

    '''
        Here we calculate Likelihood of Evidence and multiple all individual probabilities with priori
        (Outcome|Multiple Evidence) = P(Evidence1|Outcome) x P(Evidence2|outcome) x ... x P(EvidenceN|outcome) x P(Outcome)
        scaled by P(Multiple Evidence)
    '''
    def calculate_conditional_probabilities(self, hypothesis):
        for i in self.priori:
            self.cp[i] = {}
            for j in hypothesis:
                self.cp[i].update({ hypothesis[j]: self.get_cp(j, hypothesis[j], i)})

    def classify(self):
        os.system('cls')
        print ("Result: ")
        for i in self.cp:
            print ("\n\n" +str(i), " ==> ", str(reduce(lambda x, y: x*y, self.cp[i].values())*self.priori[i]))
            print("\n")

    
if __name__ == "__main__":
    c = Classifier(filename="Covid_Dataset.csv", class_attr="COVID-19" )
    c.calculate_priori()

    # Initialize CMD
    os.system('cls')
    os.system('@echo off')
    os.system('color F')
    os.system('title Covid-19 Presence Predictor')
    os.system('echo Covid-19 Presence Predictor')
    os.system('echo.')
    os.system('echo.')

    cond.append(input("\nDo you have problem in breathing? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nDo you have fever? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nDo you have dry cough? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nDo you have a sore throat? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nDo you have a runny nose? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nDo you have asthma? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nDo you have lungs disease? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nDo you have headache? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nDo you have heart disease? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nDo you have diabetes? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nHave you travelled abroad within 14 days? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nHave you contacted with any covid patient within 14 days? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nDid you attended any large gathering within 14 days? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nDid you visited any public exposed places within 14 days? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nDo any of your family member work in a public exposed place? (Yes/No)\nAnswer: ").capitalize())
    cond.append(input("\nDo you wear a mask? (Yes/No)\nAnswer: ").capitalize())

    
##    for i in cond:
##        if i != "Yes" and i != "No":
##            os.system('cls')
##            os.system('color E')
##            print("[WARNING] You must answer the questions with only Yes and No...You can't use words like '" + i +"'")
##            os.system('pause')
##            os.system('cls')
##            os.system('color F')
##            print("[INFO] Restarting model...Please wait")
##            time.sleep(3)
##            main()
    
            
    c.hypothesis = {"Breathing Problem":cond[0], "Fever":cond[1], "Dry Cough":cond[2], "Sore throat":cond[3],
    		 "Runny Nose":cond[4], "Asthma":cond[5], "Chronic Lung Disease":cond[6], "Headache":cond[7], 
    		 "Heart Disease":cond[8], "Diabetes":cond[9], "Travel abroad":cond[10], "Contacted with COVID Patient":cond[11],
    		 "Attended Large Gathering":cond[12], "Visited Public Exposed Places":cond[13], "Family worked in Public Exposed Places":cond[14], 
    		 "Wearing Masks":cond[15]}

    c.calculate_conditional_probabilities(c.hypothesis)
    c.classify()
    os.system('pause')
