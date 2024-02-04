//bootstrap code
@256
D = A
@SP
M = D
// process function call Sys.init with args 0
// push return address label Sys.init_0
@Sys.init_0
D=A
@SP
A=M
M=D
@SP
M=M+1
//push LCL
@LCL
D=A
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=A
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=A
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=A
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
(Sys.init_0)

// function declaration Main.fibonacci with 0
(Main.fibonacci)

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

//lt
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
@L0
D;JGT
@1
D=A
@L1
0;JMP
(L0)
@0
D=A
(L1)
@SP
A=M
M=D
@SP
M=M+1

// if-goto @Main.fibonacci$N_LT_2
@SP
M=M-1
@SP
A=M
D=M
@Main.fibonacci$N_LT_2
A=M
D;JGT

//goto @Main.fibonacci$N_GE_2
@Main.fibonacci$N_GE_2
A=M
0;JMP

//label Main.fibonacci$N_LT_2
(Main.fibonacci$N_LT_2)

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

// process function return
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

//label Main.fibonacci$N_GE_2
(Main.fibonacci$N_GE_2)

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

// process function call Main.fibonacci with args 1
// push return address label Main.fibonacci_1
@Main.fibonacci_1
D=A
@SP
A=M
M=D
@SP
M=M+1
//push LCL
@LCL
D=A
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=A
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=A
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=A
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
@1
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Main.fibonacci
@Main.fibonacci
0;JMP
(Main.fibonacci_1)

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

// process function call Main.fibonacci with args 1
// push return address label Main.fibonacci_2
@Main.fibonacci_2
D=A
@SP
A=M
M=D
@SP
M=M+1
//push LCL
@LCL
D=A
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=A
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=A
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=A
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
@1
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Main.fibonacci
@Main.fibonacci
0;JMP
(Main.fibonacci_2)

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

// process function return
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

// function declaration Sys.init with 0
(Sys.init)

// push constant 4
//*sp=i
@4
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// process function call Main.fibonacci with args 1
// push return address label Main.fibonacci_3
@Main.fibonacci_3
D=A
@SP
A=M
M=D
@SP
M=M+1
//push LCL
@LCL
D=A
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=A
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=A
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=A
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
@1
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Main.fibonacci
@Main.fibonacci
0;JMP
(Main.fibonacci_3)

//label Sys.init$END
(Sys.init$END)

//goto @Sys.init$END
@Sys.init$END
A=M
0;JMP

