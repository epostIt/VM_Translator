//////
// BasicTest
// push constant 0B1111111
@127 // 0
D=A // 1
@SP // 2
A=M // 3
M=D // 4
@SP // 5
M=M+1 // 6
// push constant 0X7fff
@32767 // 7
D=A // 8
@SP // 9
A=M // 10
M=D // 11
@SP // 12
M=M+1 // 13
