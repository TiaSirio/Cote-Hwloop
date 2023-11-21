/******************************************************************************
Written and Copyright (C) by Dirk Klose
and the EmSec Embedded Security group of Ruhr-Universitaet Bochum.
All rights reserved.

Contact lightweight@crypto.rub.de for comments & questions.
This program is free software; You may use it or parts of it or
modifiy it under the following terms:

(1) Usage and/or redistribution and/or modification of the software
or parts of the software is permitted for non-commercial use only.

(2a) If this software or parts are used as part of a new software, you
must license the entire work, as a whole, under this License to anyone
who comes into possession of a copy. This License will therefore
apply, to the whole of the work, and all its parts, regardless of how
they are packaged.

(2b) You may expand this license by your own license. In this case this
license still applies to the software as mentioned in (2a) and must
not be changed. The expansion must be clearly recognizable as such. In
any case of collision between the license and the expansion the
license is superior to the expansion.

(3) If this software or parts are used as part of a new software, you
must provide equivalent access to the source code of the entire work,
as a whole, to anyone who comes into possession of a copy, in the same
way through the same place at no further charge, as for the binary
version.

(4) This program is distributed in the hope that it will be useful,
but   WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
(5) These notices must be retained in any copies of any part of this
documentation and/or software.

(6) If this software is used credit must be given to the
"Embedded Security Group of Ruhr-Universitaet Bochum, Germany" as
the authors of the parts of the software used. This can be in the form
of a textual message at program startup or  at *beginning* of the
documentation (online or textual) provided with the package.

If you are interested in a commercial use
please contact '''lightweigth@crypto.rub.de'''
******************************************************************************/

/*
Algorithm: PRESENT6480
Hardening technique: duplicated variables (T4)
Details:
  - each variable is duplicated and every modification of the original variable
    is performed on its duplicate.
  - in the end of each block the original and its duplicate values are compared
*/


// Include-file
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

void error(int linenumber) {
	fprintf(stderr, "HARDERR T4 The algorithm failed to execute properly on %d line\n", linenumber);
  exit(-1);
}

