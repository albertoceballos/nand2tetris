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

// pop pointer 1
// SP--
@SP
M=M-1
// this/that = *sp
@SP
A=M
D=M
@THAT
M=D

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

// pop that 0
// addr = segment_pointer + segment_num
@0
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

// pop that 1
// addr = segment_pointer + segment_num
@1
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

// push constant 2
//*sp=i
@2
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

// if-goto @COMPUTE_ELEMENT
@SP
M=M-1
@SP
A=M
D=M
@COMPUTE_ELEMENT
D;JGT

//goto @END
@END
0;JMP

//label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)

// push that 0
// addr = segment_pointer + segment_num
@0
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

// push that 1
// addr = segment_pointer + segment_num
@1
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

// push pointer 1
// *sp = this
@THAT
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

// pop pointer 1
// SP--
@SP
M=M-1
// this/that = *sp
@SP
A=M
D=M
@THAT
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

//goto @LOOP
@LOOP
0;JMP

//label END
(END)

