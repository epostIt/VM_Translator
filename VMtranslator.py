#!/usr/bin/env python
'''
VM Translator
Daniel Kronovet
kronovet@gmail.com
'''
#small change

import os
import fileinput
import re


# FILE_PATH = '/Users/Elisabeth/Desktop/pj02_username/XVMTe/Test.vm'

COMMENT = '//'
global_curr_inst = None

class FileLine(object): 
    def checkIfLineIsComment(line):
        return line.startswith('//')

    def printError(stringLookingFor, error): #function that searches for the string causing a problem and finds the line number it is on
        stringLookingFor = stringLookingFor + "\n"
        with fileinput.input(files=(FILE_PATH)) as f:
            for line in f:
                if (stringLookingFor == line):
                    if not FileLine.checkIfLineIsComment(line):
                        print("ERROR:" + error + " - Line " + str(fileinput.lineno()) + ": " + line )
                        f = open("ErrorFile.txt", "a")
                        f.write("ERROR:" + error + " - Line " +
                                str(fileinput.lineno()) + ": " + line + "\n")
                        f.close()


# Create one per input file
class Parser(object):
    def __init__(self, vm_filename):
        self.vm_filename = vm_filename
        self.vm = open(vm_filename, 'r')
        self.EOF = False
        self.commands = self.commands_dict()
        self.curr_instruction = None
        self.initialize_file()

    #######
    ### API
    def advance(self):
        global global_curr_inst
        self.curr_instruction = self.next_instruction
        global_curr_inst = self.curr_instruction
        self.load_next_instruction()

    @property
    def has_more_commands(self):
        return not self.EOF

    @property
    def command_type(self):
        return self.commands.get(self.curr_instruction[0].lower())

    @property
    def arg1(self):
        '''Math operation if C_ARITHMETIC'''
        if self.command_type == 'C_ARITHMETIC':
            return self.argn(0)
        return self.argn(1)

    @property
    def arg2(self):
        '''Only return if C_PUSH, C_POP, C_FUNCTION, C_CALL'''
        return self.argn(2)

    ### END API
    ###########
    def close(self):
        self.vm.close()

    def initialize_file(self):
        self.vm.seek(0)
        self.load_next_instruction()

    def load_next_instruction(self, line=None):
        loaded = False
        while not loaded and not self.EOF:
            tell = self.vm.tell()
            line = self.vm.readline().strip()
            if self.is_instruction(line):
                self.next_instruction = line.split(COMMENT)[0].strip().split()
                loaded = True
            if tell == self.vm.tell(): # File position did not change
                self.EOF = True

    def is_instruction(self, line):
        return line and line[:2] != COMMENT

    def argn(self, n):
        if len(self.curr_instruction) >= n+1:
            return self.curr_instruction[n]
        return None

    def commands_dict(self):
        return {
            'add': 'C_ARITHMETIC',
            'sub': 'C_ARITHMETIC',
            'neg': 'C_ARITHMETIC',
             'eq': 'C_ARITHMETIC',
             'gt': 'C_ARITHMETIC',
             'lt': 'C_ARITHMETIC',
             'le': 'C_ARITHMETIC',
             'ge': 'C_ARITHMETIC',
             'ne': 'C_ARITHMETIC',
             'bool': 'C_BOOLEAN',
             'l-not': 'C_LOGICALNOT',
             'l-and': 'C_LOGICALAND',
             'l-or': 'C_LOGICALOR',
             'l-xor': 'C_LOGICALXOR',
            'and': 'C_ARITHMETIC',
             'or': 'C_ARITHMETIC',
            'not': 'C_ARITHMETIC',
           'push': 'C_PUSH',
            'pop': 'C_POP',
          'label': 'C_LABEL',
           'goto': 'C_GOTO',
        'if-goto': 'C_IF',
       'function': 'C_FUNCTION',
         'return': 'C_RETURN',
           'call': 'C_CALL'
        }


