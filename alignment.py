
#import numpy as np   # just to visualize table
import random
from sys import stdout      # allows progress
#str1 = ''
#str2 = 'EXPONENTIALPOLY'


def randomProtein(L):
    stringy = ''
    for i in range(L):   
        stringy += random.sample(['A','C', 'G', 'T'],1)[0]
    return stringy


rules = 'class'
rules = 'HW'

if ( rules == 'class'):
    # Values from lecture, also change max functions to min. 
    same = 0
    different = 1
    indel = 1
    swap = 3  
else:
    same = 0
    different = 10
    indel = 1    
    swap = 10

    
def CreateBase(x,y):
    #create table of len(x)+2, and len(y)+2 in dimensions.
    S = [[None]*(len(x)+2) for _ in range(len(y)+2)]   #table length x by length y  
    # Add to string to make it pretty
    x2 = '+-' + x             
    y2 = '-' + y    
    # Add string characters to array
    for i in range(0,len(x2)):
        S[0][i] = x2[i]
    for i in range(0, len(y2)):
        S[i+1][0] = y2[i]    
    # Align the '-' character to zero
    S[1][1]= 0
    
    # By definition '-' character will not match any other. 
    # Maybe later change to max(len(y), len(x)), and include error handling to prevent two loops.
    for i in range(2, (len(y)+2)):        
        S[i][1] = S[i-1][1]+1           
    for i in range(2, len(x)+2):        
        S[1][i] = S[1][i-1]+1 
    return S


def sub(S,x,y):
    if (S[x][0] == S[0][y]):  return same
    else: return different
        
def a(S,x,y):
    return (S[x][y-1]+indel)
   
def b(S,x,y):
    return (S[x-1][y]+indel)

def c(S,x,y):    
    return (S[x-1][y-1]+sub(S,x,y))
    
def d(S,x,y):
    return (S[x-2][y-2]+swap)
    
    

    
    
def cost(S, x, y):
    #row 2 and col 2 cannot use function d since this is outside indice bound
    if ((y == 2) or x == 2): 
        return (min( a(S,x,y) , b(S,x,y), c(S,x,y)))        
    # all other values can acces any function (a,b,c,d)   
    if  ((x >= 3) and (y >= 3)):
        return (min(a(S,x,y),b(S,x,y),c(S,x,y),d(S,x,y)))        
    
def alignStrings(x,y):       
    S = CreateBase(x,y) 
    
    pct = len(S)/100 
    
    for i in range(2, len(S)):
        #if ((i % int(pct) == 0) and (len(S) > 4000)): 
        #    val = i/int(pct)
        #    stdout.write("\r%.f" % val+ " percent complete")	    # progress indicator

        for j in range (2, len(S[0])):
            S[i][j] = cost(S, i, j)           #return optimal cost.         
    #stdout.write("\r100 percent complete\n")
    #stdout.write("\r100 percent complete\n")
    #print(np.matrix(S))
    return S



    
def determineOptimalOp(S, x, y):
    # This happens if first column, can only go up. 
    if (x == 1):
        return ('d', [x, y-1])  #insert delete, new indice value. 
       
    # This happens if first row, can only go left. 
    if (y == 1):
        return ('i', [x-1, y]) # indel and new indice value. 
        #return(x-1,y)
    # All other cases
    else:       
        # d can only be for rows and columns greater than 3
        prev = [a(S,x,y), b(S,x,y), c(S,x,y)]
        if  ((x >= 3) and (y >= 3)):       
            prev.append(d(S,x,y))
           
    return(findNext(S,x,y,prev))


    
def findNext(S, x, y, poss):
    # Now we have a list of all possible moves, in an array that is [top, left, diag_1, diag_2] 
    # list of 3 or 4 items. Corresponds to move made. 
  
    nextMove = []
    #Check if the current location S[x][y]
    for i in range(0, len(poss)):
        if (poss[i]== S[x][y]):       
            # add the char a-> d to poss matrix. 
            nextMove.append(chr(i+97))
            
    if (len(nextMove) > 1):
        # pick a random. 
        # random.randint(0, last index) returns a random value. 
        nextMove[0] = nextMove[random.randint(0,len(nextMove)-1)]
    
    
    move = ''
    updateIndice = []
    #compare the character to value. 
    if (nextMove[0] == 'a'):
        #indel, 
        move = 'd'
        updateIndice = [x,y-1]
        
        
    elif (nextMove[0] == 'b'):
        move = 'i'
        updateIndice = [x-1,y]
        
        
    elif (nextMove[0] == 'c'):
        move = 'su'
        updateIndice = [x-1, y-1]
        # if doing sub op, but both values are the same. Then we return the same value. 
        
        if (S[x][y] == S[x-1][y-1]):
            move = 'n'
        
    elif (nextMove[0] == 'd'):
        move = 'sw'
        updateIndice = [x-2, y-2]
        
    return (move,updateIndice)   
        
        
def updateIndices(S,x,y,a):
    print('update this')
    
    
    
    
