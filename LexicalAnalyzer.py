#######################################################################
# LEXICAL ANALYZER - BY URWA FATIMA (uf00983) & TALAL ZAHID (tz01815) #
#                                                                     #
# To Run, enter the file name (without quotation marks) when prompted #
# by the console.                                                     #
#######################################################################




isStringB = False #to check if a string is being read indicated by encountering ". Resets when another " is encountered.
isComment = False #is true when # is encountered and remains true till new line begins
isMultiLineComment = False #is true when #/ is encountered and remains true till #/
isDigitB = False
midStringQuote = False
floatCheck = False
varCheck = False
commentCheckSingle = False
commentCheckMultiple = False
eofCheck = False
lastElement = False
notNull = False
validID = True
isEmptyBuffer = True
quoteCount=0
quoteLine = 0
line=1
opCount = 0
state = 0
symbolTableIndex = 0
cMLine = line
buffer=[]
symbolTable = []
symbolTableTemp = [] 
tokenBuffer = []
tokenList =[]
errorList =[]


#asciiLowerCase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
#numbers = ['0','1','2','3','4','5','6','7','8','9']


#Valid Keywords in this language
keyWords = ['END', 'def', 'for', 'range', 'while', 'TRUE', 'FALSE', 'if', 'else', 'else if', 'return', 'NULL', 'input', 'var', 'int', 'str', 'and', 'or', 'not']

#Valid alphanumeric characters in this language
caps = range(ord('A'), ord('Z')+1)
small = range(ord('a'), ord('z')+1)
nums = range(ord('0'),ord('9')+1)

#Valid symbols in this language
symbols= ['(' , ')' , ',' , ';' , ':','{','}','[',']']

#Valid operators in this language
operators={'+':'plus', '-':'minus', '*':'multiply', '/':'divide', '//':'fdivide',
           '%':'mod', '**':'power' ,'=':'assign',
           '+=':'plus_assign', '-=':'minus_assign', '*=':'mult_assign', '/=':'div_assign',
           '<':'LT','>':'GT','==':'EQ','<=':'LEQ','>=':'GEQ','!=':'NEQ' }
logicalOperators={'and':'logical_and', 'or':'logical_or', 'not':'logical_not'}



def lexMain(fname):

    global prog,fileName,progLen
    
    #fname = input("Input File Name: ")
    prog = open(fname, 'r').read()
    fileName = fname.split('.', 1)[0]
    progLen = len(prog)
    mainLoop()
    saveFiles()

    return tokenList,errorList, symbolTableTemp
    #popUpResult()


#Checks if the character is from 0-9 or '.' in case of float.
def isDigit(i):
    
    global floatCheck
    if (ord(i) in nums):

        return True

    elif ((i == '.' and len (buffer) > 1)and floatCheck == False):
        floatCheck = True
        return True
    
    elif (i == '.' and floatCheck == True):
        return False
             
    else:
        return False

#Checks for inverted commas (or single quotation marks)
def quoteCheck(i):

    if (i == '\''):
        return True
    else:
        return False

#Checks for inverted commas (or single quotation marks)
def tokenize(lexeme, category):
    global state, tokenList

    if (category == 'punctuation'):
        a = '<' + (''.join([str(x) for x in lexeme])) + ',' + str(line)+ '>'

    elif (category == 'identifier'):
        a = '<' + category + ',' + str(lexeme) +',' + str(line)+ '>'
    else:
        a = '<' + category + ',' + (''.join([str(x) for x in lexeme])) +',' + str(line)+ '>'
    tokenList.append(a)
    buffer = []
    state = 0
 
#Clears buffer of all elements
def clearBuffer():

    global buffer

    buffer = []

#Change state of main Loop
def changeState(x):

    global state

    state = x

#Checks if float has already occurred in a number
def clearFloatCheck():

    global floatCheck

    floatCheck = False


#Checks if hashtag '#' has occurred
def commentCheck(i):

    if i == '#':
        return True
    else:
        return False

#Checks digit pattern and tokenizes them
def stateDigits(i, buffer):
        
    if (isDigit(i)):
        if (lastElement):
            tokenize(buffer, 'int')
            clearBuffer()
            clearTokenBuffer()
            changeState(0)
        
        clearTokenBuffer()
        return True
    
    elif ((i == ' ' or i == '\n') or isPunctuation(i) or operatorCheck(i) or quoteCheck(i) or checkValidCharacter(i)):
        
        if (isPunctuation(i) or operatorCheck(i) or quoteCheck(i) or checkValidCharacter(i)):

            if (floatCheck):
                tokenize(buffer[:-1], 'float')
            else:
                tokenize(buffer[:-1], 'int')
            deleteTillNthBufferElement(-1)

        else:
            deleteNthBufferElement(-1)

            if (floatCheck):
                tokenize(buffer[:-1], 'float')
            else:
                tokenize(buffer[:-1], 'int')
            clearTokenBuffer()
            clearBuffer()
        changeState(0)
        
        clearFloatCheck()
        return True   
    else:
        return False

