// push constant 0
//*sp=i
@0
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

//label LOOP
(LOOP)

// push argument 0
// addr = segment_pointer + segment_num
@0
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

// push argument 0
// addr = segment_pointer + segment_num
@0
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

// push constant 1
//*sp=i
@1
D=A
@SP
A=M
M=D
//*SP++
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

// pop argument 0
// addr = segment_pointer + segment_num
@0
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

// push argument 0
// addr = segment_pointer + segment_num
@0
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

// if-goto @LOOP
@SP
M=M-1
@SP
A=M
D=M
@LOOP
D;JGT

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

