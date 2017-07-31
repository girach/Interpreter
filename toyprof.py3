#!/usr/bin/python3
import io
import tokenize
class Programme:           #scanning may not be that perfect needed to have some look at different cases
  def __init__(self,fptr):  #instead of creating objects,use inheritance
    self.ptr=fptr
    dict={}
    self.store=dict
    self.tokens(fptr)
  def tokens(self,fptr):
    lines=f.readlines()
    stream=[]
    for i in range(len(lines)):
      new=io.StringIO(lines[i]).readline
      #print(new)
      for token in tokenize.generate_tokens(new):
      #print(token.string)
        if token.string!="  " and token.string!="\n" and token.string!=" " and token.string!='' and token.string!="\t":
          stream.append(token.string)
    #print(stream)
    first=Compound()
    first.breaking(stream,self.store)
class Compound:
  def breaking(self,stream,store):
    if len(stream)!=0:
      #print("Got this string to break",stream)
      if stream[0]=="while":
        ctr=i=0
        while(1):
          if stream[i]=="done":
            #print(stream[i],i)
            ctr=ctr-1
            if ctr==0:
              break
            i=i+1
          elif stream[i]=="while":
            #print(stream[i],i)
            ctr=ctr+1
            if ctr==0:
              break
            i=i+1
          else:
            i=i+1
        first=Loop(stream[0:i],store)
        first=Compound()
        first.breaking(stream[i+2:],store)
      elif stream[0]=="if":
        ctr1=ctr2=i=j=0
        flag=0
        while(1):
          if stream[i]=="fi":
            #print(stream[i],i)
            ctr1=ctr1-1
            flag=(flag+1)%2
            if ctr1==0:
              break
            i=i+1
          elif stream[i]=="if":
            #print(stream[i],i)
            ctr1=ctr1+1
            flag=(flag+1)%2
            if ctr1==0:
              break
            i=i+1
          else:
            i=i+1
        if "else" in stream[0:i]:
          flag=0
          while(1):
            if stream[j]=="else":
              #print(stream[j],j)
              if flag==1:
                break
              j=j+1
            elif stream[j]=="if":
              flag=(flag+1)
              #print(stream[j],j)
              ctr2=ctr2+1
              if ctr2==0:
                break
              j=j+1
            elif stream[j]=="fi":
              flag=flag-1
              j=j+1
            else:
              j=j+1
              if j>i:
                break
        #print("Before life was like this:",stream)
        second=ifstat(stream[0:i],store,j)
        first=Compound()
        #print(stream)
        first.breaking(stream[i+2:],store)
      elif ";" in stream:
        pos=stream.index(";")
        first=Statement(stream[:pos],store)
        first=Compound()  #haven't used still
        first.breaking(stream[pos+1:],store)
      else:
        #print("It goes here")
        Statement(stream,store)
class Loop:
  def __init__(self,stream,store):
    self.evaluate(stream,store)
  def evaluate(self,stream,store):
    pos=stream.index("do")
    exp=Expression()
    while exp.evaluate(stream[2:pos-1],store):
      first=Compound()
      first.breaking(stream[pos+1:len(stream)],store)
class ifstat:
  def __init__(self,stream,store,j):
    self.evaluate(stream,store,j)
  def evaluate(self,stream,store,j):
    pos=stream.index("then")
    exp=Expression()
    first=Compound()
    if j==0 or j>len(stream):
      if exp.evaluate(stream[2:pos-1],store):
        #print("firstfirst")
        first.breaking(stream[pos+1:len(stream)],store)
    else:
      if exp.evaluate(stream[2:pos-1],store):
        #print("secondfirst")
        first.breaking(stream[pos+1:j],store)
        #print("done") 
      else:
        #print("secondsecond")
        first.breaking(stream[j+1:len(stream)],store)
        #print("over")
      
class Statement:
  def __init__(self,stream,store):
    #print(stream)
    self.evaluate(stream,store)
  def evaluate(self,stream,store):
    if "=" in stream:
      first=Assignment(stream,store)
      #print(store)
    elif "print" in stream:
      first=printing(stream[1:],store)
class printing:
  def __init__(self,stream,store):
    self.evaluate(stream,store)
  def evaluate(self,stream,store):
    #print("Entered for printing",stream)
    if stream[0][0]=='"':
      if len(stream)!=1:
        print(stream[0][1:len(stream[0])-1],end=" ")
        first=printing(stream[2:],store)
      else:
        print(stream[0][1:len(stream[0])-1])
    else:
      if "," in stream:
        pos=stream.index(",")
        exp=Expression()
        k=exp.evaluate(stream[:pos],store)
        print(k,end=" ")
        first=printing(stream[pos+1:],store)
      else:
        exp=Expression()
        k=exp.evaluate(stream,store)
        print(k)
    '''else:
      #print(len(stream[0]))
      if not stream[0] in store:
        raise ValueError('The value which you want is non existing')
      if "," in stream:
        pos=stream.index(",")
        exp=Expression()
        k=exp.evaluate(stream[:pos],store)
        print("Main program printing:",k)
        first=printing(stream[pos+1:],store)'''
