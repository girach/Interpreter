#!/usr/bin/python3
import io
import tokenize
class Programme:
  def __init__(self,fptr):
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
    print(stream)
    Compound(stream,self.store)
class Compound:
  def __init__(self,stream,store):
    self.breaking(stream,store)
  def breaking(self,stream,store):
    if len(stream)!=0:
      print("Got this string to break",stream)
      if stream[0]=="while":
        ctr=i=0
        while(1):
          if stream[i]=="done":
            print(stream[i],i)
            ctr=ctr-1
            if ctr==0:
              break
            i=i+1
          elif stream[i]=="while":
            print(stream[i],i)
            ctr=ctr+1
            if ctr==0:
              break
            i=i+1
          else:
            i=i+1
        Loop(stream[0:i],store)
        self.breaking(stream[i+2:],store)
      elif stream[0]=="if":
        ctr1=ctr2=i=j=0
        flag=0
        while(1):
          if stream[i]=="fi":
            print(stream[i],i)
            ctr1=ctr1-1
            flag=(flag+1)%2
            if ctr1==0:
              break
            i=i+1
          elif stream[i]=="if":
            print(stream[i],i)
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
              print(stream[j],j)
              if flag==1:
                break
              j=j+1
            elif stream[j]=="if":
              flag=(flag+1)
              print(stream[j],j)
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
        print("Before life was like this:",stream)
        ifstat(stream[0:i],store,j)
        print(stream)
        self.breaking(stream[i+2:],store)
      elif ";" in stream:
        pos=stream.index(";")
        Statement(stream[:pos],store)  #haven't used still
        self.breaking(stream[pos+1:],store)
      else:
        print("It goes here")
        Statement(stream,store)
class Expression:
  def is_number(self,s):
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
  def evaluateexp(self,stream,store):
    print("In exp",store)
    print(stream)
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
      print(stream[pos+1:i])
      b=[]
      b.append(str(self.evaluateexp(stream[pos+1:i],store)))
      stream=stream[:pos]+b+stream[i+1:]
      #print("after:",stream)
      self.evaluateexp(stream,store)
    if "+" in stream:
      first=PlusExp()
      return first.evaluateP(stream,store)
    if "-" in stream:
      first=MinusExp()
      return first.evaluateM(stream,store)
    if "*" in stream:
      first=MultiExp()
      return first.evaluateMUL(stream,store)
    if "/" in stream:
      first=DivExp()
      return first.evaluateD(stream,store)
    if "%" in stream:
      first=ModExp()
      return first.evaluateMOD(stream,store)
    if "<=" in stream:
      first=CondLE()
      print("Enterd")
      return first.evaluateLE(stream,store)
    if ">=" in stream:
      print("Enterd")
      first=CondGE()
      return first.evaluateGE(stream,store)
    if "<" in stream:
      first=CondL()
      print("Enterd")
      return first.evaluateL(stream,store)
    if ">" in stream:
      print("Enterd")
      first=CondG()
      return first.evaluateG(stream,store)
    if "==" in stream:
      print("Enterd")
      first=CondE()
      return first.evaluateE(stream,store)
    if "!=" in stream:
      print("Enterd")
      first=CondNE()
      return first.evaluateNE(stream,store)
    if "fromterminal" in stream:
      pos=stream.index("fromterminal")
      if stream[len(stream)-1]==":":
        return int(input())
      else:
        return int(input(stream[pos+2][1:len(stream[pos+2])-1]))
    else:
      if self.is_number(stream[0]):
        print("yu")
        return eval(stream[0])
      else:
        if not stream[0] in store:
          raise ValueError('The value',stream[0],'is non existing')
        return store[stream[0]]
class Loop(Compound,Expression):
  def __init__(self,stream,store):
    self.evaluate(stream,store)
  def evaluate(self,stream,store):
    pos=stream.index("do")
    while self.evaluateexp(stream[2:pos-1],store):
      self.breaking(stream[pos+1:len(stream)],store)
