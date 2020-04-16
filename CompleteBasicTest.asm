//////
// CompleteBasicTest
// Executes pop and push commands using the virtual memory segments.
// push constant 10
@10 // 0
D=A // 1
@SP // 2
A=M // 3
M=D // 4
@SP // 5
M=M+1 // 6
// pop local 0
@LCL // 7
D=M // 8
@0 // 9
A=D+A // 10
D=A // 11
@R13 // 12
M=D // 13
@SP // 14
M=M-1 // 15
A=M // 16
D=M // 17
@R13 // 18
A=M // 19
M=D // 20
// push constant 21
@21 // 21
D=A // 22
@SP // 23
A=M // 24
M=D // 25
@SP // 26
M=M+1 // 27
// push constant 22
@22 // 28
D=A // 29
@SP // 30
A=M // 31
M=D // 32
@SP // 33
M=M+1 // 34
// pop argument 2
@ARG // 35
D=M // 36
@2 // 37
A=D+A // 38
D=A // 39
@R13 // 40
M=D // 41
@SP // 42
M=M-1 // 43
A=M // 44
D=M // 45
@R13 // 46
A=M // 47
M=D // 48
// pop argument 1
@ARG // 49
D=M // 50
@1 // 51
A=D+A // 52
D=A // 53
@R13 // 54
M=D // 55
@SP // 56
M=M-1 // 57
A=M // 58
D=M // 59
@R13 // 60
A=M // 61
M=D // 62
// push constant 36
@36 // 63
D=A // 64
@SP // 65
A=M // 66
M=D // 67
@SP // 68
M=M+1 // 69
// this should throw
// pop this 6
@THIS // 70
D=M // 71
@6 // 72
A=D+A // 73
D=A // 74
@R13 // 75
M=D // 76
@SP // 77
M=M-1 // 78
A=M // 79
D=M // 80
@R13 // 81
A=M // 82
M=D // 83
// push constant 42
@42 // 84
D=A // 85
@SP // 86
A=M // 87
M=D // 88
@SP // 89
M=M+1 // 90
// push constant 45
@45 // 91
D=A // 92
@SP // 93
A=M // 94
M=D // 95
@SP // 96
M=M+1 // 97
// pop that 5
@THAT // 98
D=M // 99
@5 // 100
A=D+A // 101
D=A // 102
@R13 // 103
M=D // 104
@SP // 105
M=M-1 // 106
A=M // 107
D=M // 108
@R13 // 109
A=M // 110
M=D // 111
// pop that 2
@THAT // 112
D=M // 113
@2 // 114
A=D+A // 115
D=A // 116
@R13 // 117
M=D // 118
@SP // 119
M=M-1 // 120
A=M // 121
D=M // 122
@R13 // 123
A=M // 124
M=D // 125
// push constant 510
@510 // 126
D=A // 127
@SP // 128
A=M // 129
M=D // 130
@SP // 131
M=M+1 // 132
// pop temp 6
@R56 // 133
D=A // 134
@R13 // 135
M=D // 136
@SP // 137
M=M-1 // 138
A=M // 139
D=M // 140
@R13 // 141
A=M // 142
M=D // 143
// push local 0
@LCL // 144
D=M // 145
@0 // 146
A=D+A // 147
D=M // 148
@SP // 149
A=M // 150
M=D // 151
@SP // 152
M=M+1 // 153
// push that 5
@THAT // 154
D=M // 155
@5 // 156
A=D+A // 157
D=M // 158
@SP // 159
A=M // 160
M=D // 161
@SP // 162
M=M+1 // 163
// add
@SP // 164
M=M-1 // 165
A=M // 166
D=M // 167
@SP // 168
M=M-1 // 169
@SP // 170
A=M // 171
M=M+D // 172
@SP // 173
M=M+1 // 174
// push argument 1
@ARG // 175
D=M // 176
@1 // 177
A=D+A // 178
D=M // 179
@SP // 180
A=M // 181
M=D // 182
@SP // 183
M=M+1 // 184
// sub
@SP // 185
M=M-1 // 186
A=M // 187
D=M // 188
@SP // 189
M=M-1 // 190
@SP // 191
A=M // 192
M=M-D // 193
@SP // 194
M=M+1 // 195
// push this 6
@THIS // 196
D=M // 197
@6 // 198
A=D+A // 199
D=M // 200
@SP // 201
A=M // 202
M=D // 203
@SP // 204
M=M+1 // 205
// push this 6
@THIS // 206
D=M // 207
@6 // 208
A=D+A // 209
D=M // 210
@SP // 211
A=M // 212
M=D // 213
@SP // 214
M=M+1 // 215
// add
@SP // 216
M=M-1 // 217
A=M // 218
D=M // 219
@SP // 220
M=M-1 // 221
@SP // 222
A=M // 223
M=M+D // 224
@SP // 225
M=M+1 // 226
// sub
@SP // 227
M=M-1 // 228
A=M // 229
D=M // 230
@SP // 231
M=M-1 // 232
@SP // 233
A=M // 234
M=M-D // 235
@SP // 236
M=M+1 // 237
// push temp 6
@R56 // 238
D=M // 239
@SP // 240
A=M // 241
M=D // 242
@SP // 243
M=M+1 // 244
// add
@SP // 245
M=M-1 // 246
A=M // 247
D=M // 248
@SP // 249
M=M-1 // 250
@SP // 251
A=M // 252
M=M+D // 253
@SP // 254
M=M+1 // 255
