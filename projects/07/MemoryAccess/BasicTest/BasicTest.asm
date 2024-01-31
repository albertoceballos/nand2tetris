// push constant 10
//*sp=i
@10
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// pop local 0
// addr = segment_pointer + segment_num
@0
D=A
@LCL
D=D+M
@addr
M=D
// SP--
@SP
M=M-1
// *addr = *sp
@SP
A=M
D=M
@addr
A=M
M=D

// push constant 21
//*sp=i
@21
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// push constant 22
//*sp=i
@22
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// pop argument 2
// addr = segment_pointer + segment_num
@2
D=A
@ARG
D=D+M
@addr
M=D
// SP--
@SP
M=M-1
// *addr = *sp
@SP
A=M
D=M
@addr
A=M
M=D

// pop argument 1
// addr = segment_pointer + segment_num
@1
D=A
@ARG
D=D+M
@addr
M=D
// SP--
@SP
M=M-1
// *addr = *sp
@SP
A=M
D=M
@addr
A=M
M=D

// push constant 36
//*sp=i
@36
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// pop this 6
// addr = segment_pointer + segment_num
@6
D=A
@THIS
D=D+M
@addr
M=D
// SP--
@SP
M=M-1
// *addr = *sp
@SP
A=M
D=M
@addr
A=M
M=D

// push constant 42
//*sp=i
@42
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// push constant 45
//*sp=i
@45
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// pop that 5
// addr = segment_pointer + segment_num
@5
D=A
@THAT
D=D+M
@addr
M=D
// SP--
@SP
M=M-1
// *addr = *sp
@SP
A=M
D=M
@addr
A=M
M=D

// pop that 2
// addr = segment_pointer + segment_num
@2
D=A
@THAT
D=D+M
@addr
M=D
// SP--
@SP
M=M-1
// *addr = *sp
@SP
A=M
D=M
@addr
A=M
M=D

// push constant 510
//*sp=i
@510
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// pop temp 6
// addr = 5 + segment_num
@5
D=A
@6
D=D+A
@addr
M=D
// SP--
@SP
M=M-1
// *addr = *sp
@SP
A=M
D=M
@addr
A=M
M=D

// push local 0
// addr = segment_pointer + segment_num
@0
D=A
@LCL
D=D+M
@addr
M=D
// *sp = *addr
@addr
A=M
D=M
@SP
A=M
M=D
// SP++
@SP
M=M+1

// push that 5
// addr = segment_pointer + segment_num
@5
D=A
@THAT
D=D+M
@addr
M=D
// *sp = *addr
@addr
A=M
D=M
@SP
A=M
M=D
// SP++
@SP
M=M+1

//add
@SP
M=M-1
@SP
A=M
D=M
@a
M=D
@SP
M=M-1
@SP
A=M
D=M
@b
M=D
@b
D=M
@a
D=D+M
@SP
A=M
M=D
@SP
M=M+1

// push argument 1
// addr = segment_pointer + segment_num
@1
D=A
@ARG
D=D+M
@addr
M=D
// *sp = *addr
@addr
A=M
D=M
@SP
A=M
M=D
// SP++
@SP
M=M+1

//sub
@SP
M=M-1
@SP
A=M
D=M
@a
M=D
@SP
M=M-1
@SP
A=M
D=M
@b
M=D
@b
D=M
@a
D=D-M
@SP
A=M
M=D
@SP
M=M+1

// push this 6
// addr = segment_pointer + segment_num
@6
D=A
@THIS
D=D+M
@addr
M=D
// *sp = *addr
@addr
A=M
D=M
@SP
A=M
M=D
// SP++
@SP
M=M+1

// push this 6
// addr = segment_pointer + segment_num
@6
D=A
@THIS
D=D+M
@addr
M=D
// *sp = *addr
@addr
A=M
D=M
@SP
A=M
M=D
// SP++
@SP
M=M+1

//add
@SP
M=M-1
@SP
A=M
D=M
@a
M=D
@SP
M=M-1
@SP
A=M
D=M
@b
M=D
@b
D=M
@a
D=D+M
@SP
A=M
M=D
@SP
M=M+1

//sub
@SP
M=M-1
@SP
A=M
D=M
@a
M=D
@SP
M=M-1
@SP
A=M
D=M
@b
M=D
@b
D=M
@a
D=D-M
@SP
A=M
M=D
@SP
M=M+1

// push temp 6
// addr = 5 + segment_num
@5
D=A
@6
D=D+A
@addr
M=D
// *sp = *addr
@addr
A=M
D=M
@SP
A=M
M=D
// SP++
@SP
M=M+1

//add
@SP
M=M-1
@SP
A=M
D=M
@a
M=D
@SP
M=M-1
@SP
A=M
D=M
@b
M=D
@b
D=M
@a
D=D+M
@SP
A=M
M=D
@SP
M=M+1

