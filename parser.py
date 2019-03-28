import os 
import LexicalAnalyzer as la
from pandas import read_excel



my_sheet = 'Parse Table edited'
file_name = 'ptable.xlsx'
dff = read_excel(file_name, sheet_name = my_sheet)
dff['TRUE'] = dff[True]
dff['FALSE'] = dff[False]
del dff[True]
del dff[False]
df = dff

def tokenProcessor(i):
    
    j = i.split(',')

    if j[1] == '':
        return [',',j[-1][:-1]]

    j[0] = j[0][1:]
    j[-1] = j[-1][:-1]
    

    return j


def token2terminal(x):

    terminals = []
    ls = ['keyword','logical-operator','operator']
    for i in x:
        j = tokenProcessor(i)
        
        
        
        if j[0] in ls:
            if j[1] == 'END':
                terminals.append(('$',j[-1]))
                print('prob:' ,i)
            else:
                terminals.append((j[1],j[-1]))

##        elif j[0] == 'operator':
##
##            terminals.append(j[1])
            
        elif j[0] == 'identifier':
            if j[0] == '':
                print('prob:' ,i)
            terminals.append(('identifier',j[-1]))
        
        elif j[0] == 'str':
            if j[0] == '':
                print('prob:' ,i)
            terminals.append(('stringliteral',j[-1]))

        elif j[0] == 'int' or j[0] == 'float':
            if j[0] == '':
                print('prob:' ,i)
            terminals.append(('numberliteral',j[-1]))

        else:
            #print('Not reckoned: ',i)
            if j[0] == '':
                print('Not reckoned: ',i)
                terminals.append((',',j[-1]))
            else:
                terminals.append((j[0],j[-1]))

    return terminals
            

            



#tokenList = []
#errorList = []
#symbolTable = []

#filename = input("Input File Name: ")


#prog = open(fname, 'r').read()
#fileName = fname.split('.', 1)[0]
#print(fileName)



#F = [('Identifier'),('(',E),')']
#T0 = [('Op-Multiply',F,T0),('null')]
#T = [(F,T0)]
#E0 = [('Op-Plus',T,E0),('null')]
#E = [(T),(E0)]


import pandas as pd

rws = ['E','E0','T','T0','F']
cls = ['Identifier','Op-Plus','Op-Multiply','(',')','$']
#df = pd.DataFrame( index=rws, columns=cls)

#df = pd.read_pickle('df.pkl')

#rules={'E':''}
case1 = ['*','id','+','(','id','*','(',')','id',')','*','$']


case2 = [')','+','*','(','*','(','id','+','id','id',')','*','id','$']
er=[]

def start():

    global er, ptStack, pt
    #w = ['(','*',')','+','*','(','*','(','id','+','id','id',')','*','id','$']
    w = token2terminal(tokenList)
    w = w[::-1]
    buffer = ['$','Program']
    parseTree = []
    match = []
    ptStack = []
    pt = []
    
    while (w != []):

        #parseTree.append(df.loc[buffer[-1],w[-1]])
        #print('Buffer,Input: ' ,buffer[-1],w[-1])
        
        #print('Prod: ', df.loc[buffer[-1],w[-1]])
        
        if (buffer[-1] == 'ε'):
            del buffer[-1]
            
            if (buffer [-1] not in df.columns):
                x = 'Exiting: ' + ptStack[-1]
                pt.append(x)
                del ptStack[-1]
            
            
            
        elif w[-1][0] == buffer [-1]:
            match.append(w[-1][0])

            x = 'Matched: ' + str(w[-1])
            pt.append(x)
            
            

            del buffer[-1]
            del w[-1]

            if buffer != []:
                if (buffer [-1] not in df.columns):
                    x = 'Exiting: ' + ptStack[-1]
                    pt.append(x)
                    del ptStack[-1]

            
                

        elif (buffer [-1] in df.columns):
            
            del buffer[-1]
            
       

        elif (pd.isnull(df.loc[buffer[-1],w[-1][0]]) == False and df.loc[buffer[-1],w[-1][0]] != 'Sync'):
            parseTree.append(df.loc[buffer[-1],w[-1][0]])
            
            prod = df.loc[buffer[-1],w[-1][0]]
            p = list(filter(None, prod.split('→')[1].split(' ')))
            p = list(map(lambda x: x.replace('\xa0',''),p))

            x = 'In: ' + buffer[-1]
            pt.append(x)
            ptStack.append(buffer[-1])
            
            del buffer[-1]
            buffer = buffer + p[::-1]

        elif (df.loc[buffer[-1],w[-1][0]] == 'Sync'):             #Panic Mode error recovery - sync

            #Panic Mode error recovery - delete production upon sync match in parse table
            if buffer[-2] == '$':
                print('rule 3')
                #print('Deleted: ', w[-1])
                parseTree.append('Rule 3 Error')
                errorGenerator(7,buffer,w)

                del w[-1]
            else:
                
                print('rule 1')
                parseTree.append('Rule 1 Error')
                #print('Deleted: ', buffer[-1])
                errorGenerator(8,buffer,w)

                if (buffer [-1] not in df.columns)and buffer != []:
                    x = 'Exiting: ' + ptStack[-1]
                    pt.append(x)
                    del ptStack[-1]

                del buffer[-1]
                
            #continue


        elif (pd.isnull(df.loc[buffer[-1],w[-1][0]])):
            #Panic Mode error recovery - delete input symbol upon null matching entries in the parsing table
            
            #print(df.loc[buffer[-1],w[-1]] == 'sync')
            #print('Error: Expected \'' + buffer[-1] + '\' - Recieved \'' + w[-1] + '\'.' )
            #print('\nBuffer,Input: ' ,buffer[-1],w[-1[0]])
            print('rule 2')
            parseTree.append('Rule 2 Error')
            c = 'Buffer,Input: ' + buffer[-1],w[-1][0]
            parseTree.append(c)

            errorGenerator(7,buffer,w)

            
          #  print('Deleted: ', w[-1])
            del w[-1]
            #w = []

        else:
            print('BREAK')

        #print('Buffer,Input: ' ,buffer,w)
            

        

    
    #for i in parseTree:
     #   print(i)

    return match,parseTree, pt


def errorGenerator(x,buffer,w):

    global errorList

    if x == 7:

        rr = ('Line: '+ w[-1][-1] + ' - Error Code: 7' + ' - Error: Syntax Error. Expected " '
                    + buffer[-1] + ' "'+ ', Got " '+ w[-1][0] +' "' +
                      ' - Status: Resolved - Action: Input token deleted')
        

    else:

        rr = ('Line: '+ w[-1][-1] + ' - Error Code: 8' + ' - Error: Syntax Error. Expected " '
                    + buffer[-1] + ' "'+ ', Got " '+ w[-1][0] +' "' +
                      ' - Status: Resolved - Action: Expected token popped')

        
    errorList.append(rr)
    
def saveFiles():

    global ptStack
    fname = filename.split('.', 1)[0]
    with open(fname + '.err', "a") as myfile:
        for i in errorList:
            
            myfile.write(i + '\n')

    ptStack = ptStack[::-1]
    for i in ptStack:
        a = 'Exiting: ' + i
        pt.append(a)

    f = open(fname + '.tr',"w+")

    for i in pt:
        f.write(i + '\n')

    f.close()
    
filename = 'test11.pj'
tokenList,errorList, symbolTable = la.lexMain(filename)
print('ErrorList: ', errorList)
start()
saveFiles()


#Wla.saveFiles(tokenList,errorList, symbolTable)


    

