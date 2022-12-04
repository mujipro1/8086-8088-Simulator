from tkinter import *
import processing
import Priorqueue


class Microprocessor:
    root = Tk()
    color = "#1f2a2e"
    font = "Arial 12"
    current_ins = ''
    DataObj = ''
    stateObj = processing.Data()
    MemLabelText = ["00014", "00013", "00012", "00011"]
    myQ = Priorqueue.Queue()
    Mtemp1 = []
    Mtemp2 = []
    Rtemp1 = []
    Rtemp2 = []


    def _init_(self, Data):
        self.DataObj = Data

    def basic_screen(self):
        root = self.root
        root.state('zoomed')
        root.resizable(False, False)
        root.config(bg=self.color)
        root.title("8086 Simulator")

        def foc_root(event):
            event.widget.focus()
        root.bind("<Button>", foc_root)

        coloredFrame = Frame(root, height=40, width=1400, bg="#15abb0")
        coloredFrame.place(x=0, y=0, anchor="nw")

        nameLbl = Label(root, text="8086/8088 Simulator",
                        bg="#15abb0", fg="white",
                        font="Cambria 14 bold")
        nameLbl.place(x=580, y=8, anchor="nw")

        instLbl = Label(root, text="Instruction",fg='white',
                        bg=self.color, font="Arial 12 bold")
        instLbl.place(x=50, y=60, anchor="nw")

        tmp = Label(root, width=50, bg='#77bcf2')
        tmp.place(x=150, y=61, anchor='nw')

        instEntry = Entry(root, bd=0, fg='white', insertbackground='white', bg=self.color, font="Arial 13 bold")
        instEntry.place(x=150, y=60, anchor="nw", width=360)

        def clicked(event):
            tmp.place(x=150, y=62, anchor="nw")

        def left(event):
            tmp.place(x=150, y=61, anchor="nw")

        instEntry.bind("<Return>", self.get_instruction)
        instEntry.bind("<FocusIn>", clicked)
        instEntry.bind("<FocusOut>", left)

        next_btn = Button(root, text="NEXT", bg="#03a7ff",
                          fg="white", font="Arial 13 bold", height=2, width=7,
                          activebackground="#476b6a", command=self.nextIR)
        next_btn.place(x=1100, y=55, anchor="nw")

        def enterNext(event):
            event.widget.config(cursor="hand2")

        def LeaveNext(event):
            event.widget.config(cursor="arrow")

        next_btn.bind("<Enter>", enterNext)
        next_btn.bind("<Leave>", LeaveNext)
        # root.bind("<Return>",self.nextIR)

        global priorityLabel

        priorityLabel = Label(root, text='0', bg='dark red',fg='white',font='Arial 13 bold', width=6, height=2)
        priorityLabel.place(x=1200, y =55, anchor='nw')

   
    def get_instruction(self, event):
        self.root.focus()
        instruction = event.widget.get()
        event.widget.delete(0, 'end')

        if (instruction != ""):
            self.current_ins = self.myQ.enqueue(instruction.upper())
            self.memory_queue(self.myQ.array)
    

    def control_unit(self, PC, IR, prioritybit):
        root = self.root
        tempFr = Frame(root, width=360, height=323, bg="#162121")
        tempFr.place(x=52, y=122, anchor="nw")

        ProcFrame = Frame(root, width=360, height=323,
                          bg="#294040",
                          highlightthickness=2,
                          highlightbackground="#528080")
        ProcFrame.place(x=50, y=120, anchor="nw")

        processorLbl = Label(ProcFrame, text="Processor", fg="#93dbd8",
                             font="Arial 14 bold", bg="#294040")
        processorLbl.place(x=30, y=18, anchor="nw")

        controller = Frame(ProcFrame, width=300, height=100, bg="#a1133b")
        controller.place(x=30, y=60, anchor="nw")

        controllerLbl = Label(controller, text="CONTROLLER", fg="white",
                              font="Arial 20 bold", bg="#a1133b")
        controllerLbl.place(x=50, y=30, anchor="nw")

        # PC IR Registers

        PCReg = Label(ProcFrame, text=PC,
                      height=2, width=5, font="Arial 18 bold",
                      bg="#3e36c9", fg="white")
        PCReg.place(x=30, y=200, anchor="nw")

        IRReg = Label(ProcFrame, text=IR,
                      height=2, width=13, font="Arial 18 bold",
                      bg="purple", fg="white")
        IRReg.place(x=127, y=200, anchor="nw")

        PCLbl = Label(ProcFrame, text="PC", fg="#61baba",
                      font="Arial 14 bold", bg="#294040")
        PCLbl.place(x=52, y=275, anchor="nw")

        IRLbl = Label(ProcFrame, text="IR", fg="#61baba",
                      font="Arial 14 bold", bg="#294040")
        IRLbl.place(x=215, y=275, anchor="nw")

        priorityLabel.config(text = prioritybit)

    def memory_queue(self, MemQueueList):
        root = self.root
        tempFr = Frame(root, width=360, height=245, bg="#162121")
        tempFr.place(x=52, y=462, anchor="nw")

        QueueFrame = Frame(root, width=360, height=245,
                           bg="#294040",
                           highlightthickness=2,
                           highlightbackground="#528080")
        QueueFrame.place(x=50, y=460, anchor="nw")

        MemoryLbl = Label(QueueFrame, text="Memory", fg="#93dbd8",
                          font="Arial 14 bold", bg="#294040")
        MemoryLbl.place(x=30, y=12, anchor="nw")

        MemBlocks = [0, 0, 0, 0]

        for i in range(4):

            MemLbl = Label(QueueFrame, text=self.MemLabelText[i], bg="#294040",
                           fg="#61baba", font="Arial 14 bold",)
            MemLbl.place(x=35, y=47+(i*48), anchor="nw")

            MemBlocks[i] = Label(QueueFrame, text=MemQueueList[i],
                                 height=2, width=20, font="Arial 13 bold",
                                 bg="#476b6a", fg="white")
            MemBlocks[i].place(x=120, y=40+(i*48), anchor="nw")

        # self.PCreg = MemLabelText[0]
        # if(self.IRreg == MemQueueList[0]):
        #     self.PCReg = MemLabelText[1]

    def registers_screen(self, regList, highlighter):
        root = self.root

        tempFr1 = Frame(root, width=360, height=323, bg="#162121")
        tempFr1.place(x=453, y=123, anchor="nw")

        RegFrame = Frame(root, width=360, height=323,
                         bg="#294040",
                         highlightthickness=2,
                         highlightbackground="#528080")
        RegFrame.place(x=450, y=120, anchor="nw")

        registersLbl = Label(RegFrame, text="General Registers", fg="#93dbd8",
                             font="Arial 14 bold", bg="#294040")
        registersLbl.place(x=30, y=18, anchor="nw")

        GPRegs = [0, 0, 0, 0, 0, 0, 0, 0]
        GPRegBoxes = [0, 0, 0, 0, 0, 0, 0, 0]

        UpperGPRegs = ["AH", "BH", "CH", "DH"]
        LowerGPRegs = ["AL", "BL", "CL", "DL"]

        UpperGPRegText = [regList[i] for i in range(0, 4)]
        LowerGPRegText = [regList[i] for i in range(4, 8)]

        for i in range(4):            
            GPRegs[i] = Label(RegFrame, text=UpperGPRegs[i], bg="#294040",
                              fg="#61baba", font="Arial 14 bold",)
            GPRegs[i].place(x=25, y=73+(i*65), anchor="nw")

            GPRegBoxes[i] = Label(RegFrame, text=UpperGPRegText[i],
                                  height=2, width=7, font="Arial 15 bold",
                                  bg="#476b6a", fg="white")
            GPRegBoxes[i].place(x=75, y=60+(i*65), anchor="nw")

            if(i == highlighter[0] or i == highlighter[1] or i == highlighter[4] or i == highlighter[5]):
                GPRegBoxes[i].config(bg = 'red', fg='white')

            GPRegs[i+4] = Label(RegFrame, text=LowerGPRegs[i], bg="#294040",
                                fg="#61baba", font="Arial 14 bold",)
            GPRegs[i+4].place(x=185, y=73+(i*65), anchor="nw")

            GPRegBoxes[i+4] = Label(RegFrame, text=LowerGPRegText[i],
                                    height=2, width=7, font="Arial 15 bold",
                                    bg="#476b6a", fg="white")
            GPRegBoxes[i+4].place(x=230, y=60+(i*65), anchor="nw")

            
            if(i+4 == highlighter[0] or i+4 == highlighter[1] or i+4 == highlighter[4] or i+4 == highlighter[5]):
                GPRegBoxes[i+4].config(bg = 'red', fg='white')
            
            self.opcodeScreen(self.DataObj.opcode)
    

    def opcodeScreen(self, opcodeList):
        root = self.root

        tempFr = Frame(root, width=360, height=245, bg="#162121")
        tempFr.place(x=452, y=462, anchor="nw")

        opFrame = Frame(root, width=360, height=245,
                         bg="#294040",
                         highlightthickness=2,
                         highlightbackground="#528080")
        opFrame.place(x=450, y=460, anchor="nw")

        codeLbl = Label(opFrame, text="Machine Code", fg="#93dbd8",
                          font="Arial 14 bold", bg="#294040")
        codeLbl.place(x=30, y=15, anchor="nw")

        oplabel = Label(opFrame, text="OPcode", fg="#61baba",
                          font="Arial 13 bold", bg="#294040")
        oplabel.place(x=38, y=150, anchor='nw')

        opcode = ''
        for i in range(6):
            opcode += opcodeList[i] 

        optextLabel = Label(opFrame, text=opcode,
                             height=2, width=8, font="Arial 14 bold",
                             bg="#476b6a", fg="white")
        optextLabel.place(x=20, y=80, anchor="nw")

        dlabel = Label(opFrame, text="D-bit", fg="#61baba",
                          font="Arial 13 bold", bg="#294040")
        dlabel.place(x=135, y=150, anchor='nw')
        
        dtextLabel = Label(opFrame, text=opcodeList[6],
                             height=2, width=4, font="Arial 14 bold",
                             bg="#476b6a", fg="white")
        dtextLabel.place(x=130, y=80, anchor="nw")

        wlabel = Label(opFrame, text="W-bit", fg="#61baba",
                          font="Arial 13 bold", bg="#294040")
        wlabel.place(x=195, y=150, anchor='nw')

        wtextLabel = Label(opFrame, text=opcodeList[7],
                             height=2, width=4, font="Arial 14 bold",
                             bg="#476b6a", fg="white")
        wtextLabel.place(x=192, y=80, anchor="nw")

        modlabel = Label(opFrame, text="MOD", fg="#61baba",
                          font="Arial 13 bold", bg="#294040")
        modlabel.place(x=268, y=150, anchor='nw')

        modtextLabel = Label(opFrame, text=opcodeList[8]+opcodeList[9],
                             height=2, width=6, font="Arial 14 bold",
                             bg="#476b6a", fg="white")
        modtextLabel.place(x=254, y=80, anchor="nw")
