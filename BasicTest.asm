//////
// BasicTest
// l-or
@SP // 0
AM=M-1 // 1
D=M // 2
@LOR_NEXT0 // 3
D;JEQ // 4
@SP // 5
AM=M-1 // 6
M=-1 // 7
@LOR_CONT0 // 8
0;JMP // 9
(LOR_NEXT0)
@SP // 10
A=M-1 // 11
D=M // 12
@LOR_FALSE0 // 13
D;JEQ // 14
@SP // 15
AM=M-1 // 16
M=-1 // 17
@LOR_CONT0 // 18
0;JMP // 19
(LOR_FALSE0)
@SP // 20
A=M // 21
M=0 // 22
(LOR_CONT0)
@SP // 23
M=M+1 // 24
