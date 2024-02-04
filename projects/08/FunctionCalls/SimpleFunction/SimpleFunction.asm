(SimpleFunction.test)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
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

// push local 1
// addr = segment_pointer + segment_num
@1
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

//not
// sp--
@SP
M=M-1
// d=*sp
@SP
A=M
D=M
D=!D
@SP
A=M
M=D
@SP
M=M+1

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

@LCL
D=M
@end_frame
M=D
@end_frame
D = M
@5
D = D - A
A = D
D = M
@ret_address
M = D
@SP
M = M - 1
A = M
D = M
@ARG
A = M
M = D
@ARG
D = M + 1
@SP
M = D
@end_frame
D = M - 1
A = D
D = M
@THAT
M = D
@end_frame
D = M
@2
D = D - A
A = D
D = M
@THIS
M = D
@end_frame
D = M
@3
D = D - A
A = D
D = M
@ARG
M = D
@end_frame
D = M
@4
D = D - A
A = D
D = M
@LCL
M = D
@ret_address
A = M
0;JMP

