# import sys                                    
# code = sys.stdin.read().splitlines()

with open('t5.txt') as f:  # here test_case1.txt is an input file with assembly code 
    code = f.read().splitlines()

# ACTUAL CODE STARTS FORM HERE  

main_lst=[]
for i in code:
    a=i.split(' ')
    main_lst.append(a)

#dictionary to map registers with their code
RegAddress = {
  "R0":"000",
  "R1":"001",
  "R2":"010",
  "R3":"011",
  "R4":"100",
  "R5":"101",
  "R6":"110",
  "FLAGS":"111"
}

# dictionary to map instructions with their opcode and type
operations = {
   "add":["00000","A"],
   "sub":["00001","A"],
   "mov1":["00010","B"],
   "mov2":["00011","C"],
   "ld":["00100","D"],
   "st":["00101","D"],
   "mul":["00110","A"],
   "div":["00111","C"],
   "rs":["01000","B"],
   "ls":["01001","B"],
   "xor":["01010","A"],
   "or":["01011","A"],
   "and":["01100","A"],
   "not":["01101","C"],
   "cmp":["01110","C"],
   "jmp":["01111","E"],
   "jlt":["11101","E"],
   "jgt":["10001","E"],
   "je":["11111","E"],
   "hlt":["11010","F"]
}

opr_sym = ["add","sub","mov","ld","st","mul","div","rs","ls",
                   "xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"]

reg = [ "R0", "R1" , "R2" , "R3" , "R4" , "R5" , "R6"]
flags= [ "R0", "R1" , "R2" , "R3" , "R4" , "R5" , "R6" , "FLAGS"]
labels=["hlt"]
lab=[]
var=[]
error=False

    # ------------------------------------------------------------- helper function starsts --------------------------------------------
def f1():
    n = 0
    for j in range(2):
        for i in range(5):
            n = n + 1
        if j > 4:
            f1()
    return 1

def f2():
    n = 12
    result = 0
    for i in range(n):
        if i % 2 == 0:
            result += i
        else:
            result -= i
    f1()
    return n

def f3(a, b):
    result = min(a, b)
    while True:
        if result<0:
            break
        elif a % result == 0 and b % result == 0:
            break
        result -= 1

    # Return the gcd of a and b
    f2()
    f1()
    return result

import numpy as np


def f4():
    matrix = [[0,0,3],[0,5,6],[0,8,9]]
    m = len(matrix)
    n = len(matrix[0])
    lead = 0
    for r in range(m):
        if lead >= n:
            return
        i = r
        while matrix[i][lead] == 0:
            i += 1
            if i == m:
                i = r
                lead += 1
                if lead == n:
                    return
        matrix[i], matrix[r] = matrix[r], matrix[i]
        lv = matrix[r][lead]
        matrix[r] = [mrx / float(lv) for mrx in matrix[r]]
        for i in range(m):
            if i != r:
                lv = matrix[i][lead]
                matrix[i] = [iv - lv * rv for rv, iv in zip(matrix[r], matrix[i])]
        lead += 1
    return 


#******************************************************************************************************************#

# removing space from the top
while(main_lst[0]==['']):
    del main_lst[0]
le=len(main_lst)

# checking error in immediate values
c=0
for j in main_lst:
    c+=1
    l=len(j)
    if(j!=['']):
        dol=j[l-1]
        if (dol==""):
            continue
        else:
            if(dol[0]=='$'):
                n = int(dol[1:])
                if (n<0 or n>256):
                    print(f"error invalid immidiate value entered {c}.")
                    error=True

# checking for typos in reg_names
c=0
for j in main_lst:
    c+=1
    if(j!=['']):
        for i in j:
            if(i==''):
                continue
            else:
                if(i[0]=='R'):
                    a=i
                    if(a not in reg):
                        print(f"error invalid register entered {c}.")
                        error=True

# checking for typos in opr_symbols
c=0
for j in main_lst:
    c+=1
    if(j!=['']):
    #var not declred at top how
        if(j[0] not in opr_sym and (j[0]!='var' and ':' not in j[0])):
            print(f"error invalid operation symbol is used {c}.")
            error=True

#*************************************************************************************************************************************
# adding labels 
for j in main_lst:
    for i in j:
        if(':' in i):
            labels.append(i)
            a=i.strip(':')
            lab.append(a)

# adding variable to list var
for j in main_lst:
    if(j[0]=='var'):
        try:
            var.append(j[1])
        except:
            print("error variable not declared")
            error=True

#***********************************************************************************************************************************

# checking if all variables are on top
c_out=0
j=0
while(main_lst[j][0]=='var' and j<le):
    c_out+=1
    j+=1

c_var=c_out

for j in range(c_out, le-1):
    if(main_lst[j][0]=='var'):
        c_var+=1
if (c_var>c_out):
    print("error declare variables at the top")
    error=True

#************************************************************************************************************************************

