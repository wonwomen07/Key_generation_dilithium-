#!/usr/bin/env python
# coding: utf-8

# In[1]:


#libaries used 

import hashlib
from bitstring import BitArray
import random
import hashlib
from bitstring import BitArray
import numpy as np


# # Taking any 256 bit sequence using random library

# In[2]:


def rand_key(p):
    g = ""
 
    for i in range(p):
         
        temp = str(random.randint(0, 1))

        g += temp
         
    return(g)
 
# Driver Code
n = 256
str1 = rand_key(n)
print("Desired length random binary string is: ", str1)
len(str1)


# # Running shake-256 by taking "str1" value  (256 bit sequence) as input and generating 1024 bits

# In[3]:


def hashing(str1):

#using hashlib module and shake128 algorithm .
    has = hashlib.shake_256()
    has.update((str1).encode('utf-8'))
    var = has.hexdigest(128)
    

#converting the hexadecimal values into string of bits.
    c = BitArray(hex=var)
    c=c.bin

#converting the sytring of bits into binary format.
    var = bin(int(c,2))
    return var
    
    
has_256 = hashing(str1)
print(has_256)


# # Parameters "rho" , "rho_dash" and "K" generated using the 1024 hashed bits using shake-256 where , rho=256 bits ,rho-dash=512 bits and K=256 bits.

# In[4]:


def param(has_256 ,n):
    
    str=has_256
    chunks=[str[i:i+n] for i in range(0, len(str) ,n)]
    #print(chunks)

    rho_dash = chunks[1] +chunks[2]
    

    rho , rho_dash , k = chunks[0] , rho_dash , chunks[3]

    print("----------***-----------")
    print(rho)
    print("length of rho is:" , len(rho))
    print("----------***------------")

    print(rho_dash)
    print("length of rho_dash is:" , len(rho_dash))
    print("----------***-------------")

    print(k)
    print("length of k is :" , len(k))
    print("----------***-----------")
    
    return rho , rho_dash , k

params = param(has_256 , 256)
print(params)

rho = params[0]    #rho value

rho_dash = params[1]   #rho_dash value

k = params[2]        #k value


# # To generate matrix A [EXPAND A(rho)]

# In[7]:


global mat
def matrix_A(rho , version):
    
    ak3 =[]
    
    # to get m and n value for a specified version
    
    def ver(version):
        if version==2:
            m=4
            n=4
        elif version==3:
            m=6
            n=5
        elif version==5:
            m=8
            n=7
            
        return m , n 
    vers = ver(version)
    
    m = vers[0]
    
    n  = vers[1]
        
    for i in range(1,vers[0]+1):
        for j in range(1,vers[1]+1):
            
            #to generate 256 values for each coefficient in matrix
            #256*i+j
        
            temp = 256*i+j
            
            #converting the 256*i+j into binary format(according to the process)
        
            bin = format(temp , '016b')
        
            n = 8
            byte = [bin[i:i+n] for i in range(0,len(bin) , n)]

            #16 bits of little endian format of 256*i+j
        
            byte[0] , byte[1] = byte[1] , byte[0]
            byte = byte[0] +byte[1]

            #next rho||16 bits of little endian format of 256*i+j [rho||byte]
        
            val = rho + byte 
            val[2:]

            #taking val as input into shake-128 algorithm
        
            hash = hashlib.shake_128()
            hash.update((val).encode('utf-8'))
            var = hash.hexdigest(768)
        
            c = BitArray(hex = var)
            c  = c.bin

            #splitting c variable into bytes format(8 bits)
        
            m = 8
            byte = [c[i:i+n] for i in range(0 , len(c) , m)]

            #splitting byte variable into 3 chunks
        
            def split(list_a , chunk_size):
                for i in range(0 , len(list_a) , chunk_size):
                    yield list_a[i:i+chunk_size]
            chunk_size = 3
            value = list(split(byte , chunk_size))


            # process to find out the aij values

            #2^16 b2` + 2^8 b1 + b0 for every integer
        
        
            ak=[]
            ak1 = []
            ak2 =[]
        
            count = 0
            for m in range(0 , len(value)):

            #2^16*b2 in 23 bit format:

                def first_term(b_sec_index , b='01111111'):
                    b_sec_index = int(b_sec_index,2)
                    b = int(b,2)
                    res = b_sec_index & b
                    res = int(res)
                    res = res <<16
                    res = format(res ,'023b')
                    return res
                a = value[m][2]
                b='01111111'
                result = first_term(a)
                #print(result)

                #2^8*b1 in 23 bit format:
        
                def sec_term(b_first_index , b1='01111111'):
                    b_first_index = int(b_first_index , 2)
                    b_first_index = b_first_index <<8 
                    b_first_index = format(b_first_index , '023b')
                    return b_first_index
                c = value[m][1]
                result1 = sec_term(c)
                #print(result1)

                #b0 in 23 bit format:
        
                def third_term(b_zero_index , b2='01111111'):
                    b_zero_index = int(b_zero_index , 2)
                    b_zero_index = format(b_zero_index , '023b')
                    return b_zero_index 
                d = value[m][0]
                result2 = third_term(d)
                #print(result2)
            


                #to form the aij = 2^16 b2` + 2^8 b1 + b0

            
            
                aij= int(result) + int(result1) + int(result2)
                ak.append("{}".format(aij))
        
            #print(ak)
        
        
            for l in range(0 , len(ak)):
                ak1.append(int(ak[l] ,2))
                 #print(ak1)

        # condition statement whether the integers is in the limit of (2**23-1) if it is not then print(count)
        
            for z in range(0,len(ak1)):    
                if (ak1[z] < (2**23-1)):
                    ak2.append(ak1[z])
                    #print(ak2[0])
                else:
                    count = count + 1
                    print(count)
            
            
            #print(ak2)
            #print("----------------***********------------------")

            
            ak3.append(ak2)   
    #print(ak3)
    

    if(version==2):
        mat = np.array([ak3[0:4] , ak3[4:8] , ak3[8:12] ,ak3[12:16]]) 
        
    elif(version==3):
        mat = np.array([ak3[0:5] , ak3[5:10] , ak3[10:15] , ak3[15:20] , ak3[20:25] , ak3[25:30]])
        
    elif(version==5):
        mat = np.array([ak3[0:7] , ak3[7:14] , ak3[14:21] , ak3[21:28] ,ak3[28:35] ,ak3[35:42] , ak3[42:49] , ak3[49:56]])
        
    return mat
    
   