class Assignment:
  def __init__(self,stream,store):
    self.evaluate(stream,store)
  def evaluate(self,stream,store):
    pos=stream.index("=")
    #print("before =",store)
    store.setdefault(stream[0],"None")
    #print("after=",store)
    exp=Expression()
    k=exp.evaluate(stream[pos+1:],store)
    #print("Atlst",k)
    store[stream[0]]=k
    #print(store)
class Conditionallessthanequal:
  def evaluate(self,stream,store):
    pos=stream.index("<=")
    exp=Expression()
    return exp.evaluate(stream[:pos],store)<=exp.evaluate(stream[pos+1:],store)
class Conditionalgreaterthanequal:
  def evaluate(self,stream,store):
    pos=stream.index(">=")
    exp=Expression()
    return exp.evaluate(stream[:pos],store)>=exp.evaluate(stream[pos+1:],store)
class Conditionalequality:
  def evaluate(self,stream,store):
    pos=stream.index("==")
    exp=Expression()
    return exp.evaluate(stream[:pos],store)==exp.evaluate(stream[pos+1:],store)
class Conditionallessthan:
  def evaluate(self,stream,store):
    pos=stream.index("<")
    exp=Expression()
    return exp.evaluate(stream[:pos],store)<exp.evaluate(stream[pos+1:],store)
class Conditionalgreaterthan:
  def evaluate(self,stream,store):
    pos=stream.index(">")
    exp=Expression()
    return exp.evaluate(stream[:pos],store)>exp.evaluate(stream[pos+1:],store)
class Conditionalnegation:
  def evaluate(self,stream,store):
    pos=stream.index("!=")
    exp=Expression()
    return exp.evaluate(stream[:pos],store)!=exp.evaluate(stream[pos+1:],store)
class Expression:
  def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
  def evaluate(self,stream,store):
    #print("In exp",store)
    #print(stream)
    #print("Stream given:",stream)
    if "(" in stream:
      pos=stream.index("(")
      #print(pos)
      #print(stream)
      i=ctr=0
      while(1):
        if stream[i]=="(":
          ctr=ctr+1
          #print(ctr)
          i=i+1
        elif stream[i]==")":
          ctr=ctr-1
          #print(ctr)
          if ctr==0:
            break
          i=i+1
        else:
          i=i+1
      #print(stream[pos+1:i])
      exp=Expression()
      b=[]
      b.append(str(exp.evaluate(stream[pos+1:i],store)))
      stream=stream[:pos]+b+stream[i+1:]
      #print("after:",stream)
      exp.evaluate(stream,store)    
    if "+" in stream:
      first=PlusExp()
      return first.evaluate(stream,store)
    if "-" in stream:
      first=MinusExp()
      return first.evaluate(stream,store)
    if "*" in stream:
      first=MultiExp()
      return first.evaluate(stream,store)
    if "/" in stream:
      first=DivExp()
      return first.evaluate(stream,store)
    if "%" in stream:
      first=ModExp()
      return first.evaluate(stream,store)
    if "<=" in stream:
      first=Conditionallessthanequal()
      #print("Enterd")
      return first.evaluate(stream,store)
    if ">=" in stream:
      first=Conditionalgreaterthanequal()
      #print("Enterd")
      return first.evaluate(stream,store)
    if "<" in stream:
      first=Conditionallessthan()
      #print("Enterd")
      return first.evaluate(stream,store)
    if ">" in stream:
      first=Conditionalgreaterthan()
      #print("Enterd")
      return first.evaluate(stream,store)
    if "==" in stream:
      first=Conditionalequality()
      #print("Enterd")
      return first.evaluate(stream,store)
    if "!=" in stream:
      first=Conditionalnegation()
      #print("Enterd")
      return first.evaluate(stream,store)
    if "fromterminal" in stream:
      pos=stream.index("fromterminal")
      if stream[len(stream)-1]==":":
        return int(input())
      else:
        return int(input(stream[pos+2][1:len(stream[pos+2])-1]))
    else:
      exp=Expression
      if exp.is_number(stream[0]):
       #print("yu")
        return eval(stream[0])
      else:
        if not stream[0] in store:
          raise ValueError('The value',stream[0],'is non existing')
        return store[stream[0]]
class PlusExp:
  def evaluate(self,stream,store):
    pos=stream.index("+")
    first=Expression()
    k=first.evaluate(stream[:pos],store)+first.evaluate(stream[pos+1:],store)
    #print(k)
    return k
class MinusExp:
  def evaluate(self,stream,store):
    pos=stream.index("-")
    first=Expression()
    k=first.evaluate(stream[:pos],store)-first.evaluate(stream[pos+1:],store)
    #print(k)
    return k
class MultiExp:
  def evaluate(self,stream,store):
    pos=stream.index("*")
    first=Expression()
    k=first.evaluate(stream[:pos],store)*first.evaluate(stream[pos+1:],store)
    #print(k)
    return k
class DivExp:
  def evaluate(self,stream,store):
    pos=stream.index("/")
    first=Expression()
    k=first.evaluate(stream[:pos],store)/first.evaluate(stream[pos+1:],store)
    #print(k)
    return k
class ModExp:
  def evaluate(self,stream,store):
    pos=stream.index("%")
    first=Expression()
    k=first.evaluate(stream[:pos],store)%first.evaluate(stream[pos+1:],store)
    #print(k)
    return k
f=open("es.txt","r")
Programme(f)
