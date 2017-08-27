#!/usr/bin/python3
import io
import tokenize

class Program:
  def __init__(self,fptr):
     self.ptr=fptr
     self.array=[]
     self.string=self.tokens()
     # self.compound becomes a tree which will be executed during evaluation of the programme
     self.compound=cmpdstat(self.string,self.array)
  def tokens(self):
    #Tokenizing every line or rather parsing 
    lines=self.ptr.readlines()
    stream=[]
    for i in range(len(lines)):
      new=io.StringIO(lines[i]).readline
      for token in tokenize.generate_tokens(new):
        if token.string!="  " and token.string!="\n" and token.string!=" " and token.string!='' and token.string!="\t":
          stream.append(token.string)
    return stream
  def evaluate(self):
    self.compound.evaluate()
class cmpdstat:
  def __init__(self,stream,array):
    self.array=array
    #print(stream)
    # check for while/if else/or ususal statement
    if len(stream)!=0:
      if stream[0]=='while':
        #print("Ene")
        #final will help to find the corresponding ending indicator for while/if else
        pos=final.find("while","done",stream)
        #print("POs",pos)
        self.array.append(Loop(stream[:pos]))
        cmpdstat(stream[pos+2:],self.array)
      elif stream[0]=="if":
        pos=final.find("if","fi",stream)
        j=0
        if "else" in stream[0:pos]:
          flag=ctr2=0
          while(1):
            if stream[j]=="else":
              if flag==1:
                break
              j=j+1
            elif stream[j]=="if":
              flag=(flag+1)
              ctr2=ctr2+1
              if ctr2==0:
                break
              j=j+1
            elif stream[j]=="fi":
              flag=flag-1
              j=j+1
            else:
              j=j+1
              if j>pos:
                break
        self.array.append(ifstat(stream[:pos],j))
        cmpdstat(stream[pos+2:],self.array) 
      elif ";" in stream:
        pos=stream.index(";")
        self.array.append(Statement.build(stream[:pos])) 
        #print(stream[pos+1:])
        cmpdstat(stream[pos+1:],self.array)
      else:
        #print("Entered in else")
        #print(stream)
        k=Statement.build(stream)
        #print("Falut",k)
        self.array.append(k)
  def evaluate(self):
    #print(self.array)
    for i in self.array:
      #print(len(self.array))
      i.evaluate()
class final:
  def find(string1,string2,stream):
    ctr=i=0
    while(1):
      if stream[i]==string2:
        ctr=ctr-1
        if ctr==0:
          break
        i=i+1
      elif stream[i]==string1:
          ctr=ctr+1
          if ctr==0:
            break
          i=i+1
      else:
          i=i+1
    return i  
# carries over the printing work of the language
class Print:
  def __init__(self,stream):
    self.array=stream
  def evaluate(self):
    if self.array[0][0]=='"':
      if len(self.array)!=1:
        print(self.array[0][1:len(self.array[0])-1],end=" ")
        Print(self.array[2:]).evaluate()
      else:
        print(self.array[0][1:len(self.array[0])-1])
    else:
      if "," in self.array:
        pos=self.array.index(",")
        print(Expr(self.array[:pos]).evaluate(),end=" ")
        Print(self.array[pos+1:]).evaluate()
      else:
        print(Expr(self.array).evaluate())
# classifies the statements and passes them to appropriate class
class Statement:
  def build(stream):
    #print("In statement",stream)
    if stream[0]=="print":
      return Print(stream[1:])
    if "=" in stream:
      #print("Going to Assignment")
      pos=stream.index("=")
      if len(stream[:pos])==1:
        return Assign(stream)
      else:
        return swap(stream)
# Handling the looping part in language design
class Loop:
  def __init__(self,stream):
    pos=stream.index("do")
    self.array=[]
    #print(stream[pos+1:])
    #print(stream[1:pos])
    self.structure=cmpdstat(stream[pos+1:],self.array)
    self.condition=Expr(stream[1:pos])
  def evaluate(self):
    #print(self.condition.evaluate())
    while self.condition.evaluate():
      #print(state)
      for i in self.structure.array:
        i.evaluate()
# Handles Condidional part in language design.
class ifstat:
  def __init__(self,stream,j):
    self.array1=[]
    self.array2=[]
    pos=stream.index("then")
    if j==0 or j>len(stream):
      self.present=False
      self.ifcond=Expr(stream[1:pos])
      self.ifbody=cmpdstat(stream[pos+1:],self.array1)
    else:
      self.present=True
      self.ifcond=Expr(stream[1:pos])
      self.ifbody=cmpdstat(stream[pos+1:j],self.array1)
      self.elsebody=cmpdstat(stream[j+1:],self.array2)
  def evaluate(self):
    if not self.present:
      #print("only one")
      if self.ifcond.evaluate():
        for i in self.ifbody.array:
          i.evaluate()
    else:
      #print("Had both")
      if self.ifcond.evaluate():
        for i in self.ifbody.array:
          i.evaluate()
      else:
        for i in self.elsebody.array:
          i.evaluate()
