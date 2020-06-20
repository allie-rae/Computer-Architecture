"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256 # size of RAM
        self.register = [0] * 8 # 8 registers
        self.pc = 0 # program counter starts at 0
        self.hlt = False # halted is false
        self.sp = 0xF4 # pointer to top of stack
        self.ldi = 0b10000010 
        self.prn = 0b01000111 
        self.halt = 0b00000001


    def ram_read(self, mar): # MAR = memory address register
        return self.ram[mar] 
    
    def ram_write(self, mdr, mar): # MDR = memory data register
        self.ram[mar] = mdr 

    def LDI(self): # store a value in register
        self.register[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
        self.pc += 3

    def PRN(self): # print a value in register
        print(f'value: {self.register[self.ram_read(self.pc + 1)]}')
        self.pc += 2

    def HLT(self): # stop program (halt)
        self.hlt = True
        self.pc += 1

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        while self.hlt == False: 
            ir = self.ram[self.pc] # IR = instruction register
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == self.ldi:
                self.LDI()
            elif ir == self.prn:
                self.PRN()
            elif ir == self.halt:
                self.HLT()
            