#Checks for logical operators from keywords (and, not, or)
def isLogicalOperator(a):

    if a in logicalOperators.keys():
        return True
    else:
        return False   
   
#Checks strings pattern and tokenizes them
def stateString(i, buffer):

    global midStringQuote, quoteCount, quoteLine

    if i == '\n':
        changeNthBufferElement(-1,'\\n')
    
    if (quoteCheck(i)):
        
        if (len(buffer) > 1):
           
            if (buffer[-2] == '\\'):
                deleteNthBufferElement(-2)
                midStringQuote = True
            
        if (not midStringQuote) and (quoteCount ==0):
            quoteLine = line
           
        if (quoteCount < 2 and midStringQuote == False):
            
            quoteCount +=1

        if((quoteCount==2 and midStringQuote == False)):

            quoteCount = 0
            deleteNthBufferElement(-1)
            if (buffer[0] == '\''):
                del buffer[0]
            tokenize(buffer, 'str')
            clearBuffer()
            changeState(0) 

    midStringQuote = False
    clearTokenBuffer()    
    return True

#removes n buffer elements
def deleteTillNthBufferElement(x):
    global buffer

    del buffer[:x]
    
#removes nth buffer element
def deleteNthBufferElement(x):
    global buffer

    del buffer[x]

#Checks for whitespace ' '
def checkWhiteSpace(i):

    if i == ' ' or i =='\t':
        return True

    else:
        return False

#Checks for new Line '\n'
def checkNewLine(i):

    if i == '\n':
        return True

    else:
        return False

#Increases line count
def incrementLine():

    global line

    line +=1

#Checks if its a valid AlphaNumeric Character
def isString(i):

    if (((ord(i) in caps) or (ord(i) in small))):
       
        return True
    else:
        return False

#Checks if its a valid Identifier Name
def isIdentifier(word, f):
   
    global symbolTable, notNull, symbolTableIndex, symbolTableTemp

    if word in symbolTableTemp:
        tokenize(word,'identifier')

        if f:            
            changeBufferToNthElement(-1)
        else:
            clearBuffer()
            clearTokenBuffer()

        changeState(0)
        notNull = False
        return True
    
    elif (word[0] == "_") or (ord(word[0]) in caps )or (ord(word[0]) in small):
        for i in range(1,len(word)):
            if (not (ord(word[i])in nums or ord(word[i]) in caps or ord(word[i]) in small or word[i] == '_') and len(word) > 1):

                notNull = False        
                return False
                               
        symbolTableTemp.append(word)
        print('Word added to table: ', word)
        tokenize(symbolTableIndex,'identifier')
        symbolTableIndex += 1

        if f:          
            changeBufferToNthElement(-1)
        else:
            clearBuffer()
            clearTokenBuffer()

        changeState(0)
        notNull = False
        return True
    else:
        notNull = False
        return False
    
#Checks for a valid punctuation mark
def isPunctuation(character):
    if character in symbols:
        return True
    else:
        return False

#Checks for a valid character recongnized by this language
def checkValidCharacter(i):

    if (operatorCheck(i) == True or isPunctuation(i) == True or quoteCheck(i) or (ord(i) in caps) or (ord(i) in small)
        or (ord(i) in nums) or (i in symbols) or i ==' ' or i == '\n' or i =='\t'):

        return True
    else:
        return False