class ifstat(Compound,Expression):
  def __init__(self,stream,store,j):
    self.evaluate(stream,store,j)
  def evaluate(self,stream,store,j):
    print("This came in if class",stream)
    print("Main part",j,stream[j:])
    pos=stream.index("then")
    if j==0 or j>len(stream):
      if self.evaluateexp(stream[2:pos-1],store):
        print("firstfirst")
        self.breaking(stream[pos+1:len(stream)],store)
    else:
      if self.evaluateexp(stream[2:pos-1],store):
        print("secondfirst")
        self.breaking(stream[pos+1:j],store)
        print("done") 
      else:
        print("secondsecond")
        self.breaking(stream[j+1:len(stream)],store)
        print("over")
class Assignment(Expression):
  def __init__(self,stream,store):
    self.evaluate(stream,store)
  def evaluate(self,stream,store):
    pos=stream.index("=")
    print("before =",store)
    store.setdefault(stream[0],"None")
    print("after=",store)
    k=self.evaluateexp(stream[pos+1:],store)
    print("Atlst",k)
    store[stream[0]]=k
    print(store)
class printing(Expression):
  def __init__(self,stream,store):
    self.evaluate(stream,store)
  def evaluateprint(self,stream,store):
    print("Entered for printing",stream)
    if stream[0][0]=='"':
      if len(stream)!=1:
        print("Main program printing:",stream[0][1:len(stream[0])-1],end=" ")
        self.evaluateprint(stream[2:],store)
      else:
        print("Main program printing:",stream[0][1:len(stream[0])-1])
    else:
      if "," in stream:
        pos=stream.index(",")
        k=self.evaluateexp(stream[:pos],store)
        print("Main program printing:",k,end=" ")
        self.evaluateprint(stream[pos+1:],store)
      else:
        print("Here bitch")
        k=self.evaluateexp(stream,store)
        print("Main program printing:",k)
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
class Statement(printing):
  def __init__(self,stream,store):
    print(stream)
    self.evaluate(stream,store)
  def evaluate(self,stream,store):
    if "=" in stream:
      first=Assignment(stream,store)
      print(store)
    elif "print" in stream:
      self.evaluateprint(stream[1:],store)
class CondLE(Expression):
  def evaluateLE(self,stream,store):
    pos=stream.index("<=")
    return self.evaluateexp(stream[:pos],store)<=self.evaluateexp(stream[pos+1:],store)
class CondGE(Expression):
  def evaluateGE(self,stream,store):
    pos=stream.index(">=")
    return self.evaluateexp(stream[:pos],store)>=self.evaluateexp(stream[pos+1:],store)
class CondE(Expression):
  def evaluateE(self,stream,store):
    pos=stream.index("==")
    return self.evaluateexp(stream[:pos],store)==self.evaluateexp(stream[pos+1:],store)
class CondL(Expression):
  def evaluateL(self,stream,store):
    pos=stream.index("<")
    return self.evaluateexp(stream[:pos],store)<self.evaluateexp(stream[pos+1:],store)
class CondG(Expression):
  def evaluateG(self,stream,store):
    pos=stream.index(">")
    return self.evaluateexp(stream[:pos],store)>self.evaluateexp(stream[pos+1:],store)
class CondNE(Expression):
  def evaluateNE(self,stream,store):
    pos=stream.index("!=")
    return self.evaluateexp(stream[:pos],store)!=self.evaluateexp(stream[pos+1:],store)
class PlusExp(Expression):
  def evaluateP(self,stream,store):
    pos=stream.index("+")
    k=self.evaluateexp(stream[:pos],store)+self.evaluateexp(stream[pos+1:],store)
    print(k)
    return k
class MinusExp(Expression):
  def evaluateM(self,stream,store):
    pos=stream.index("-")
    k=self.evaluateexp(stream[:pos],store)-self.evaluateexp(stream[pos+1:],store)
    print(k)
    return k
class MultiExp(Expression):
  def evaluateMUL(self,stream,store):
    pos=stream.index("*")
    k=self.evaluateexp(stream[:pos],store)*self.evaluateexp(stream[pos+1:],store)
    print(k)
    return k
class DivExp(Expression):
  def evaluateD(self,stream,store):
    pos=stream.index("/")
    k=self.evaluateexp(stream[:pos],store)/self.evaluateexp(stream[pos+1:],store)
    print(k)
    return k
class ModExp(Expression):
  def evaluateMOD(self,stream,store):
    pos=stream.index("%")
    k=self.evaluateexp(stream[:pos],store)%self.evaluateexp(stream[pos+1:],store)
    print(k)
    return k
f=open("check.txt","r")
Programme(f)
