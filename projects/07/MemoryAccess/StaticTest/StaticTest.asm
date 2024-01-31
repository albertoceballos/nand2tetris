// push constant 111
//*sp=i
@111
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// push constant 333
//*sp=i
@333
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// push constant 888
//*sp=i
@888
D=A
@SP
A=M
M=D
//*SP++
@SP
M=M+1

// pop static 8
// SP-- 
@SP
M=M-1
// var = *sp
@SP
A=M
D=M
// set variable value
@StaticTest.vm.8
M=D

// pop static 3
// SP-- 
@SP
M=M-1
// var = *sp
@SP
A=M
D=M
// set variable value
@StaticTest.vm.3
M=D

// pop static 1
// SP-- 
@SP
M=M-1
// var = *sp
@SP
A=M
D=M
// set variable value
@StaticTest.vm.1
M=D

// push static 3
// get variable value
@StaticTest.vm.3
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
@StaticTest.vm.1
D=M
// *sp = var value
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

// push static 8
// get variable value
@StaticTest.vm.8
D=M
// *sp = var value
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