result = matrix_A(rho ,5)
print(len(result))
print(result)


# # secret key generation (s1 , s2)

# In[6]:


def sec_key_parts(rho_dash , eta , l , k ):
    
    entries = l+k
    list =[]
    list2=[]
    list3=[]
    count = 0
    count1=0
    
    for i in range(1 ,entries+1 ):
        temp = i
        bin = format(temp , '08b')
    
        n = 4
        byte = [bin[i:i+n] for i in range(0,len(bin) , n)]
        #print(byte)
    
        #little endian format of byte ()
    
        byte[0] , byte[1] = byte[1] , byte[0]
        byte = byte[0] + byte[1]
        
        #rho||byte [rho||16bitsoflitend(I)]
    
        value = rho_dash+byte
        value = value[2:]
        
    
        # hashing the value using SHAKE-256 algorithm to generate 256*8 bits for a row(for 8 rows)
    
        hash = hashlib.shake_256()
        hash.update((value).encode('utf-8'))
        var = hash.hexdigest(128)
        #print(var)
        #print(len(var))

    
        c = BitArray(hex = var)
        c  = c.bin
        
        #print("1024 bits creation :" , c)
        
    
        #list of 8 - 256 4 bits each index 
    
    
        m = 4
        byte = [c[i:i+m] for i in range(0 , len(c) , m)]
        #print("byte:" , byte)
        list.append(byte)
        
    for x in range(len(list)):
        for y in range(len(list[x])):
            integer = int(list[x][y] , 2)
            list2.append(integer)
            
    
    if eta==2:
        limit = 5
        for z in range(len(list2)):
            if (list2[z] <= 15):
                    trans = eta - list2[z]%5
                    list3.append(trans)
            else:
                count = count+1
                print(count)
                
    elif (eta==4):
        for c in range(len(list2)):
            if(list2[c] <=15):
                trans1 = eta - list2[c]%5
                list3.append(trans1)
            else:
                count=count+1
                print(count)
    
    
    chunk_size = 256
    list_chunked = [list3[i:i + chunk_size] for i in range(0, len(list3), chunk_size)]
    

    matrix = np.array([list_chunked[0:4] , list_chunked[4:8]])
    
    S1 = matrix[0]
    S2 = matrix[1]
    
    
    return matrix
                
    
            
sec_parts =sec_key_parts(rho_dash , 2 , 6, 5)
print(len(sec_parts))
#print(sec_parts)

S1 = sec_parts[0]

S2 = sec_parts[1]
    
print(S1)  

print(S2)
    


# In[ ]:





# In[ ]:




