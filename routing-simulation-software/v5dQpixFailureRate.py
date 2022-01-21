#!/usr/bin/python3

#from QpixSimplifiedAsic import *
import random
import math
import sys
import numpy

# This is a single trial array

# Seed the RNG
random.seed()

# Debug status
debugLevel = 1 #5 - debug
debugLevel = -2
debugLevel = 0

# Create an array of QPixAsics
nRows = 6
nCols = 6
#nPixs = 16

# Fail rate per ASIC and conncetion
randomFailRatePerASIC = 0.01
randomFailRatePerConn = 0.005


# How many steps in sim
EndStep = nRows*nCols+1

#MC count
CounterMC = 100

class QPixSimplifiedAsic:
  def __init__(self , connUP=True, connDown=True, connLeft=True, connRight=True, row = None, col = None, isReadout = False, isWorking = True, hasData = False):
    #self.connections    = [None] * 4
    #self.connOuts     = [0,0,0,0] #[Left, Right, Up, Down]
    self.connUP         = connUP
    self.connDown       = connDown
    self.connLeft       = connLeft
    self.connRight      = connRight
    #self.randomRate     = randomRate
    #self.stepCount      = stepCount
    self.row            = row
    self.col            = col
    self.isReadout      = isReadout
    self.isWorking      = isWorking
    self.hasData        = hasData
def init_matrix(asicMatrix):
  outScreen = ''
  for i in range(0,nRows):
    outScreen += '\n'
    outScreen2= ''  
    for j in range(0,nCols):
      # create initial connections
      isReadout = False
      r=1
      l=1
      u=1
      d=1
      if(j==0):
        l=0
      elif(j==nCols-1):
        r=0
      else:
        u=0
        d=0
      if(i==0): u=0
      if(i==nRows-1): d=0
      #if(i%2==0): l=0
      #if(i%2==1): r=0
      if(j==nCols-1 and i==nRows-1):
          isReadout=True
      if(j==0 and i==0):
          isReadout=True
      if (r==1): outScreen=outScreen+'r'
      if (l==1): outScreen=outScreen+'l'
      if (u==1): outScreen=outScreen+'u'
      if (d==1): outScreen=outScreen+'d'
      outScreen = outScreen+'\t'
      if(isReadout==True): outScreen2=outScreen2+'1\t'
      else: outScreen2+='0\t'     
      # Create an ASIC at this position
      #print(i,j, '    :     ',u,d,l,r)
      asicMatrix[i][j] = QPixSimplifiedAsic(bool(u), bool(d), bool(l), bool(r), row = i, col = j, isReadout = isReadout , isWorking = True, hasData = False)
  if(debugLevel==-2): print(outScreen)

def comp_fail(asicMatrix):
  # break some connections and asics
  outScreen = ''
  outScreen2= ''
  compfailcount = [0,0]
  for i in range(0,nRows):
    outScreen+='\n'
    outScreen2+='\n'  
    for j in range(0,nCols):
      if(random.uniform(0,1)<randomFailRatePerASIC):
        asicMatrix[i][j].isWorking = False
        compfailcount[0]+=1
      if(random.uniform(0,1)<randomFailRatePerConn):
        asicMatrix[i][j].connUP = False
        compfailcount[1]+=1
      if(random.uniform(0,1)<randomFailRatePerConn):
        asicMatrix[i][j].connDown = False
        compfailcount[1]+=1
      if(random.uniform(0,1)<randomFailRatePerConn):
        asicMatrix[i][j].connLeft = False 
        compfailcount[1]+=1
      if(random.uniform(0,1)<randomFailRatePerConn):
        asicMatrix[i][j].connRight = False
        compfailcount[1]+=1                     
      if (asicMatrix[i][j].connRight==True): outScreen=outScreen+'r'  
      if (asicMatrix[i][j].connLeft==True): outScreen=outScreen+'l'       
      if (asicMatrix[i][j].connUP==True): outScreen=outScreen+'u'       
      if (asicMatrix[i][j].connDown==True): outScreen=outScreen+'d'
      outScreen = outScreen+'\t'
      if(asicMatrix[i][j].isWorking==True): outScreen2=outScreen2+'1\t'
      else: outScreen2+='0\t' 
  if(debugLevel>0):
    print(outScreen)
    print(outScreen2)
  return compfailcount


