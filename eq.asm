@SP // 0
M=M-1 // 1
A=M // 2
D=M // 3
@SP // 4
M=M-1 // 5
@SP // 6
A=M // 7
D=M-D // 8
@BOOL0 // 9
D;JEQ // 10
@SP // 11
A=M // 12
M=0 // 13
@ENDBOOL0 // 14
0;JMP // 15
(BOOL0)
@SP // 16
A=M // 17
M=-1 // 18
(ENDBOOL0)
@SP // 19
M=M+1 // 20
