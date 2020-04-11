//////
// BasicTest
// l-not
@SP // 0
AM=M-1 // 1
D=M // 2
@ENDBOOL0 // 3
D;JEQ // 4
@SP // 5
A=M // 6
M=0 // 7
@ENDSTATEMENT0 // 8
0;JMP // 9
(ENDBOOL0)
@SP // 10
A=M // 11
M=-1 // 12
(ENDSTATEMENT0)
@SP // 13
M=M+1 // 14
