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
A=D+M
// *sp = *addr
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
A=D+M
// *sp = *addr
D=M
@SP
A=M
M=D
// SP++
@SP
M=M+1

// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
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
A=D+M
// *sp = *addr
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

// sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
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
A=D+M
// *sp = *addr
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
A=M
D=M
@LOOP
D;JNE

// push local 0
// addr = segment_pointer + segment_num
@0
D=A
@LCL
A=D+M
// *sp = *addr
D=M
@SP
A=M
M=D
// SP++
@SP
M=M+1