def extractAlignment(S ,x, y):  
    a = []                            #empty vector of edit operations   
    j = len(x)+1
    i = len(y)+1    
    
    while ((i > 1) or (j >1)) :        
        move, next =  determineOptimalOp(S,i,j) # what is the optimal choice?   
        a.insert(0,move)
        [i,j] = next    #update indices function, not needed. 
              
    
    return a
       
def commonSubstrings(word ,L,  a):
    strings = []
    begin = -1
    count_d = 0
    for i in range(len(a)):        
        if (a[i] != 'n'):             
            if(begin >= 0): #end of the string
                #need to find the string from begin to i-1- d_count                
                strings.append(word[(begin - count_d):(i-count_d)])
                begin = -1
            if (a[i] == 'd'):
                count_d += 1
        elif (begin < 0 ): # a[i] == n, but there is no current string processing. 
            begin = i
        elif(i == len(a)-1):   #end of array with current string processing
            strings.append(word[(begin - count_d):(i-count_d+1)])
     
    #can be a weird case where terminates last value is         
            
    
    long_enough = [strings[i] for i, val in enumerate(strings) if (len(val) >= L)] 
    return long_enough

def runAll(L, N):
    str1 = randomProtein(L)
    str2 = randomProtein(L)
    print('strings made')
    fin = extractAlignment(alignStrings(str1,str2), str1, str2)
    print('alignment extracted')
    commonSubstrings(str2, N, fin)
    
    
def runLiberalAgendaFiles():
    N = 10
    with open('csci3104_S2017_PS6_data_string_x.txt', 'r', encoding = 'utf8') as f:
        str1 = f.read()
    with open('csci3104_S2017_PS6_data_string_y.txt', 'r',encoding = 'utf8') as f:
        str2 = f.read()
    
    fin = extractAlignment(alignStrings(str1,str2), str1, str2)
    print('alignment extracted')
    results =  commonSubstrings(str2, N, fin)
    with open('LIEberalMedia.txt','w', encoding = 'utf8') as f:
        for i in range(len(results)):
            f.write(results[i]+ '\n')

def TrumpDidNothingWrong():
    N = 5
    str1 = '“We hold these truths to be self-evident, that all men are created equal’ — just words. Just words. ‘We have nothing to fear but fear itself’-just words. ‘Ask not what your country can do for you, ask what you can do for your country’ — just words. ‘I have a dream’ — just words,”'
    str2 = '“Don’t tell me words don’t matter! ‘I have a dream.’ Just words. ‘We hold these truths to be self-evident, that all men are created equal.’ Just words. ‘We have nothing to fear but fear itself.’ Just words, just speeches,”'
    fin = extractAlignment(alignStrings(str1,str2), str1, str2)
    print('alignment extracted')
    results =  commonSubstrings(str2, N, fin)
    with open('illuminatiConfirmed.txt','w', encoding = 'utf8') as f:
        for i in range(len(results)):
            f.write(results[i]+ '\n')

TrumpDidNothingWrong()
#runLiberalAgendaFiles()
#runAll(1000,5)

def randomizeFreqChar(lines):
    freq= []
    chr = []
    randChrArray = []
    for i in range(len(lines)):
        chr.append(lines[i][1])
    
        freq.append(int(lines[i][4:]))
    
    while (sum(freq) != 0):
        # get random value from 0 to length of freq. corresponds to char in 'chr'
        chr_val = random.randint(0, len(chr)-1)
        # append to new array
        randChrArray.append(chr[chr_val])  
        #decrement frequency by one
        freq[chr_val] -= 1
        #if we just added the last (1->0), remove from both lists. 
        if (freq[chr_val] == 0):
            freq.pop(chr_val)   # remove from array
            chr.pop(chr_val)    # remove from array
    return randChrArray    

def randomString(arr, n):
    str = ''
    for i in range(n):
        str += arr[random.randint(0, len(arr)-1)]
    return str
with open('csci3104_S2017_PS6_data_muchAdo_txt.txt', 'r', encoding = 'utf8') as f:
        shakingPears = f.read()
print(len(shakingPears))
    
def MonkeysTyping(n):
    
    with open('csci3104_S2017_PS6_data_muchAdo_freqs.txt', 'r', encoding = 'utf8') as f:
        lines = f.read().splitlines()
    print(len(lines))
    randArr = randomizeFreqChar(lines)
    randString = randomString(randArr, n)
    return randString

