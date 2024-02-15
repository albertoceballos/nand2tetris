//bootstrap code
@256
D = A
@SP
M = D
// process function call Sys.init with args 0
// push return address label Sys.init_ret_0
@Sys.init_ret_0
D=A
@SP
A=M
M=D
@SP
M=M+1
//push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP - 5 - num_args
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Sys.init
@Sys.init
0;JMP
(Sys.init_ret_0)

// function declaration Class1.set with 0
(Class1.set)

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

// pop static 0
// SP-- 
@SP
M=M-1
// var = *sp
A=M
D=M
// set variable value
@Class1.0
M=D

// push argument 1
// addr = segment_pointer + segment_num
@1
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

// pop static 1
// SP-- 
@SP
M=M-1
// var = *sp
A=M
D=M
// set variable value
@Class1.1
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

// process function return
@LCL
D=M
@end_frame
M=D
@5
D=D-A
A=D
D=M
@ret_address
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@end_frame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@end_frame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@end_frame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@end_frame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@ret_address
A=M
0;JMP

// function declaration Class1.get with 0
(Class1.get)

// push static 0
// get variable value
@Class1.0
D=M
// *sp = var value
@SP
A=M
M=D
// SP++
@SP
M=M+1

// push static 1
// get variable value
@Class1.1
D=M
// *sp = var value
@SP
A=M
M=D
// SP++
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

// process function return
@LCL
D=M
@end_frame
M=D
@5
D=D-A
A=D
D=M
@ret_address
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@end_frame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@end_frame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@end_frame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@end_frame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@ret_address
A=M
0;JMP

// function declaration Class2.set with 0
(Class2.set)

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

// pop static 0
// SP-- 
@SP
M=M-1
// var = *sp
A=M
D=M
// set variable value
@Class2.0
M=D

// push argument 1
// addr = segment_pointer + segment_num
@1
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

// pop static 1
// SP-- 
@SP
M=M-1
// var = *sp
A=M
D=M
// set variable value
@Class2.1
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

// process function return
@LCL
D=M
@end_frame
M=D
@5
D=D-A
A=D
D=M
@ret_address
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@end_frame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@end_frame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@end_frame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@end_frame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@ret_address
A=M
0;JMP

// function declaration Class2.get with 0
(Class2.get)

// push static 0
// get variable value
@Class2.0
D=M
// *sp = var value
@SP
A=M
M=D
// SP++
@SP
M=M+1

// push static 1
// get variable value
@Class2.1
D=M
// *sp = var value
@SP
A=M
M=D
// SP++
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

// process function return
@LCL
D=M
@end_frame
M=D
@5
D=D-A
A=D
D=M
@ret_address
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@end_frame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@end_frame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@end_frame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@end_frame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@ret_address
A=M
0;JMP

// function declaration Sys.init with 0
(Sys.init)

// push constant 6
//*sp=i
@6
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// push constant 8
//*sp=i
@8
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// process function call Class1.set with args 2
// push return address label Class1.set_ret_1
@Class1.set_ret_1
D=A
@SP
A=M
M=D
@SP
M=M+1
//push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP - 5 - num_args
@SP
D=M
@5
D=D-A
@2
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Class1.set
@Class1.set
0;JMP
(Class1.set_ret_1)

// pop temp 0
// addr = 5 + segment_num
@5
D=A
@0
D=D+A
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

// push constant 23
//*sp=i
@23
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// push constant 15
//*sp=i
@15
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// process function call Class2.set with args 2
// push return address label Class2.set_ret_2
@Class2.set_ret_2
D=A
@SP
A=M
M=D
@SP
M=M+1
//push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP - 5 - num_args
@SP
D=M
@5
D=D-A
@2
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Class2.set
@Class2.set
0;JMP
(Class2.set_ret_2)

// pop temp 0
// addr = 5 + segment_num
@5
D=A
@0
D=D+A
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

// process function call Class1.get with args 0
// push return address label Class1.get_ret_3
@Class1.get_ret_3
D=A
@SP
A=M
M=D
@SP
M=M+1
//push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP - 5 - num_args
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Class1.get
@Class1.get
0;JMP
(Class1.get_ret_3)

// process function call Class2.get with args 0
// push return address label Class2.get_ret_4
@Class2.get_ret_4
D=A
@SP
A=M
M=D
@SP
M=M+1
//push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP - 5 - num_args
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Class2.get
@Class2.get
0;JMP
(Class2.get_ret_4)

//label END
(END)

//goto @END
@END
0;JMP

