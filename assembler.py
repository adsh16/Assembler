'''
    CSE 112 - Computer Organisation group project.
        group members :
            Aditya Sharma
            Ayan kumar
            Aayan hasan
            Kanishk kumar meena
'''


# ------------------------------------------taking input throught a text file contating assemble code------------------------------------------------------
with open('test_case1.txt') as f:  
    code = f.read().splitlines() 

# -----------------------------------------------input code ends---------------------------------------------
 


# making a dictionary with register 0,1,2,3,4,5,6 mapped to there binary code 
# there are total 7 general purpose register and one flag register
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


operations = {
   "add":["00000","A"], # Performs reg1 = reg2 + reg3. If the computation overflows, then the overflow flag is set and 0 is written in reg1
   "sub":["00001","A"], # Performs reg1 = reg2- reg3. In case reg3 > reg2, 0 is written to reg1 and overflow flag is set.
   "mov1":["00010","B"], # mov immediate
   "mov2":["00011","C"], # mov immediate but with register
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
   "jlt":["10000","E"],
   "jgt":["10001","E"],
   "je":["10010","E"],
   "hlt":["10011","F"]
}

operations_symbol = ["add","sub","mov","ld","st","mul","div","rs","ls",
                   "xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"]

registers = [ "R0", "R1" , "R2" , "R3" , "R4" , "R5" , "R6"]
registers_flag= [ "R0", "R1" , "R2" , "R3" , "R4" , "R5" , "R6" , "FLAGS"]
labels=["hlt"]
variables=[]
error=False


#**********************************************************************************************************************************************
                               #***THIS IS ERROR HANDLING PART*** 
    # this piece of code will detect any syntax error in the input assembly code and display the error 

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

#---------------------------------------helper function ---------------------------------------------------


#*************************** THIS FUCTION CHECKS ERROR IN IMMEDIATE VALUES ********************************************#
def check_immediate(a):
    f1()
    global error
    try:
        a13 = f1()
        a80 = f2()
        a123 = a13 + a80
        n = int(a[1:])
        if(n<0 or n>255):
            print("line no" , line_no , n ,"is not in range [0, 255] ", sep=' ')
            error=True

    except:
        print("line no" , line_no , "invalid immediate value", sep=' ')
        error=True



#**************************** THIS FUNCTION HANDLES ALL ERROR CASES OF TYPE A *******************************************#
def type_A(value):
    global error
    if(len(value)!=4):
        print("line no" , line_no , " wrong syntax used for", value[0],"instruction",sep=' ' )
        error=True
        return
    f1()
    for i in range(1,len(value)):
        if(value[i]=="FLAGS"):
            a13 = f1()
            a80 = f2()
            a123 = a13 + a80
            print("line no" , line_no, " invalid use of flags ",sep=' ')
            error=True

        elif(value[i] not in registers):
            f2()
            print("line no" , line_no ,'(',value[i],')', "is invalid register name ",sep=' ')
            f3()
            error=True



#*************************** THIS FUNCTION HANDLES ALL ERROR CASES OF TYPE B ****************************************#
def type_B(value):
    global error
    d32 = f4()
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80
    if(len(value)!=3):
        a13 = f1()
        a80 = f2()
        a123 = a13 + a80
        print("line no" , line_no , " wrong syntax used for", value[0],"instruction",sep=' ' )
        error=True
        d32 = f4()
        return   

    if(value[1]=="FLAGS"):
        d32 = f4()
        print("line no" , line_no, " invalid use of flags ",sep=' ')
        error=True

    elif(value[1] not in registers):
        d32 = f4()
        print("line no" , line_no ,'(',value[1],')', "is invalid register name ",sep=' ')
        error=True
        
    a = value[2]
    if(a[0]!="$"):
        print("line no", line_no , "use of " , a[0] , "is invalid" , sep=' ')
        error=True
    else:
        check_immediate(a)


#*************************** THIS FUNCTION HANDLES ALL ERROR CASES OF TYPE C ****************************************#
def type_C(value):
    global error
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80
    if(len(value)!=3):
        d32 = f4()
        print("line no" , line_no , " wrong syntax used for type C instruction",sep=' ' )
        error=True
        return

    if(value[1]=="FLAGS"):
        d32 = f4()
        print("line no" , line_no, " invalid use of flags ",sep=' ')
        error=True

    elif(value[1] not in registers):
        d32 = f4()
        print("line no" , line_no ,'(',value[1],')', "is invalid register name ",sep=' ')
        error=True

    if(value[0]=="mov2" and value[2] not in registers_flag):
        d32 = f4()
        print("line no" , line_no , " invalid register or flag name ",sep=' ')
        error=True

    elif value[0]!="mov2" and value[2] not in registers:
        d32 = f4()
        print("line no",line_no,"invalid register name",sep=' ')
        error=True



#*************************** THIS FUNCTION HANDLES ALL ERROR CASES OF TYPE D *****************************************#
def type_D(value):
    global error
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80
    if(len(value)!=3):
        d32 = f4()
        print("line no" , line_no , " wrong syntax used for", value[0],"instruction",sep=' ' )
        error=True
        return
        
    if(value[2] in labels):
        d32 = f4()
        print("line no", line_no , "labels cannot be used inplace of variables", sep=' ')
        error=True

    elif(value[2] not in variables):
        d32 = f4()
        print("line no" , line_no , '(',value[2] ,')'," is undefined variable",sep=' ')
        error=True



