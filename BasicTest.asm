@256 // 0
D=A // 1
@SP // 2
M=D // 3
@Sys.initRET0 // 4
D=A // 5
@SP // 6
A=M // 7
M=D // 8
@SP // 9
M=M+1 // 10
@LCL // 11
D=M // 12
@SP // 13
A=M // 14
M=D // 15
@SP // 16
M=M+1 // 17
@ARG // 18
D=M // 19
@SP // 20
A=M // 21
M=D // 22
@SP // 23
M=M+1 // 24
@THIS // 25
D=M // 26
@SP // 27
A=M // 28
M=D // 29
@SP // 30
M=M+1 // 31
@THAT // 32
D=M // 33
@SP // 34
A=M // 35
M=D // 36
@SP // 37
M=M+1 // 38
@SP // 39
D=M // 40
@LCL // 41
M=D // 42
@5 // 43
D=D-A // 44
@ARG // 45
M=D // 46
@Sys.init // 47
0;JMP // 48
(Sys.initRET0)
//////
// BasicTest
// bool
@SP // 49
M=M-1 // 50
A=M // 51
D=M // 52
@SP // 53
M=M-1 // 54
@SP // 55
A=M // 56
D=M-D // 57
@BOOL0 // 58
D;JEQ // 59
@SP // 60
A=M // 61
M=0 // 62
@ENDBOOL0 // 63
0;JMP // 64
(BOOL0)
@SP // 65
A=M // 66
M=-1 // 67
(ENDBOOL0)
@SP // 68
M=M+1 // 69