class CodeWriter(object):
    knownLabel = []
    '''Write .asm files
    Contract between methods:
    1. Contents of the A and D registries are not guaranteed,
        so methods must set them to the values they need.
    2. Methods must always leave @SP pointing to the correct location.
    '''
    def __init__(self, asm_filename):
        self.asm = open(asm_filename, 'w')
        self.curr_file = None
        self.addresses = self.address_dict()
        self.line_count = 0
        self.bool_count = 0 # Number of boolean comparisons so far
        self.call_count = 0 # Number of function calls so far

    #######
    ### API
    def write_init(self):
        self.write('@256')
        self.write('D=A')
        self.write('@SP')
        self.write('M=D')
        self.write_call('Sys.init', 0)
        # self.write('@Sys.init')
        # self.write('0;JMP')

    def set_file_name(self, vm_filename):
        '''Reset pointers'''
        self.curr_file = vm_filename.replace('.vm', '').split('/')[-1]
        # self.curr_file = vm_filename.replace('.vm', '')
        self.write('//////', code=False)
        self.write('// {}'.format(self.curr_file), code=False)

    def writeBoolean(self, operation):
        self.write('@SP')
        self.write('AM=M-1')
        self.write('D=M')
        self.write('@ENDBOOL{}'.format(self.bool_count))
        self.write('D;JEQ')
        self.pushTrueOnStack()
        self.write('(ENDBOOL{})'.format(self.bool_count), code=False)
        self.increment_SP()
        self.bool_count += 1

    def writeLogicalNot(self, operation):
        self.write('@SP')
        self.write('AM=M-1')
        self.write('D=M')
        self.write('@ENDBOOL{}'.format(self.bool_count))
        self.write('D;JEQ')
        self.pushFalseOnStack() #if false
        self.write('@ENDSTATEMENT{}'.format(self.bool_count))
        self.write('0;JMP')
        self.write('(ENDBOOL{})'.format(self.bool_count), code=False) #if true
        self.pushTrueOnStack()
        self.write('(ENDSTATEMENT{})'.format(self.bool_count), code=False)
        self.increment_SP()
        self.bool_count += 1

    def writeLogicalAnd(self, operation):
        self.write('@SP')
        self.write('AM=M-1') #decrement sp
        self.write('D=M')
        self.write('@LAND_FALSE{}'.format(self.bool_count))
        self.write('D;JEQ') #if the first value is 0 (false), jump to land_false
        self.write('@SP') #check next value
        self.write('A=M-1')
        self.write('D=M')
        self.write('@LAND_FALSE{}'.format(self.bool_count))
        self.write('D;JEQ') #if the second value is false, jump to land_false
        self.pushTrueOnStack() #both are true, so store true on stack
        self.write('@LAND_CONT{}'.format(self.bool_count))
        self.write('0;JMP') #skip storing false on the stack, jump to land_cont
        self.write('(LAND_FALSE{})'.format(self.bool_count), code=False)
        self.pushFalseOnStack()
        self.write('(LAND_CONT{})'.format(self.bool_count), code=False)
        self.increment_SP()

    def writeLogicalXOR(self, operation):
        self.write('@SP')
        self.write('AM=M-1') #decrement sp
        self.write('D=M') #grab first value
        self.write('@LXOR_SECOND_FALSE{}'.format(self.bool_count))
        self.write('D;JNE') #if the first value is true (non-zero), jump to second value
        
        self.write('@SP') #otherwise check next value
        self.write('A=M-1')
        self.write('D=M')
        self.write('@LXOR_FALSE{}'.format(self.bool_count))
        self.write('D;JEQ') #if the second value also false, jump to lor_false
        self.write('@LXOR_CONT{}'.format(self.bool_count))
        self.write('0;JMP') #and jump to continue

        self.write('(LXOR_SECOND_FALSE{})'.format(self.bool_count), code=False)
        self.write('@SP') #check next value
        self.write('A=M-1')
        self.write('D=M')
        self.write('@LXOR_FALSE{}'.format(self.bool_count))
        self.write('D;JNE') #if the second value TRUE, jump to lor_false
        
        self.pushTrueOnStack() #otherwise, push true on stack and jump to continue
        self.write('@LXOR_CONT{}'.format(self.bool_count))
        self.write('0;JMP') 

        self.write('(LXOR_FALSE{})'.format(self.bool_count), code=False)
        self.pushFalseOnStack()
        self.write('(LXOR_CONT{})'.format(self.bool_count), code=False)
        self.increment_SP()


    def writeLogicalOr(self, operation):
        self.write('@SP')
        self.write('AM=M-1') #decrement sp
        self.write('D=M')
        self.write('@LOR_NEXT{}'.format(self.bool_count))
        self.write('D;JEQ') #if the first value is 0 (false), jump to second value
        self.pushTrueOnStack()#otherwise, push true to stack
        self.write('@LOR_CONT{}'.format(self.bool_count)) 
        self.write('0;JMP') #jump to continue
        self.write('(LOR_NEXT{})'.format(self.bool_count), code=False)
        self.write('@SP') #check next value
        self.write('A=M-1')
        self.write('D=M')
        self.write('@LOR_FALSE{}'.format(self.bool_count))
        self.write('D;JEQ') #if the second value false, jump to lor_false
        self.pushTrueOnStack() #second is true, so store true on stack
        self.write('@LOR_CONT{}'.format(self.bool_count))
        self.write('0;JMP') #skip storing false on the stack, jump to land_cont
        self.write('(LOR_FALSE{})'.format(self.bool_count), code=False)
        self.pushFalseOnStack()
        self.write('(LOR_CONT{})'.format(self.bool_count), code=False)
        self.increment_SP()
    def write_arithmetic(self, operation):
        '''Apply operation to top of stack'''
        if operation not in ['neg', 'not']: # Binary operator
            self.pop_stack_to_D()
        self.decrement_SP()
        self.set_A_to_stack()

        if operation == 'add': # Arithmetic operators
            self.write('M=M+D')
        elif operation == 'sub':
            self.write('M=M-D')
        elif operation == 'and':
            self.write('M=M&D')
        elif operation == 'or':
            self.write('M=M|D')
        elif operation == 'neg':
            self.write('M=-M')
        elif operation == 'not':
            self.write('M=!M')
        elif operation in ['eq', 'gt', 'lt', 'le', 'ge', 'ne', 'bool']: # Boolean operators
            self.write('D=M-D')
            self.write('@BOOL{}'.format(self.bool_count))