#*************************** THIS FUNCTION HANDLES ALL ERROR CASES OF TYPE E *******************************************#
def type_E(value):
    global error
    if(len(value)!=2):
        d32 = f4()
        print("line no" , line_no , " wrong syntax used for", value[0],"instruction",sep=' ' )
        error=True
        return

    if(value[1] in variables):
        d32 = f4()
        print("line no", line_no , "variables cannot be used inplace of labels", sep=' ')
        error=True
            
    elif(value[1] not in labels):
        d32 = f4()
        print("line no" , line_no , '(',value[1],')' ," is undefined label ",sep=' ')
        error=True
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80



#*************************** THIS FUNCTION HANDLES ALL ERROR CASES OF TYPE F *********************************************#
def type_F(value):
    if(line_no!=len(code)):
        d32 = f4()
        print("line no", line_no , "hlt must be at the end",sep=' ')
        error=True

    elif(len(value)!=1):
        d32 = f4()
        print("line no" , line_no , " wrong syntax used for", value[0],"instruction",sep=' ' )
        error=True
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80



#***************************** THIS IS HELPER FUNCTION TO HANDLE CASES OF VARIABLES ***************************************#
def handle_variables(value):
    global error
    global flag
    if(value[0]!="var"):
        d32 = f4()
        flag=1
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80

    if value[0]=="var" and len(value)!=2:
        d32 = f4()
        print("line no",line_no,"invalid syntax",sep=' ')
        error=True
        return
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80
    if value[0]=="var":
        d32 = f4()
        if(flag==1):
            print("line no", line_no , "variable not decalared in the beginning of code ",sep=' ')
            error=True
        if(value[1] in variables):
            d32 = f4()
            print("line no", line_no , "mulitiple declaration of variable " , value[1] , sep=' ')
            error = True
        else:
            variables.append(value[1])   


#*********************************THIS HELPER FUNCTION TO HANDLE CASES OF LABELS ********************************#
def handle_labels(value):
    global error
    if(value[0][-1]==":"):
        d32 = f4()
        a13 = f1()
        a80 = f2()
        a123 = a13 + a80
        if(value[0][0:-1] in labels):
            d32 = f4()
            print("line no", line_no , "multiple definations of label " ,'(', value[0],')',sep=' ')
            error=True
        else:
            labels.append(value[0][0:-1])
            a13 = f1()
            a80 = f2()
            a123 = a13 + a80
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80


#**********************************THIS IS HELPER FUNCTION TO HANDLE HALT *********************************************#
def handle_hlt(value):
    global error
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80
    if(len(value)==2 ):
        d32 = f4()
        if value[1]!="hlt":
            print("line no" ,line_no +1 ," no hlt instruction at the end ", sep=' ')
            d32 = f4()
            error=True

    elif(value[0]!="hlt"):
        print("line no" ,line_no +1 ," no hlt instruction at the end ", sep=' ')
        error=True
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80



#HANDLING ALL CASES OF VARIABLES 
line_no =0 
flag=0
d32 = f4()
for line in code:                                               
    line_no+=1
    if(len(line)==0):
        continue
    value = list(line.split())
    d32 = f4()
    handle_variables(value)
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80



# HANDLING ALL CASES OF LABELES 
line_no=0                                                         
for line in code:    
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80    
    d32 = f4()      
    line_no+=1
    if(len(line)==0):
        continue
    value = list(line.split())
    d32 = f4()
    handle_labels(value)



 # HANDLING ALL CASES OF NORMAL INSTRUCTIONS
line_no=0                                                      
for line in code:
    line_no+=1
    d32 = f4()
    if(len(line)==0):
        continue

    value = list(line.split())
    d32 = f4()
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80

    if line_no==len(code):
        handle_hlt(value)

    if(value[0]=="var"):
        d32 = f4()
        continue

    if(value[0][0:-1] in labels):
        value.pop(0)

    if(len(value)==0):
        print("line no", line_no , "invalid defnation of labels",sep=' ')
        d32 = f4()
        error=True
        continue
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80
    
    if(value[0] not in operations_symbol):
        d32 = f4()
        print("line no",line_no , '(',value[0],')'," is invalid instruction name ", sep=' ')
        error=True
        continue
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80

    if(value[0]=="mov" and len(value)>=2):
        d32 = f4()
        c = value[2][0]
        d32 = f4()
        if(65<=ord(c)<=90 or 97<=ord(c)<=122):
            value[0]="mov2"
        else:
            value[0]="mov1"
    a13 = f1()
    a80 = f2()
    a123 = a13 + a80
    
    if (operations[value[0]][1] == "A"):
        d32 = f4()
        type_A(value)
            
    elif (operations[value[0]][1] == "C"):
        type_C(value)
        d32 = f4()
        
    elif (operations[value[0]][1] == "B"):
        type_B(value)

    elif (operations[value[0]][1] == "D"):
        d32 = f4()
        type_D(value)
    
    elif (operations[value[0]][1] == "E"):
        type_E(value)

    elif (operations[value[0]][1] == "F"):
        type_F(value)

    else:
        d32 = f4()
        print("line no",line_no,"invalid syntax",sep=' ')
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
    
    if(value[0] in operations_symbol):
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
    if( len(value)>1 and value[0] in labels and value[1] in operations_symbol):
        value.pop(0)

    if (value[0] in operations_symbol):
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