#Checks for KeyWords or Identifier patterns, differentiates between them and tokenizes them accordingly
def stateKeyWordorIdentifier(i, buffer):

    global varCheck, eofCheck, notNull, validID
    
    tokenizer = False
    a=[]
    if i == ' ' or i == '\n': 

        deleteNthBufferElement(-1)
        a = (''.join([str(x) for x in buffer]))
        tokenizer = True
    elif (lastElement == True):
        a = (''.join([str(x) for x in buffer]))
        tokenizer = True
    elif (operatorCheck(i) == True or isPunctuation(i) == True or quoteCheck(i) or i == '#' or checkValidCharacter(i) == False ):
        a = (''.join([str(x) for x in buffer[:-1]]))
        tokenizer = True
        notNull = True

    if (not checkValidCharacter(i)):
        
        validID = False

    if a in keyWords and tokenizer == True:

        if (a == 'END' and eofCheck == False):
            tokenize(a,'keyword')
            eofCheck = True

        else:

            if a in logicalOperators.keys():
                
                tokenize(a,logicalOperators.get(a))
            else:
                tokenize(a,'keyword')
            if notNull:
                changeBufferToNthElement(-1)
            else:
                clearBuffer()
                clearTokenBuffer()

        tokenizer = False
        changeState(0)
        notNull = False
        return True

    elif(tokenizer == True):
        if notNull:
            
            changeBufferToNthElement(-1)
        else:
            clearBuffer()
            clearTokenBuffer()

        return isIdentifier(a,notNull)
    clearTokenBuffer()
    return True


#Checks for Single or MultiLine comments and their pattern '#' or '#/'
def stateComment(i, buffer):

    global commentCheckSingle, commentCheckMultiple, cMLine
    
    if (i == '#' and commentCheckSingle == False and commentCheckMultiple == False):

        commentCheckSingle = True
        
    elif (len (buffer) > 1 and i == '/'):
        
        if (buffer[-2] == '#'):

            if (commentCheckMultiple == False):
                commentCheckSingle = False
                commentCheckMultiple = True
                cMLine = line
                
            else:
                commentCheckMultiple = False
                changeState(0)
                clearBuffer()            

    elif (i == '\n' and commentCheckSingle == True):
            commentCheckSingle == False
            changeState(0)
            clearBuffer()
            
    clearTokenBuffer()

#Checks if the character is the last character of the script
def isLastElement(x):

    if x == progLen - 1:
        return True
    else:
        return False
    
#Checks if the EOF KeyWord 'END'is present and tokenizes it
def checkEOF(buffer,x,i):
    global eofCheck

    if i == ' ' or i == '\n' or (isLastElement(x)):
        if (not (eofCheck)):
            
            if ((''.join([str(x) for x in buffer])) == 'END'):
                tokenize(buffer, 'keyword')
                changeState(0)
                clearBuffer()
                clearTokenBuffer()
                eofCheck = True
                return True
            else:
                return False       
    else:
        return False   

#Checks if the Operator encountered is a valid operator
def operatorCheck(i):

    operators.get(i, 'invalid operator')

    if (operators.get(i, 'invalid operator')) == 'invalid operator':

        return False
    else:
        return True

#Changes the xth buffer element to y
def changeNthBufferElement(x,y):

    global buffer

    buffer[x] = y

#Changes the buffer so only xth element remains
def changeBufferToNthElement(x):

    global buffer

    buffer = [buffer[x]]

#Clears the Tokken buffer
def clearTokenBuffer():

    global tokenBuffer
    tokenBuffer = []

#Checks for valid operator patterns, like in case of dual operators '++' or '--', and tokenizes them
def stateOperator(i, buffer):

    global opCount 
    if (i == ' ' or i == '/n' or not operatorCheck(i) or opCount == 2) and (opCount < 3):
        lexeme = buffer[:-1]
        a = (''.join([str(x) for x in lexeme]))
        tokenize(operators.get(a, 'invalid operator'), 'operator')
        opCount = 0

        if (i == ' ' or i =='\n' ):
            clearBuffer()
            clearTokenBuffer()
        else:
            changeBufferToNthElement(-1)

        changeState(0)
        opCount = 0
        return True

    elif (opCount < 2):

        opCount +=1
        clearTokenBuffer()
        return True

    else:
        return False
    
#Checks if the buffer is empty
def checkIsBufferEmpty(buffer):

    if buffer == []:
        return True
    else:
        return False

#Checks for valid punctuations and tokenizes them
def statePunctuation(i, buffer):

    tokenize(buffer[-1], 'punctuation')
    clearBuffer()
    clearTokenBuffer()
    changeState(0)

#Saves the Symbol Table created for this script
def saveSymbolData():

    f = open(fileName + '.sym',"w+")

    for i in range (len(symbolTableTemp)):
        f.write(str(i) + ' ' + symbolTableTemp[i] +'\n')

    f.close() 

#Saves the Token Data created for this script
def saveTokenData():

    f = open(fileName + '.out',"w+")

    for i in tokenList:
        f.write(i + '\n')

    f.close()