void encryption(uint8_t *plaintext, uint8_t *plaintext_copy, volatile uint8_t *state, volatile uint8_t *state_copy, uint8_t *key, uint8_t *key_copy) {
	const uint8_t sBox4[] =	{0xc,0x5,0x6,0xb,0x9,0x0,0xa,0xd,0x3,0xe,0xf,0x8,0x4,0x7,0x1,0x2};
	const uint8_t sBox4_copy[] =	{0xc,0x5,0x6,0xb,0x9,0x0,0xa,0xd,0x3,0xe,0xf,0x8,0x4,0x7,0x1,0x2};
	//	Counter
	uint8_t i = 0;
  uint8_t i_copy = 0;
	//	pLayer variables
	uint8_t position = 0;
  uint8_t position_copy = 0;
	uint8_t element_source = 0;
  uint8_t element_source_copy = 0;
	uint8_t bit_source = 0;
  uint8_t bit_source_copy = 0;
	uint8_t element_destination	= 0;
	uint8_t element_destination_copy	= 0;
	uint8_t bit_destination	= 0;
	uint8_t bit_destination_copy	= 0;
	uint8_t temp_pLayer[8];
	uint8_t temp_pLayer_copy[8];
	//	Key scheduling variables
	uint8_t round;
	uint8_t round_copy;
	uint8_t save1;
	uint8_t save1_copy;
	uint8_t save2;
	uint8_t save2_copy;

	//	****************** Set up state **************************
  for(i=0;i<8;i++) {
			if (i!=i_copy) error(96);
      state[i] = plaintext[i];
			state_copy[i_copy] = plaintext_copy[i_copy];
			if (plaintext[i]!=plaintext_copy[i_copy]) error(99);
      i_copy++;
  }
  if (i!=i_copy) error(102);
	i = 0;
  i_copy = 0;
	//	****************** Encryption **************************
	round=0;
  round_copy=0;
	while(round<31) {
		//	****************** addRoundkey *************************
		i = 0;
		i_copy = 0;
		while(i<=7) {
			if (i!=i_copy) error(113);
			state[i] = state[i] ^ key[i+2];
			state_copy[i_copy] = state_copy[i_copy] ^ key_copy[i_copy+2];
			if (state[i]!=state_copy[i_copy]) error(116);
			if (key[i]!=key_copy[i_copy]) error(117);
			i++;
      i_copy++;
		}
    if (i!=i_copy) error(121);

		//	****************** sBox ********************************
		while(i>0) {
      if (i!=i_copy) error(125);
			i--;
      i_copy--;
			state[i] = sBox4[state[i]>>4]<<4 | sBox4[state[i] & 0xF];
			state_copy[i_copy] = sBox4_copy[state_copy[i_copy]>>4]<<4 | sBox4_copy[state_copy[i_copy] & 0xF];
			if (state[i]!=state_copy[i_copy]) error(130);
		}
    if (i!=i_copy) error(132);

		i_copy = 0;
		//	****************** pLayer ******************************
		for(i=0;i<8;i++) {
			if (i!=i_copy) error(137);
			temp_pLayer[i] = 0;
      temp_pLayer_copy[i_copy] = 0;
      i_copy++;
		}
    if (i!=i_copy) error(142);

    i_copy = 0;
		for(i=0;i<64;i++)	{
			position = (16*i) % 63;			//Artithmetic calculation of the pLayer
			position_copy = (16*i_copy) % 63;			//Artithmetic calculation of the pLayer
      if ((i!=i_copy) || (position!=position_copy)) error(148);
			if(i == 63) {									//exception for bit 63
				position = 63;
        position_copy = 63;
      }
			element_source		= i / 8;
      element_source_copy = i_copy / 8;
      if ((i!=i_copy) || (element_source!=element_source_copy)) error(155);
			bit_source 			= i % 8;
			bit_source_copy	= i_copy % 8;
      if ((i!=i_copy) || (bit_source!=bit_source_copy) ) error(158);
			element_destination	= position / 8;
			element_destination_copy = position_copy / 8;
      if ((position!=position_copy) || (element_destination!=element_destination_copy)) error(161);
			bit_destination 	= position % 8;
			bit_destination_copy 	= position_copy % 8;
      if ((position!=position_copy) || (bit_destination!=bit_destination_copy)) error(164);
			temp_pLayer[element_destination] |= ((state[element_source]>>bit_source) & 0x1) << bit_destination;
			temp_pLayer_copy[element_destination_copy] |= ((state_copy[element_source_copy]>>bit_source_copy) & 0x1) << bit_destination_copy;
      if ((element_destination!=element_destination_copy) || (bit_destination!=bit_destination_copy)
          || (element_source!=element_source_copy)
          || (temp_pLayer[element_destination]!=temp_pLayer_copy[element_destination_copy])) error(169);
      i_copy++;
		}

    if ((i!=i_copy) || (position!=position_copy) || (element_source!=element_source_copy)
      || (bit_source!=bit_source_copy) || (element_destination!=element_destination_copy)
      || (bit_destination!=bit_destination_copy)
      || (temp_pLayer[element_destination]!=temp_pLayer_copy[element_destination_copy])) error(176);

    i_copy = 0;
		for(i=0;i<=7;i++)	{
			state[i] = temp_pLayer[i];
			state_copy[i_copy] = temp_pLayer_copy[i_copy];
      if (i!=i_copy) error(182);
			if (state[i]!=state_copy[i_copy]) error(183);
      i_copy++;
		}
    if (i!=i_copy) error(186);

		//	****************** End pLayer **************************
		//	****************** Key Scheduling **********************
		save1  = key[0];
		save1_copy = key[0];
		save2  = key[1];
		save2_copy  = key[1];
		i = 0;
    i_copy = 0;
		while(i<8) {
			if (i!=i_copy) error(197);
			key[i] = key[i+2];
			key_copy[i] = key_copy[i_copy+2];
			if (key[i]!=key_copy[i_copy]) error(200);
			i++;
      i_copy++;
		}
    if (i!=i_copy) error(204);

		key[8] = save1;
		key[9] = save2;
		key_copy[8] = save1_copy;
		key_copy[9] = save2_copy;
    if ((save1!=save1_copy) || (save2!=save2_copy)) error(210);
		i = 0;
    i_copy = 0;
		save1 = key[0] & 7;	//61-bit left shift
		save1_copy = key_copy[0] & 7;	//61-bit left shift
		while(i<9) {
			key[i] = key[i] >> 3 | key[i+1] << 5;
			key_copy[i_copy] = key_copy[i_copy] >> 3 | key_copy[i_copy+1] << 5;
			if (key[i]!=key_copy[i_copy]) error(218);
			i++;
      i_copy++;
      if (i!=i_copy) error(221);
		}
    if (i!=i_copy) error(223);

		key[9] = key[9] >> 3 | save1 << 5;
		key_copy[9] = key_copy[9] >> 3 | save1_copy << 5;
    if (save1!=save1_copy) error(227);
		if (key[9]!=key_copy[9]) error(228);

		key[9] = sBox4[key[9]>>4]<<4 | (key[9] & 0xF);	//S-Box application
		key_copy[9] = sBox4_copy[key_copy[9]>>4]<<4 | (key_copy[9] & 0xF);	//S-Box application

		if (key[9]!=key_copy[9]) error(233);

		if((round+1) % 2 == 1)	//round counter addition
			key[1] ^= 128;
		if ((round_copy+1) % 2 == 1)
			key_copy[1] ^= 128;
		key[2] = ((((round+1)>>1) ^ (key[2] & 15)) | (key[2] & 240));
		key_copy[2] = ((((round_copy+1)>>1) ^ (key_copy[2] & 15)) | (key_copy[2] & 240));
		if (key[2]!=key_copy[2]) error(241);
		//	****************** End Key Scheduling ******************
		round++;
    round_copy++;
	}
  if ((round!=round_copy) || (i!=i_copy)) error(246);
	//	****************** addRoundkey *************************
	i = 0;
  i_copy = 0;
	while(i<=7) {		//final key XOR
		if (i!=i_copy) error(251);
		state[i] = state[i] ^ key[i+2];
		state_copy[i_copy] = state_copy[i_copy] ^ key_copy[i_copy+2];
		if (state[i]!=state_copy[i_copy]) error(254);
		i++;
    i_copy++;
	}
  if (i!=i_copy) error(258);
	//	****************** End addRoundkey *********************
	//	****************** End Encryption  **********************
}