def findStringLengthForComparison(N):
    with open('csci3104_S2017_PS6_data_muchAdo_txt.txt', 'r', encoding = 'utf8') as f:
        shakingPears = f.read()
    matchLen = N
    max_val = N*(2**15) 
    # if want a match of at least 7, start with 7.  
    prev = 0
    minVal = -2
    # find the first case. 
    while (N <  max_val):
        print('trying :' + str(N))
        rString = MonkeysTyping(N)
        #print(rString)
        fin = extractAlignment(alignStrings(rString,shakingPears), rString,shakingPears)        
        matches = commonSubstrings(shakingPears, matchLen, fin)

        if (len(matches) != 0):
            max_val = N
            prev = int(N/2)
            #print('first match at N = ' + str(N))
           # print('match found; starting goal seek')
            break
        else: 
            #print('no match found for string length: ' + str(N))
            N*= 2
    N = int((N + prev)/2)
    while (abs(N - prev) > 4): #if these values are 3, we are very close to no more adjustments. 
        print('trying :' + str(N))
        rString = MonkeysTyping(N)
        #print(rString)
        fin = extractAlignment(alignStrings(rString,shakingPears), rString,shakingPears)        
        matches = commonSubstrings(shakingPears, matchLen, fin)
        if (len(matches) != 0): # N is too big
            if (N < prev):
                temp = N
                N = N - int((prev-N)/2) 
                prev = temp
            else:
                temp = N
                N = int((N+prev)/2)
                prev = temp
         
        else: #N is too small. 
            if (N > prev):
                temp = N
                N = N - int((N-prev)/2)
                prev = temp
            else: 
                temp = N
                N = int((N+prev)/2)
                prev = temp
    
    return N       

    
def Extrapolate(minStr,maxStr, numtimes):   
    SolArr = [[0 for x in range(numtimes)] for y in range(maxStr-2)]   
    for j in range(minStr, maxStr+1):
        print('str length is: ' + str(j))
        for i in range(numtimes):
            SolArr[j-2][i]= findStringLengthForComparison(j)
            print(SolArr)
    print(SolArr)

#Extrapolate(5,5,10)


def determineOptimalOpNonRandom(S, x, y):
    # This happens if first column, can only go up. 
    if (x == 1):        
        return [[ x, y-1]]  #insert delete, new indice value.        
    # This happens if first row, can only go left. 
    if (y == 1):
        return [[x-1, y]] # indel and new indice value. 
        #return(x-1,y)
    # All other cases
    else:       
        # d can only be for rows and columns greater than 3
        prev = [a(S,x,y), b(S,x,y), c(S,x,y)]
        
        if  ((x >= 3) and (y >= 3)):       
            prev.append(d(S,x,y))
           
    return findNextNonRandom(S,x,y,prev)
    
    
def findNextNonRandom(S, x, y, poss):
    # if value calculated = value at the current location [correct path], add to the moves array as a character. 
    
    moves = [chr(i+97) for i in range(len(poss)) if poss[i] == S[x][y]]
    
    #compare the character to value, lets try a python dictionary
    move_dict =  {'a' : [x,y-1], 'b' : [x-1,y], 'c': [x-1,y-1], 'd': [x-2,y-2] }
    # return the new indices in this format: [[x1,y1], [x2,y2],[x3,y3]]
    
    all_locs = [move_dict[moves[i]] for i in range(len(moves))]
    
    return all_locs
    
    
        
#input cost matrix s, x = max column, y = max row 
  
def findRoutes(S): 
    
    x = len(S)-1
    y = len(S[0])-1
    pArray = [[0]*(y+1) for _ in range(x+1)]   #table length x by length y  
    
    
    #start at the m*n value. 
    #looks for all the nodes that are part of a correct path. 
    newNodes = determineOptimalOpNonRandom(S, x, y)
        
    #start by looking at each possible route. 
    #tot = [countRoutes(S,x,y, newNodes[i], pArray) for i in range(len(newNodes))]
    sum = 0
    for i in range(len(newNodes)):
        
        sum += countRoutes(S, x,y , newNodes[i], pArray) 
        pArray[x][y] = sum
        
 #   print(np.matrix(pArray))
       

 
#input: cost, x,y, rout location.     
#output value for this one subpath
def countRoutes(S,x, y, prev, pArray ):
    #base case: in a node/ cell adjacent that relates to the root of the S matrix (either [0,1], [1,0],[1,1], [2,2]), and is a valid path.
    #return 1 in this case.
    #deal with base case, if next path = going to the root of the S matrix.
    print('routes')
    print(x,y)
    
    sum = 0 
    if (prev == [1,1]): #found a base case, could be other ways through this to the root.
        pArray[x][y]= 1
        
    if ( pArray[x][y] > 0): #found a previous solution
        return (pArray[x][y])
        
    if (pArray[x][y]  == 0): #hasn't been ran into previously
        
        pArray[x][y] = -1
        newNodes = determineOptimalOpNonRandom(S, prev[0], prev[1])
        
        for i in range(len(newNodes)):
            sum += countRoutes(S, prev[0], prev[1], newNodes[i],pArray)  
            pArray[x][y] = sum
            return sum
        
        
    if (pArray[x][y] < 0): #has been previously seen, but maybe from another location. 
        newNodes = determineOptimalOpNonRandom(S, prev[0], prev[1])
        
        for i in range(len(newNodes)):
            sum += countRoutes(S, prev[0], prev[1], newNodes[i],pArray) 
            pArray[x][y] = sum
            return sum
     
    
        
#do i need to drop paths that have no route?   
   
def BunchaPaths(Min,Max,Delta):   
    for i in range(Min,Max,Delta):
        
        print( findRoutes( alignStrings(randomProtein(i),randomProtein(i)) ) ) 

        
#BunchaPaths(10,40,10)
   
#print( findRoutes( alignStrings('APE', 'STEP') ) ) 