#Saves the Error Log created for this script
def saveErrorData():

    f = open(fileName + '.err',"w+")

    for i in range (len(errorList)):
        f.write('Line: '+ errorList[i][0] + ' -  Error Code: '+ str(errorList[i][1])+' -  Error: '+ errorList[i][2] +
                ' at " ' + errorList[i][3] + ' \"'+' -  Status: '+errorList[i][4]+' -  Action: '+errorList[i][5] + '\n')

    f.close()

#Saves all files
def saveFiles():
    saveTokenData()
    saveErrorData()
    saveSymbolData()

#Creates a PoP-Up Message for the Compilation Results
def popUpResult():

    import ctypes   

    resolved = True
    if len(errorList) == 0:
        ctypes.windll.user32.MessageBoxW(0, "Compilation complete with no Errors.", "Compiler Result", 0)
    else:
        for i in errorList:
              if i[4] != 'Resolved':
                  resolved = False
        if (resolved):
                ctypes.windll.user32.MessageBoxW(0, "Compilation complete with Errors but were resolved.", "Compiler Result", 0)
        else:
                ctypes.windll.user32.MessageBoxW(0, "Compilation completed. Some Errors remain unresolved.", "Compiler Result", 0)

##################################################################################################################################################
# MAIN LOOP - IT RUNS CHARACTER BY CHARACTER, READING THE SCRIPT FILE PROVIDED.                                                                  #
#                                                                                                                                                #
# It first adds the character into a buffer and a temp buffer. While the temp buffer is not emptied, it checks the appropriate state to send     #
# the character into as defined by functions above. If it encounters an unrecongnized characted, an error is generated. If any of the states     #
# does not accept the character, an error is generated. The compiler employs some strategies to resolve the errors which are defined in the      #
# seperate document provided. The loop also checks when the End of File has been reached.                                                        #
##################################################################################################################################################

def mainLoop():

    global lastElement, buffer, tokenBuffer, state, validID, errorList
    for x in range(progLen):

        if (eofCheck):
            break
        if isLastElement(x):
            lastElement = True

        i=prog[x]
        buffer.append(i)
        tokenBuffer.append(i)

        while (tokenBuffer != []):

            if (eofCheck):
                break

            if checkNewLine(i):
                incrementLine()
            
            if state == 0:

                if checkWhiteSpace(i):
                    deleteNthBufferElement(-1)
                    clearTokenBuffer()
                    continue
                
                elif checkNewLine(i):
                    deleteNthBufferElement(-1)
                    clearTokenBuffer()
                    continue  

                elif (isDigit(i)):

                    state = 1

                elif (quoteCheck(i)):

                    state = 2

                elif (isString(i)):
                    state = 3

                elif (commentCheck(i)):

                    state = 5

                elif (operatorCheck(i)):

                    state = 6

                elif (isPunctuation(i)):

                    state = 7

                else:
                    errorList.append((str(line),1,'Unrecognized Character',i,'Resolved','Character Removed' ))
                    deleteNthBufferElement(-1)
                    break

            if state == 1:
                if not (stateDigits(i, buffer)):
                    print ('Error, encountered unrecongnized digit')

                    errorList.append((str(line),2,'Invalid Digit Sequence',i,'Resolved','Character Removed' ))
                    deleteNthBufferElement(-1)
                    break

            if state == 2:
                
                stateString(i, buffer)

            if state == 3:

                if (not stateKeyWordorIdentifier(i, buffer) or validID == False):

                    print ('Error, encountered unrecongnized or invalid Word')
                    errorList.append((str(line),3,'Invalid Character for Identifier Name',i,'Resolved','Tokenized prior to invalid character occured' ))
                    validID = True

            if state == 5:
                stateComment(i, buffer)

            if state == 6:
                
                stateOperator(i,buffer)

            if state == 7:
                statePunctuation(i, buffer)
                
                
            if isLastElement(x):
        
                if checkEOF(buffer,x,i) or eofCheck:
        
                    print('End Compilation')
                    break
                else:
                    
                    if(quoteCount > 0):
                        print('Qoutes not closed')
                        errorList.append((str(quoteLine),5,'Closing String Character Not Found','\'','Unresolved','Revision needed' ))

                    if (commentCheckMultiple):
                        errorList.append((str(cMLine),6,'Closing Comment Character Not Found','#/','Unresolved','Revision needed' ))
                        
                    print('Error: EOF Not Found!') 
                    errorList.append((str(line),4,'EOF Token Not Found','EOF','Resolved','EOF Token added to the Token File' ))
                    tokenize(['E','N','D'],'KW')
                    break
            
##saveFiles()
##popUpResult()
  





