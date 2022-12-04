class Data:
    priority = 0
    opcode = '          '
    PCReg = ''
    IRReg = ''
    regList = ['01', "02", '03', '04', '05', '06', '07', '08']
    memorylist = ['01', '02', '03', '04', '05', '06', '07', '08',
                  '09', '10', '11', '12', '13', '14', '15', '16']
    highlighter = ['x','x','x','x','x','x']
  
  
    hexList = [str(i) for i in range(10)]
    for i in range(65,71):
        hexList.append(chr(i))

    def HextoDec(self, data):
        return int(data, base=16)

    def DectoHex(self, data, bit):
        #bit 0 : 8 bit
        #bit 1 : 16 bit
        data = self.HextoDec(data)
        data = hex(data)
        x=''
  
        for i in range(2,len(data)):
            x+=data[i]
        data = x.upper()
        
        if(bit == 0 and len(data)<2):
            return '0'+ data
        elif (bit == 1 and len(data)<4):
            for i in range(4-len(data)):
                data = '0'+data
            return data
        
       

    def XRegs(self, xreg, data='xxxx'):
        hdata = data[0]+data[1]
        ldata = data[2]+data[3]
        
        if(xreg == 'AX'):
            return [hdata,ldata, 0,4]
        if(xreg == 'BX'):
            return [hdata,ldata, 1,5]
        if(xreg == 'CX'):
            return [hdata,ldata, 2,6]
        if(xreg == 'DX'):
            return [hdata,ldata, 3,7]

    def swork(self, s):
        if(s[0] != '[' or s[-1] != ']'):
            return "Syntax Error"
        s = s.replace('[','')
        s = s.replace(']','')
        return s

class Instruction:
    string = ""
    PrevObj = Data()
    Obj = Data()

    XRegsList = ['AX','BX','CX','DX']
    InstructionList = ["MOV", "ADD", "SUB", "INC", "DEC","MUL", "DIV", "OR"]
    RegList = ["AH", "BH", "CH", "DH", "AL",
               "BL", "CL", "DL"]
    MemList = ["00000","00001", "00002", "00003", "00004", "00005", "00006", "00007",
               "00008", "00009", "0000A", "0000B", "0000C", "0000D", "0000E", "0000F"]

    def _init_(self, string, prev_Obj):
        self.string = string
        if (prev_Obj.priority >= 3):
            prev_Obj.priority = 0
        self.PrevObj = prev_Obj
        self.Obj = self.PrevObj
        pass

    def split_string(self):

        error = "invalid"
        string = self.string
        Strlist = string.split(" ", 1)
        if (len(Strlist) != 2):
            return error

        regList = Strlist[1].split(",")
        inst = Strlist[0]
        opr1 = regList[0].replace(' ', '')
        opr2 = 0

        if ("" in regList and string.find(",") != -1):
            return error

        if (len(regList) > 1):
            if (string.find(",") == -1):
                return error
            else:
                opr2 = regList[1].replace(' ', '')

        if (opr2 != 0):
            return ([inst, opr1, opr2])
        else:
            return ([inst, opr1])

    def working(self, insList):
        errorType1 = "Invalid Instruction"
        errorType2 = "Invalid Operand"
        inst = ''
        opr1 = ''
        opr2 = ''
        if (len(insList) == 3):
            inst = insList[0].upper()
            opr1 = insList[1].upper()
            opr2 = insList[2].upper()
        elif (len(insList) == 2):
            inst = insList[0].upper()
            opr1 = insList[1].upper()

        if (inst.upper() not in self.InstructionList):
            return errorType1
   
    #Instruction Set

        if (inst.upper() == "MOV"):
            a = self.mov(opr1, opr2)
            if (type(a) == str):
                return a

        if (inst.upper() == "INC" or inst.upper() == "DEC"):
            a = self.incDec(opr1, inst)
            if (type(a) == str):
                return a

        if (inst.upper() == "ADD" or inst.upper()=="SUB"):
            a = self.addSub(inst, opr1, opr2)
            if (type(a) == str):
               return a

        if (inst.upper() == "MUL"):
            self.mul(opr1)
       
        if (inst.upper() == "DIV"):
            self.div(opr1)
       
        if (inst.upper() == "OR"):
            self.orF(opr1, opr2)
        return self.Obj