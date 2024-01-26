// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//// Replace this comment with your code.

// screen memory map = [SCREEN,KBD] = [16384,24576]

//for(int j=0;j<256;j+=32){
//	for(int i=0;i<32;i++){
//      	sum = j + i
//		SCREEN[sum] = -1
//	}
//}

(MAIN)

// get keyboard
@KBD
D = M

// go to white if key is not pressed
@WHITE
D;JEQ

// col = -1 (black)
@col
M = -1

@P2
0;JMP

(WHITE)
// col = 0 (white)
@col
M = 0

(P2)
// i = 0
@i
M = 0

// j = 0
@j
M = 0

// D = SCREEN
@SCREEN
D = A

// address = SCREEN
@address
M = D

(LOOP2)
	// D = 256
	@256
	D = A

	// D = 256 - j
	@j
	D = D - M

    // if(D == 0) goto MAIN
	@MAIN
	D;JEQ

	// j = j + 1
	@j
	M = M + 1

	// i = 0
	@i
	M = 0

	(LOOP1)

		// D = 32
		@32
		D = A

		// D = 32 - i
		@i
		D = D - M

		// if(D == 0) goto LOOP2
		@LOOP2
		D;JEQ

		// D = color
		@col
		D = M

		// RAM[address] = color
		@address
		A = M
		M = D

		// i = i +1
		@i
		M = M + 1

		// address = address + 1
		@address
		M = M + 1

	// goto LOOP1
	@LOOP1
	0;JMP

@LOOP2
0;JMP

// infinite loop
//(END)
//@END
//0;JMP

