// R2 = R0 * R1
// R0 and R1 hold the values to multiply

// r2 = 0
//while(r0>=0){
//r2 += r1;
//r0--;
//}


@R2 // get RAM[2]
M=0 // RAM[2] = 0

(LOOP)
@R0 // get RAM[0]
D=M-1 // D=RAM[0]
M=D

@END
D;JLT

@R2 // get RAM[2]
D=M // D = RAM[2]

@R1 // get RAM[1]
D=D+M // RAM[2] = RAM[2] + RAM[1]

@R2 // get RAM[2]
M=D // store value in RAM[2]

@LOOP
0;JMP // go to LOOP

(END) 
@END
0;JMP // infinite loop



