// push constant 3030
//*sp=i
@3030
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// pop pointer 0
// SP--
@SP
M=M-1
// this/that = *sp
@SP
A=M
D=M
@THIS
M=D

// push constant 3040
//*sp=i
@3040
D=A
@SP
A=M
M=D
//*SP++
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

// push constant 32
//*sp=i
@32
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// pop this 2
// addr = segment_pointer + segment_num
@2
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

// push constant 46
//*sp=i
@46
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// pop that 6
// addr = segment_pointer + segment_num
@6
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

// push pointer 0
// *sp = this
@THIS
D=M
@SP
A=M
M=D
// SP++
@SP
M=M+1

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

// push this 2
// addr = segment_pointer + segment_num
@2
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

// push that 6
// addr = segment_pointer + segment_num
@6
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

