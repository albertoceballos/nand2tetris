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

// function declaration Main.fibonacci with 0
(Main.fibonacci)

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

// process lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LESS_THAN_1
D;JLT
D=0
@END_1
0;JEQ
(LESS_THAN_1)
D=-1
(END_1)
@SP
A=M
M=D
@SP
M=M+1

// if-goto @Main.fibonacci$N_LT_2
@SP
M=M-1
A=M
D=M
@Main.fibonacci$N_LT_2
D;JNE

//goto @Main.fibonacci$N_GE_2
@Main.fibonacci$N_GE_2
0;JMP

//label Main.fibonacci$N_LT_2
(Main.fibonacci$N_LT_2)

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

//label Main.fibonacci$N_GE_2
(Main.fibonacci$N_GE_2)

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

// process function call Main.fibonacci with args 1
// push return address label Main.fibonacci_ret_2
@Main.fibonacci_ret_2
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
(Main.fibonacci_ret_2)

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

// process function call Main.fibonacci with args 1
// push return address label Main.fibonacci_ret_3
@Main.fibonacci_ret_3
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
(Main.fibonacci_ret_3)

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
// push return address label Main.fibonacci_ret_4
@Main.fibonacci_ret_4
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
(Main.fibonacci_ret_4)

//label Main.fibonacci$END
(Main.fibonacci$END)

//goto @Main.fibonacci$END
@Main.fibonacci$END
0;JMP