##################### DO NOT PUT BOOL STATMENT HERE, WE DO NOT WANT THE D=M-D
            if operation == 'eq':
                self.write('D;JEQ') # if x == y, x - y == 0
            elif operation == 'gt':
                self.write('D;JGT') # if x > y, x - y > 0
            elif operation == 'lt':
                self.write('D;JLT') # if x < y, x - y < 0
            elif operation == 'le':
                self.write('D;JLE')
            elif operation == 'ge':
                self.write('D;JGE')
            elif operation == 'ne':
                self.write('D;JNE')

            self.set_A_to_stack()
            self.write('M=0') # False
            self.write('@ENDBOOL{}'.format(self.bool_count))
            self.write('0;JMP')

            self.write('(BOOL{})'.format(self.bool_count), code=False)
            self.set_A_to_stack()
            self.write('M=-1') # True
            


            self.write('(ENDBOOL{})'.format(self.bool_count), code=False)
            # if(operation == 'bool'): #false path for bool: push 0 onto stack
            #     self.write('@0')
            #     self.write('D=A')
            #     self.write('@SP')
            #     self.write('A=M')
            #     self.write('M=D')
            #     self.increment_SP
            self.bool_count += 1
        else:
            print("Hit")
            self.raise_unknown(operation)
        self.increment_SP()

    def check_for_negative_index(self, index):
        try:
            if(int(index) < 0):
                return True
            else:
                return False
        except:
            return True


    def checkIfSegmentIsInRange(self, segment, index):
        if(segment == 'temp'):
            if(int(index) > 7 or int(index)<0):
                FileLine.printError(' '.join(global_curr_inst), "Temp index out of range")
                return False
            else:
                return True
        if(segment == 'static'):
            if(self.check_for_negative_index(index) == True):
                FileLine.printError(' '.join(global_curr_inst), "Static index out of range")
                return False
            else:
                return True
        if(segment == 'pointer'):
            if(int(index)!=1):
                if(int(index)!=0):
                    FileLine.printError(' '.join(global_curr_inst), "Pointer index out of range")
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True


    def checkIfHasOneElement(curr_line):
        if(len(curr_line) != 1):
            FileLine.printError(' '.join(curr_line),"Improperly Formatted")
            return False
        else:
            return True

    def checkIfHasThreeElements(curr_line):
        if(len(curr_line) != 3):
            FileLine.printError(' '.join(curr_line),"Improperly Formatted")
            return False
        else:
            return True
    
    def checkIfKnownSegment(segment):
        if(segment != 'argument'):
            if(segment != 'local'):
                if(segment != 'static'):
                    if(segment != 'constant'):
                        if(segment != 'this'):
                            if(segment != 'that'):
                                if(segment != 'pointer'):
                                    if(segment != 'temp'):
                                        FileLine.printError(str(' '.join(global_curr_inst)),"Unknown Memory segment")
                                        return False
        return True


    def checkIfHasTwoElements(curr_line):
        if(len(curr_line) != 2):
            FileLine.printError(' '.join(curr_line),"Improperly Formatted")
            return False
        else:
            return True

    def checkIfFifteenBitUnsignedInt(index):
        if(int(index) >= 32768 or int(index) < 0):
            FileLine.printError(' '.join(global_curr_inst),"Index out of range")
            return False
        else:
            return True


    def checkIfValidFunctionOrLabelName(line):
        name = line[1]
        regex = re.compile('[@!#$%^&*()<>?/\|}{~]') 
        if(name[0].isdigit()):
            FileLine.printError(' '.join(global_curr_inst),"Invalid function name")
            return False
        elif(name[0].isalpha() == False):
            if(regex.search(name[0]) != None):
                FileLine.printError(' '.join(global_curr_inst),"Invalid function name")
                return False
        if(regex.search(name) != None):
            FileLine.printError(' '.join(global_curr_inst),"Invalid function name")
            return False
        
        else:
            return True
    
    def checkCount():
        count = int(global_curr_inst[2])
        if(count < 0):
            FileLine.printError(' '.join(global_curr_inst),"Illegal count")
            return False
        else:
            return True

    def write_push_pop(self, command, segment, index):
        self.resolve_address(segment, index)
        if command == 'C_PUSH': # load M[address] to D
            if segment == 'constant': #all ranges of segment are allowed, so no range checking needed
                if(CodeWriter.checkIfFifteenBitUnsignedInt(index) is True):
                    self.write('D=A')
                else:
                    self.write("Index out of range for this instruction")
            elif segment == 'ram':
                self.write('@' + str(index))
                self.write('D=M')
            else:
                if(self.checkIfSegmentIsInRange(segment, index) is True):
                    self.write('D=M')
            self.push_D_to_stack()
        elif command == 'C_POP': # load D to M[address]
            if(CodeWriter.checkIfHasThreeElements(global_curr_inst) is True):
                if(segment == 'constant'):
                    if(CodeWriter.checkIfFifteenBitUnsignedInt(index) is True):
                        self.decrement_SP()
                    else:
                        self.write("Index out of range for this instruction")
                elif(segment == 'ram'):
                    self.write('@SP')
                    self.write('AM=M-1')
                    self.write('D=M')
                    self.write('@' + str(index))
                    self.write('M=D')
                elif self.checkIfSegmentIsInRange(segment, index) is True:
                    self.write('D=A')
                    self.write('@R13') # Store resolved address in R13
                    self.write('M=D')
                    self.pop_stack_to_D()
                    self.write('@R13')
                    self.write('A=M')
                    self.write('M=D')
                
        else:
            self.raise_unknown(command)
   
    def write_label(self, label):
        self.write('({}${})'.format(self.curr_file, label), code=False)
        CodeWriter.knownLabel.append(label)
        

    def write_goto(self, label):
        if (label in CodeWriter.knownLabel):
            self.write('@{}${}'.format(self.curr_file, label))
            self.write('0;JMP')
        else:
            FileLine.printError(str(' '.join(global_curr_inst)),"Unresolved label")

        

    def write_if(self, label):
        if (label in CodeWriter.knownLabel):
            self.pop_stack_to_D()
            self.write('@{}${}'.format(self.curr_file, label))
            self.write('D;JNE')
        else:
            FileLine.printError(str(' '.join(global_curr_inst)),"Unresolved label")

        

    def write_function(self, function_name, num_locals):
        # (f)
        self.write('({})'.format(function_name), code=False)

        # k times: push 0
        for _ in range(num_locals): # Initialize local vars to 0
            self.write('D=0')
            self.push_D_to_stack()

    def write_call(self, function_name, num_args):
        RET = function_name + 'RET' +  str(self.call_count) # Unique return label
        self.call_count += 1

        # push return-address
        self.write('@' + RET)
        self.write('D=A')
        self.push_D_to_stack()

        # push LCL
        # push ARG
        # push THIS
        # push THAT
        for address in ['@LCL', '@ARG', '@THIS', '@THAT']:
            self.write(address)
            self.write('D=M')
            self.push_D_to_stack()

        # LCL = SP
        self.write('@SP')
        self.write('D=M')
        self.write('@LCL')
        self.write('M=D')

        # ARG = SP-n-5
        # self.write('@SP') # Redundant b/c of prev two commands
        # self.write('D=M') # Redundant b/c of prev two commands
        self.write('@' + str(num_args + 5))
        self.write('D=D-A')
        self.write('@ARG')
        self.write('M=D')

        # goto f
        self.write('@' + function_name)
        self.write('0;JMP')

        # (return_address)
        self.write('({})'.format(RET), code=False)

    def write_return(self):
        # Temporary variables
        FRAME = 'R13'
        RET = 'R14'

        # FRAME = LCL
        self.write('@LCL')
        self.write('D=M')
        self.write('@' + FRAME)
        self.write('M=D')

        # RET = *(FRAME-5)
        # Can't be included in iterator b/c value will be overwritten if num_args=0
        self.write('@' + FRAME)
        self.write('D=M') # Save start of frame
        self.write('@5')
        self.write('D=D-A') # Adjust address
        self.write('A=D') # Prepare to load value at address
        self.write('D=M') # Store value
        self.write('@' + RET)
        self.write('M=D') # Save value

        # *ARG = pop()
        self.pop_stack_to_D()
        self.write('@ARG')
        self.write('A=M')
        self.write('M=D')

        # SP = ARG+1
        self.write('@ARG')
        self.write('D=M')
        self.write('@SP')
        self.write('M=D+1')

        # THAT = *(FRAME-1)
        # THIS = *(FRAME-2)
        # ARG = *(FRAME-3)
        # LCL = *(FRAME-4)
        offset = 1
        for address in ['@THAT', '@THIS', '@ARG', '@LCL']:
            self.write('@' + FRAME)
            self.write('D=M') # Save start of frame
            self.write('@' + str(offset))
            self.write('D=D-A') # Adjust address
            self.write('A=D') # Prepare to load value at address
            self.write('D=M') # Store value
            self.write(address)
            self.write('M=D') # Save value
            offset += 1

        # goto RET
        self.write('@' + RET)
        self.write('A=M')
        self.write('0;JMP')

    ### END API
    ###########
    def write(self, command, code=True):
        self.asm.write(command)
        if code:
            self.asm.write(' // ' + str(self.line_count))
            self.line_count += 1
        self.asm.write('\n')

    def close(self):
        self.asm.close()

    def raise_unknown(self, argument):
        self.write("This is an unknown memory segment ")
        FileLine.printError(str(' '.join(global_curr_inst)),"Unknown Memory segment")

    
    def resolve_address(self, segment, index):
        
        '''Resolve address to A register'''
        address = str(self.addresses.get(segment)) #####################Cast this to a string, not sure if thats right
        if segment == 'constant':
            self.write('@' + str(index))
        elif segment == 'static':
            self.write('@' + self.curr_file + '.' + str(index))
        elif segment in ['pointer', 'temp']:
            self.write('@R' + str(address + index)) # Address is an int
        elif segment in ['local', 'argument', 'this', 'that']:
            self.write('@' + address) # Address is a string
            self.write('D=M')
            self.write('@' + str(index))
            self.write('A=D+A') # D is segment base
        elif(segment != 'ram'):
            self.raise_unknown(segment)

    def address_dict(self):
        return {
            'local': 'LCL', # Base R1
            'argument': 'ARG', # Base R2
            'this': 'THIS', # Base R3
            'that': 'THAT', # Base R4
            'pointer': 3, # Edit R3, R4
            'temp': 5, # Edit R5-12
            # R13-15 are free
            'static': 16, # Edit R16-255
        }

    def push_D_to_stack(self):
        '''Push from D onto top of stack, increment @SP'''
        self.write('@SP') # Get current stack pointer
        self.write('A=M') # Set address to current stack pointer
        self.write('M=D') # Write data to top of stack
        self.increment_SP()

    def pop_stack_to_D(self):
        '''Decrement @SP, pop from top of stack onto D'''
        self.decrement_SP()
        self.write('A=M') # Set address to current stack pointer
        self.write('D=M') # Get data from top of stack

    def decrement_SP(self):
        self.write('@SP')
        self.write('M=M-1')

    def increment_SP(self):
        self.write('@SP')
        self.write('M=M+1')

    def set_A_to_stack(self):
        self.write('@SP')
        self.write('A=M')
        
    def pushTrueOnStack(self):
        self.write('@SP')
        self.write('AM=M-1')
        self.write('M=-1')
    
    def pushFalseOnStack(self):
        self.write('@SP')
        self.write('A=M')
        self.write('M=0')


