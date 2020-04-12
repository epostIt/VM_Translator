//////
// BasicTest
// l-xor
@SP // 0
AM=M-1 // 1
D=M // 2
@LXOR_SECOND_FALSE0 // 3
D;JNE // 4
@SP // 5
A=M-1 // 6
D=M // 7
@LXOR_FALSE0 // 8
D;JEQ // 9
@LXOR_CONT0 // 10
0;JMP // 11
(LXOR_SECOND_FALSE0)
@SP // 12
A=M-1 // 13
D=M // 14
@LXOR_FALSE0 // 15
D;JNE // 16
@SP // 17
AM=M-1 // 18
M=-1 // 19
@LXOR_CONT0 // 20
0;JMP // 21
(LXOR_FALSE0)
@SP // 22
A=M // 23
M=0 // 24
(LXOR_CONT0)
@SP // 25
M=M+1 // 26