def transmit_sim(asicMatrix,hit_row,hit_col):
  if(debugLevel>0):print('\n'+str(hit_row)+'\t'+str(hit_col))
  asicMatrix[hit_row][hit_col].hasData = True
  data_next_step = numpy.zeros((nRows,nCols), dtype=int)
  data_next_step[hit_row][hit_col]=1
  for t in range(0,EndStep):
    outScreen2=''
    change_checker=0
    for i in range(0,nRows):
      outScreen2= outScreen2+'\n'  
      for j in range(0,nCols):
        if(asicMatrix[i][j].isWorking==True and asicMatrix[i][j].isReadout==True and asicMatrix[i][j].hasData==True):
          if(debugLevel>0): print(outScreen2)
          return t+1
        #outScreen = outScreen+'\t'
        if(asicMatrix[i][j].hasData==True and asicMatrix[i][j].isWorking == True): 
          if (asicMatrix[i][j].connRight==True): 
            data_next_step[i][j+1]=1 
            change_checker=1
          if (asicMatrix[i][j].connLeft==True): 
            data_next_step[i][j-1]=1      
            change_checker=1
          if (asicMatrix[i][j].connUP==True): 
            data_next_step[i-1][j]=1       
            change_checker=1
          if (asicMatrix[i][j].connDown==True): 
            data_next_step[i+1][j]=1  
            change_checker=1
          outScreen2=outScreen2+'1\t'
        else: outScreen2+='0\t'    
    if (change_checker==0):
      if(debugLevel>0): print(outScreen2)
      return 0   
    if(t==0 and debugLevel>0): print(outScreen2)
    for i in range(0,nRows): 
      for j in range(0,nCols):
        if(asicMatrix[i][j].isWorking==True):
          asicMatrix[i][j].hasData=bool(data_next_step[i][j])
  if(debugLevel>0): print(outScreen2)
  return -1



#Run MC over MC_sample_count

#Initiate one random hit placement
#hit_row = random.randrange(0,nRows)
#hit_col = random.randrange(0,nCols)

  # break some connections and asics
outScreen = ''
f2 = open('collectionTime.txt','w')
f2str = ('i'+'\t'+'j'+'\t'+'ASICfailCount'+'\t'+'ConnFailCount'+'\t'+'TransmissionStepCount'+'\n')
f2.write(f2str)
f2.close()
success_transmit_rate = numpy.zeros((nRows,nCols), dtype=float)
effective_ASIC_failure_rate = 0.0
for i in range(0,nRows):
  outScreen+='\n'
  for j in range(0,nCols):
    success_transmit = 0.0
    f2 = open('collectionTime.txt','a')
    for c in range(0,CounterMC):
      # Create the array and populate all positions
      asicMatrix = [[QPixSimplifiedAsic() for i in range(nCols)] for j in range(nRows)] 
      init_matrix(asicMatrix)
      compfailcount = comp_fail(asicMatrix)
      transmit = transmit_sim(asicMatrix,i,j)
      if(debugLevel>=1):
        print(transmit)
      if (transmit>0):
        success_transmit += 1
      f2str = (str(i)+'\t'+str(j)+'\t'+str(compfailcount[0])+'\t'+str(compfailcount[1])+'\t'+str(transmit)+'\n')
      f2.write(f2str)
    success_transmit_rate[i][j] = success_transmit*1.0 / CounterMC
    effective_ASIC_failure_rate += success_transmit_rate[i][j]
    outScreen = outScreen+str(success_transmit_rate[i][j])+'\t'
    print(i,j)
    f2.close()
print(outScreen)
effective_ASIC_failure_rate = 1.0 - (effective_ASIC_failure_rate / (nRows*nCols*1.0))

f = open('v5dout.txt','a')
f.write('\n')
f.write("\nMC sample count =\t" + str(CounterMC))
f.write('\nnumber of Rows =\t'+str(nRows))
f.write('\nnumber of Columns =\t'+str(nCols))
f.write('\nIndividual effective ASIC failure rate =\t'+str(randomFailRatePerASIC))
f.write('\nIndividual data connection failure rate =\t'+str(randomFailRatePerConn))
f.write('\n\n'+'effective ASIC failure rate = '+str(effective_ASIC_failure_rate))
f.write('\n')
f.close()

print('\n')
print('MC sample count =\t' + str(CounterMC))
print('number of Rows =\t'+str(nRows))
print('number of Columns =\t'+str(nCols))
print('Individual effective ASIC failure rate =\t'+str(randomFailRatePerASIC))
print('Individual data connection failure rate =\t'+str(randomFailRatePerConn))
print('\n'+'effective ASIC failure rate = '+str(effective_ASIC_failure_rate))
print('\n')

""" print("MAX QUEUE DEPTHS")
# Check the current queue depths
for i in range(0,nRows):
  for j in range(0,nCols):
    print(str(i)+" "+str(j)+" "+str(asicMatrix[i][j].maxDepth)+" ",end='')
    for d in range(0,4):
      print(str(asicMatrix[i][j].maxConnDepths[d])+" ",end='')
    print()

print("PROCESSING TIMES")
for i in range(0,len(eventTimes)):
  print(str(eventTimes[i]))

print("HITS PER EVENT")
for i in range(0,len(hitsPerEvent)):
  print(str(hitsPerEvent[i])) """
