//////
// ErrorTest
// poopy label 2
// pop4 thing
// _pop_ thing
// push. okay
// and$
// $or
// pop temp
Command improperly formatted // 0
// pop temp 5 okay
Command improperly formatted // 1
// push temp
Command improperly formatted // 2
// push
Command improperly formatted // 3
// function epic 5 5
Command improperly formatted // 4
// add 5 6
Command improperly formatted // 5
// sub 3
Command improperly formatted // 6
// and 1 1 1 1 1 1
Command improperly formatted // 7
// push fake 69
This is an unknown memory segment  // 8
D=M // 9
@SP // 10
A=M // 11
M=D // 12
@SP // 13
M=M+1 // 14
// pop fake 69
This is an unknown memory segment  // 15
D=A // 16
@R13 // 17
M=D // 18
@SP // 19
M=M-1 // 20
A=M // 21
D=M // 22
@R13 // 23
A=M // 24
M=D // 25
// push constant -666
@-666 // 26
Index out of range for this instruction // 27
@SP // 28
A=M // 29
M=D // 30
@SP // 31
M=M+1 // 32
// pop local -1
@LCL // 33
D=M // 34
@-1 // 35
A=D+A // 36
D=A // 37
@R13 // 38
M=D // 39
@SP // 40
M=M-1 // 41
A=M // 42
D=M // 43
@R13 // 44
A=M // 45
M=D // 46
// push this -1
@THIS // 47
D=M // 48
@-1 // 49
A=D+A // 50
D=M // 51
@SP // 52
A=M // 53
M=D // 54
@SP // 55
M=M+1 // 56
// push that -1
@THAT // 57
D=M // 58
@-1 // 59
A=D+A // 60
D=M // 61
@SP // 62
A=M // 63
M=D // 64
@SP // 65
M=M+1 // 66
// pop constat NAN
This is an unknown memory segment  // 67
D=A // 68
@R13 // 69
M=D // 70
@SP // 71
M=M-1 // 72
A=M // 73
D=M // 74
@R13 // 75
A=M // 76
M=D // 77
// pop aCap inYoButt
This is an unknown memory segment  // 78
D=A // 79
@R13 // 80
M=D // 81
@SP // 82
M=M-1 // 83
A=M // 84
D=M // 85
@R13 // 86
A=M // 87
M=D // 88
// push constant 42069420
@42069420 // 89
Index out of range for this instruction // 90
@SP // 91
A=M // 92
M=D // 93
@SP // 94
M=M+1 // 95
// pop temp 8
@R58 // 96
D=A // 97
@R13 // 98
M=D // 99
@SP // 100
M=M-1 // 101
A=M // 102
D=M // 103
@R13 // 104
A=M // 105
M=D // 106
// pop local 32768
@LCL // 107
D=M // 108
@32768 // 109
A=D+A // 110
D=A // 111
@R13 // 112
M=D // 113
@SP // 114
M=M-1 // 115
A=M // 116
D=M // 117
@R13 // 118
A=M // 119
M=D // 120
// pop argument 32768
@ARG // 121
D=M // 122
@32768 // 123
A=D+A // 124
D=A // 125
@R13 // 126
M=D // 127
@SP // 128
M=M-1 // 129
A=M // 130
D=M // 131
@R13 // 132
A=M // 133
M=D // 134
// push pointer 3
@R33 // 135
@SP // 136
A=M // 137
M=D // 138
@SP // 139
M=M+1 // 140
// pop pointer 3
@R33 // 141
D=A // 142
@R13 // 143
M=D // 144
@SP // 145
M=M-1 // 146
A=M // 147
D=M // 148
@R13 // 149
A=M // 150
M=D // 151
// push static 240
@ErrorTest.240 // 152
D=M // 153
@SP // 154
A=M // 155
M=D // 156
@SP // 157
M=M+1 // 158
// pop static 240
@ErrorTest.240 // 159
D=A // 160
@R13 // 161
M=D // 162
@SP // 163
M=M-1 // 164
A=M // 165
D=M // 166
@R13 // 167
A=M // 168
M=D // 169
// push ram 32768
@32768 // 170
D=M // 171
@SP // 172
A=M // 173
M=D // 174
@SP // 175
M=M+1 // 176
// pop ram 32768
@SP // 177
AM=M-1 // 178
D=M // 179
@32768 // 180
M=D // 181
// label %okay%
Invalid label name // 182
// label (okay)
Invalid label name // 183
// label ok~ay
Invalid label name // 184
// goto 123dk
Invalid label call // 185
// if-goto YEET*&
Invalid label call // 186
// goto doesNotExist
// if-goto doesNotExist
// function %okay% 1
Invalid function name // 187
// function (okay) 1
Invalid function name // 188
// function 123dk 1
Invalid function name // 189
// function YEET*& 1
Invalid function name // 190
// call %okay% 1
Invalid function name // 191
// call (okay) 1
Invalid function name // 192
// call 123dk 1
Invalid function name // 193
// call YEET*& 1
Invalid function name // 194
// function okay -5
Non-negative number was used // 195
// call okay -5
Non-negative number was used // 196