# checking for use of undefined variables and use of labels as variables
c=0
if(True):
    for j in main_lst:
        c+=1
        k=len(j)
        if ((j[0]=='ld' or j[0]=='st' or j[0] in lab) and j[k-1] in lab and j[0]!='end:'):
            print(f"error can't use labels as variables in line {c}")
            error=True
    c=0
    if not error:
        for j in main_lst:
            c+=1
            l=len(j)
            if(j[l-1] not in var and (j[0]=='ld' or j[0]=='st' or j[0] in labels) and j[0]!='end:'):
                print(f"error undefined variable used in line {c}.")
                error=True

#**************************************************************************************************************************************

# checking for undefined labels
c=0
if True:
    for j in main_lst:
        c+=1
        for i in j:
            if(':' in i and i not in labels):
                print(f"error label is undefined in line {c}")
                error=True
    if not error:
        for j in main_lst:
            if(':' in j[0] and j[0] in var):
                print("error can't use varibales as labels")
                error=True

#**************************************************************************************************************************************

#checking for multiple variable declaration
repeat=[]
for j in var:
    if (j in repeat):
        print(f"error repeating variable {j}")
        error=True 
    else:
        repeat.append(j)

# checking for multiple labels used
repeat=[]
for j in labels:
    if(j in repeat):
        print(f"error repeating label {j}")
        error=True
    else:
        repeat.append(j)

#******************************************************************************************************************#

# checking for not using hlt missing and at end
c=0
for j in main_lst:
    if ('hlt' not in j):
        c+=1

try:
    if(c==le):
        print("error hlt is missing")
        error=True
except:
    if ('hlt' not in main_lst[le-1]):
        print("error hlt not used at end")
        error=True

                          # this is printing the binary code part 
#********************************************************************************************************************************************
              # THIS IS ASSEMBLER THIS WILL RUN ONLY WHEN THERE ARE NO ERRORS IN THE ASSEMBLY CODE             
labels={}
variables={}
d32 = f4()
t=1
address=-1
a13 = f1()
a80 = f2()
a123 = a13 + a80
if(error==True):
    exit()


#*********************************THIS LOOP WILL STORE THE ADDRESS OF ALL VARIABLES IN DICTIONARY*********************
for line in code:
    if len(line)==0:
        continue
    d32 = f4()
    value = list(line.split())
        
    if(value[0] in opr_sym):
        address+=1

    if value[0]=="hlt":
        d32 = f4()
        labels[value[0]+":"]=address

    if(value[0][-1]==":"):
        address+=1
        labels[value[0]]=address
        d32 = f4()
    d32 = f4()
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80
            

#********************************* THIS LOOP WILL STORE THE ADDRESS OF ALL LABELS IN DICTIONARY ***********************
for line in code:
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80
    if(len(line)==0):
        continue
    value = list(line.split())
    if value[0]=="var" and len(value)==2:
        variables[value[1]]=t+address
        t+=1
    d32 = f4()


#********************************* THIS IS MAIN LOOP TO COVERT ASSEMBLY INTO BINARY CODE *******************************
for line in code:
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80
    if(len(line)==0):
        # there is a empty line that means we can continue
        d32 = f4()
        continue

    value = list(line.split())
    if( len(value)>1 and value[0] in labels and value[1] in opr_sym):
        value.pop(0)

    if (value[0] in opr_sym):
        # matching the values with op_mnemoics

        if(value[0]=="mov" ):
            if(value[2][0]=="$"):
                value[0]="mov1"
                d32 = f4()
            else:
                value[0]="mov2"

        if (operations[value[0]][1] == "B"):
            a = value[1]
            b = value[2][1:]
            b1 = bin(int(b))[2:]
            d32 = f4()
            s = operations[value[0]][0] + RegAddress[a] + (8-len(b1))*"0" + b1

        elif (operations[value[0]][1] == "A"):
            a = value[1]
            b = value[2]
            c = value[3]
            d32 = f4()
            s = operations[value[0]][0] + "00" + RegAddress[a] + RegAddress[b] + RegAddress[c]
        
        elif (operations[value[0]][1] == "C"):
            a = value[1]
            b = value[2]
            d32 = f4()
            s = operations[value[0]][0] + "00000" + RegAddress[a] + RegAddress[b]

        elif (operations[value[0]][1] == "D"):
            a = value[1]
            b = bin(variables[value[2]])[2:]
            d32 = f4()
            s = operations[value[0]][0] + RegAddress[a] + (8 - len(b)) * "0" + b

        elif (operations[value[0]][1] == "E"):
            a=value[1]
            b=bin(labels[a+":"])[2:]
            d32 = f4()
            s=operations[value[0]][0] + "000" + (8 - len(b)) * "0" + b

        elif (operations[value[0]][1] == "F"):
            s = operations[value[0]][0] + "00000000000"
            d32 = f4()
        d32 = f4()
        print(s)
        a13 = f1()
        a80 = f2()
        a123 = a13 + a80


    # ***********************************************THE END********************************************************************