class Main(object):
    def __init__(self, FILE_PATH):
        self.parse_files(FILE_PATH)
        self.cw = CodeWriter(self.asm_file)
        # self.cw.write_init()
        for vm_file in self.vm_files:
            self.translate(vm_file)
        self.cw.close()

    def parse_files(self, FILE_PATH):
        if '.vm' in FILE_PATH:
            self.asm_file = FILE_PATH.replace('.vm', '.asm')
            self.vm_files = [FILE_PATH]
        else:
            FILE_PATH = FILE_PATH[:-1] if FILE_PATH[-1] == '/' else FILE_PATH
            path_elements = FILE_PATH.split('/')
            path = '/'.join(path_elements)
            self.asm_file = path + '/' + path_elements[-1] + '.asm'
            dirpath, dirnames, filenames = next(os.walk(FILE_PATH), [[],[],[]])
            vm_files = filter(lambda x: '.vm' in x, filenames)
            self.vm_files = [path + '/' +  vm_file for vm_file in vm_files]

    def translate(self, vm_file):
        parser = Parser(vm_file)
        self.cw.set_file_name(vm_file)
        while parser.has_more_commands:
            parser.advance()
            self.cw.write('// ' + ' '.join(parser.curr_instruction), code=False)
            if parser.command_type == 'C_PUSH':
                if(CodeWriter.checkIfHasThreeElements(global_curr_inst) == True):
                    self.cw.write_push_pop('C_PUSH', parser.arg1, parser.arg2)
                else:
                    self.cw.write("Command improperly formatted")
            elif parser.command_type == 'C_POP':
                if(CodeWriter.checkIfHasThreeElements(global_curr_inst) == True):
                    self.cw.write_push_pop('C_POP', parser.arg1, parser.arg2)
                else:
                    self.cw.write("Command improperly formatted")
            elif parser.command_type == 'C_ARITHMETIC': 
                if(CodeWriter.checkIfHasOneElement(global_curr_inst) == True):
                    self.cw.write_arithmetic(parser.arg1)
                else:
                    self.cw.write("Command improperly formatted")
            elif parser.command_type == 'C_LOGICALNOT':
                if(CodeWriter.checkIfHasOneElement(global_curr_inst) == True):
                    self.cw.writeLogicalNot(parser.arg1)
                else:
                    self.cw.write("Command improperly formatted")
            elif parser.command_type == 'C_LOGICALAND':
                if(CodeWriter.checkIfHasOneElement(global_curr_inst) == True):
                    self.cw.writeLogicalAnd(parser.arg1)
                else:
                    self.cw.write("Command improperly formatted")
            elif parser.command_type == 'C_LOGICALOR':
                if(CodeWriter.checkIfHasOneElement(global_curr_inst) == True):
                    self.cw.writeLogicalOr(parser.arg1)
                else:
                    self.cw.write("Command improperly formatted")
            elif parser.command_type == 'C_LOGICALXOR':
                if(CodeWriter.checkIfHasOneElement(global_curr_inst) == True):
                    self.cw.writeLogicalXOR(parser.arg1)
                else:
                    self.cw.write("Command improperly formatted")
            elif parser.command_type == 'C_BOOLEAN':
                if(CodeWriter.checkIfHasOneElement(global_curr_inst) == True):
                    self.cw.writeBoolean(parser.arg1)
                else:
                    self.cw.write("Command improperly formatted")
            elif parser.command_type == 'C_LABEL':
                if(CodeWriter.checkIfHasTwoElements(global_curr_inst) == True):
                    if(CodeWriter.checkIfValidFunctionOrLabelName(global_curr_inst) == True):
                        self.cw.write_label(parser.arg1)
                    else:
                        self.cw.write("Invalid label name")
                else:
                    self.cw.write("Command improperly formatted")
            elif parser.command_type == 'C_GOTO':
                if(CodeWriter.checkIfHasTwoElements(global_curr_inst) == True):
                    if(CodeWriter.checkIfValidFunctionOrLabelName(global_curr_inst) == True):
                        self.cw.write_goto(parser.arg1)
                    else:
                        self.cw.write("Invalid label call")
                else:
                    self.cw.write("Command improperly formatted")
            elif parser.command_type == 'C_IF':
                if(CodeWriter.checkIfHasTwoElements(global_curr_inst) == True):
                    if(CodeWriter.checkIfValidFunctionOrLabelName(global_curr_inst) == True):
                        self.cw.write_if(parser.arg1)
                    else:
                        self.cw.write("Invalid label call")
                else:
                    self.cw.write("Command improperly formatted")
            elif parser.command_type == 'C_FUNCTION':
                if(CodeWriter.checkIfHasThreeElements(global_curr_inst) == True):
                    if(CodeWriter.checkIfValidFunctionOrLabelName(global_curr_inst) == True):
                        if(CodeWriter.checkCount() ==  True):
                            self.cw.write_function(parser.arg1, int(parser.arg2))
                        else:
                            self.cw.write("Non-negative number was used")
                    else:
                        self.cw.write("Invalid function name")
                else:
                    self.cw.write("Command improperly formatted")
            elif parser.command_type == 'C_CALL':
                if(CodeWriter.checkIfHasThreeElements(global_curr_inst) == True):
                    if(CodeWriter.checkIfValidFunctionOrLabelName(global_curr_inst) == True):
                        if(CodeWriter.checkCount() ==  True):
                            self.cw.write_call(parser.arg1, int(parser.arg2))
                        else:
                            self.cw.write("Non-negative number was used")
                    else:
                        self.cw.write("Invalid function name")
                else:
                    self.cw.write("Command improperly formatted")
            elif parser.command_type == 'C_RETURN':
                if(CodeWriter.checkIfHasOneElement(global_curr_inst) == True):
                    self.cw.write_return()
                else:
                    self.cw.write("Command improperly formatted")
            else:
                FileLine.printError(' '.join(parser.curr_instruction), "Unknown Command") #if not one of the recognized instructions, it must be some type of error
        parser.close()


if __name__ == '__main__':
    import sys

    FILE_PATH = sys.argv[1]
    Main(FILE_PATH)