int main(int argc, char *argv[]){

	if (argc<3) {
		fprintf(stderr, "ERROR: Wrong number of arguments\n");
	  exit(-1);
	}

	uint8_t key[10];	// 10 bytes = 80 bits
	uint8_t key_copy[10];	// 10 bytes = 80 bits
	uint8_t plaintext[8];	// 8 bytes = 64 bits
	uint8_t plaintext_copy[8];	// 8 bytes = 64 bits

	uint8_t i = 0, k = 0, t = 0;
	uint8_t i_copy = 0, k_copy = 0, t_copy = 0;

	// read 20 characters of key in hex (first argument)
	for (k = 0; k < 10; k++) {
    sscanf(&argv[1][k * 2], "%2hhx", &key[k]);
    sscanf(&argv[1][k_copy * 2], "%2hhx", &key_copy[k_copy]);
    if (k!=k_copy) error(282);
    k_copy++;
  }

  if ((k!=k_copy) || (key[k-1]!=key_copy[k_copy-1])) error(286);

	// read 16 characters of plaintext in hex (second argument)
	for (t = 0; t < 8; t++) {
    sscanf(&argv[2][t * 2], "%2hhx", &plaintext[t]);
    sscanf(&argv[2][t_copy * 2], "%2hhx", &plaintext_copy[t_copy]);
    if (t!=t_copy) error(292);
    t_copy++;
  }
  if ((t!=t_copy) || (plaintext[t-1]!=plaintext_copy[t_copy-1])) error(295);

	// Input values
	volatile uint8_t state[] = {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00};
	volatile uint8_t state_copy[] = {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00};

	encryption(plaintext, plaintext_copy, state, state_copy, key, key_copy);

	i = 0;
  i_copy = 0;
	while (i < 8) {
		//	****************** BEGIN PRINTING FOR DEBUG *********************
		printf("0x%02x ",state[i]);
    if (i!=i_copy) error(308);
		if (state[i]!=state_copy[i_copy]) error(309);
		if (plaintext[i]!=plaintext_copy[i_copy]) error(310);
		i++;
    i_copy++;
	}
  if (i!=i_copy) error(314);
	//	****************** END PRINTING FOR DEBUG *********************
	printf("\n");
	return 0;
}
