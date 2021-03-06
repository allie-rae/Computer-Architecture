"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256  # size of RAM
        self.register = [0] * 8  # 8 registers
        self.pc = 0  # program counter starts at 0
        self.hlt = False  # halted default value is false
        self.sp = 0xF4  # pointer to top of stack
        self.ldi = 0b10000010
        self.prn = 0b01000111
        self.halt = 0b00000001
        self.mul = 0b10100010
        self.cmp = 0b10100111
        self.jmp = 0b01010100
        self.jeq = 0b01010101
        self.jne = 0b01010110
        self.E = 0
        self.G = 0
        self.L = 0

    def ram_read(self, mar):  # MAR = memory address register
        return self.ram[mar]

    def ram_write(self, mdr, mar):  # MDR = memory data register
        self.ram[mar] = mdr

    def load(self, filename):
        address = 0
        with open(filename) as f:
            for line in f:
                cleaned_code = line.split("#")[0].strip()
                if cleaned_code == "":
                    continue
                base_10 = int(cleaned_code, 2)
                self.ram[address] = base_10
                address += 1

    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        elif op == "CMP":
            if self.register[reg_a] == self.register[reg_b]:
                self.E = 1
            elif self.register[reg_a] > self.register[reg_b]:
                self.G = 1
            elif self.register[reg_a] < self.register[reg_b]:
                self.L = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        while self.hlt == False:
            ir = self.ram[self.pc]  # IR = instruction register
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == self.ldi:  # store a value in register
                self.register[self.ram_read(
                    self.pc + 1)] = self.ram_read(self.pc + 2)
                self.pc += 3
            elif ir == self.prn:  # print a value in the register
                print(f'{self.register[self.ram_read(self.pc + 1)]}')
                self.pc += 2
            elif ir == self.mul:  # multiply
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif ir == self.cmp:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3
            elif ir == self.halt:
                self.hlt = True
                self.pc += 1
            elif ir == self.jmp:
                self.pc = self.register[operand_a]
            elif ir == self.jeq:
                if self.E == 1:
                    self.pc = self.register[operand_a]
                else:
                    self.pc += 2
            elif ir == self.jne:
                if self.E == 0:
                    self.pc = self.register[operand_a]
                else:
                    self.pc += 2
            else:
                raise Exception("Unsupported ALU operation")