# Allows the language for assigning values to variables      
class Assign:
  def __init__(self,stream):
    pos=stream.index("=")
    self.lexp=stream[0].strip()
    self.rexp=Expr(stream[pos+1:])
  def evaluate(self):
    #print("Enteres")
    state[self.lexp]=self.rexp.evaluate()
    #print(state[self.lexp])
# Added feature of swapping as that of python
class swap:
  def __init__(self,stream):
    self.first=stream[0]
    self.second=stream[2]
  def evaluate(self):
    state[self.first],state[self.second]=state[self.second],state[self.first]
# allows us to define varaibles
class var:
  def __init__(self,stream):
    self.variable=stream.strip()
  def evaluate(self):
    if self.variable in state:
      return state[self.variable]
    else:
      raise NameError("name",self.variable,"isn't defined yet")
# Functionality for taking inputs for the user
class Taker:
  def __init__(self,stream):
    pos=stream.index("fromterminal")
    if stream[len(stream)-1]==":":
      self.value=None
    else:
      self.value=(stream[pos+2][1:len(stream[pos+2])-1])
  def evaluate(self):
    if self.value==None:
      return int(input())
    return int(input(self.value))
# helps us in using constant
class const:
  def __init__(self,stream):
    self.constant=eval(stream)
  def evaluate(self):
    return self.constant
# Handling Expressions and passing them to corresponding classes thereby creating a tree
class Expr:
  def __init__(self,stream):
    #print(stream)
    if "+" in stream:
      self.type=PlusExp(stream)
    elif "-" in stream:
      self.type=MinusExp(stream)
    elif "*" in stream:
      self.type=MulExp(stream)
    elif "/" in stream:
      self.type=DivExp(stream)
    elif "<=" in stream:
      self.type=CondLE(stream)
    elif ">=" in stream:
      self.type=CondGE(stream)
    elif "<" in stream:
      self.type=CondL(stream)
    elif ">" in stream:
      self.type=CondG(stream)
    elif "fromterminal" in stream:
      self.type=Taker(stream)
    elif stream[0].isdigit():
      self.type=const(stream[0])
    else:
      self.type=var(stream[0])
  def evaluate(self):
    return self.type.evaluate()      
class PlusExp:
  def __init__(self,stream):
    pos=stream.index("+")
    self.lexp=Expr(stream[:pos])
    self.rexp=Expr(stream[pos+1:])
  def evaluate(self):
    return self.lexp.evaluate()+self.rexp.evaluate()
class MinusExp:
  def __init__(self,stream):
    pos=stream.index("-")
    self.lexp=Expr(stream[:pos])
    self.rexp=Expr(stream[pos+1:])
  def evaluate(self):
    return self.lexp.evaluate()-self.rexp.evaluate()
class MulExp:
  def __init__(self,stream):
    pos=stream.index("*")
    self.lexp=Expr(stream[:pos])
    self.rexp=Expr(stream[pos+1:])
  def evaluate(self):
    return self.lexp.evaluate()*self.rexp.evaluate()
class DivExp:
  def __init__(self,stream):
    pos=stream.index("/")
    self.lexp=Expr(stream[:pos])
    self.rexp=Expr(stream[pos+1:])
  def evaluate(self):
    if self.rexp.evaluate()==0:
      raise ZeroDivisionError("division by zero is being done")
    return self.lexp.evaluate()/self.rexp.evaluate()
class CondLE:
  def __init__(self,stream):
    pos=stream.index("<=")
    self.lexp=Expr(stream[:pos])
    self.rexp=Expr(stream[pos+1:])
  def evaluate(self):
    return self.lexp.evaluate()<=self.rexp.evaluate()
class CondGE:
  def __init__(self,stream):
    pos=stream.index(">=")
    self.lexp=Expr(stream[:pos])
    self.rexp=Expr(stream[pos+1:])
  def evaluate(self):
    return self.lexp.evaluate()>=self.rexp.evaluate()
class CondL:
  def __init__(self,stream):
    pos=stream.index("<")
    self.lexp=Expr(stream[:pos])
    self.rexp=Expr(stream[pos+1:])
  def evaluate(self):
    return self.lexp.evaluate()<self.rexp.evaluate()
class CondG:
  def __init__(self,stream):
    pos=stream.index(">")
    self.lexp=Expr(stream[:pos])
    self.rexp=Expr(stream[pos+1:])
  def evaluate(self):
    return self.lexp.evaluate()>self.rexp.evaluate()
#print("Bilal")
fptr=open("test.txt","r+")
# Program compilation happens here... any errors(though not handled..currently) will be popped in terminal..
p=Program(fptr)
state=dict={}
#execution of programm happens here.
p.evaluate()
#print(state,"finally")

