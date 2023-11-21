/**
* @file black_white.c
* @brief C program to convert image to pure black and white, without using any libraries.
* @author Priya Shah
* @version v1
* @date 2018-01-10
*/
#include <stdio.h>
#include <string.h>
#define THRESHOLD 128
#define WHITE 255
#define BLACK 0

int main(int argc, char* argv[]){

    if (argc != 5) {
        printf("ERROR");
        return -1;
    }

    char datasetAddress[100];
    datasetAddress[0] = '\0';
    strcat(datasetAddress, argv[1]);
    strcat(datasetAddress, argv[3]);

    char resultAddress[100];
    resultAddress[0] = '\0';
    strcat(resultAddress, argv[2]);
    strcat(resultAddress, argv[4]);

	FILE *fIn = fopen(datasetAddress,"r");				//Input File name
	FILE *fOut = fopen(resultAddress,"w+");		            //Output File name

	int i;
	unsigned char byte[54];								//to get the image header
	unsigned char colorTable[1024];						//to get the colortable

	if(fIn==NULL)										// check if the input file has not been opened succesfully.
	{										
		printf("File does not exist.\n");
        return 1;
	}

	for(i=0;i<54;i++)									//read the 54 byte header from fIn
	{									
		byte[i]=getc(fIn);								
	}

	fwrite(byte,sizeof(unsigned char),54,fOut);			//write the header back

	// extract image height, width and bitDepth from imageHeader 
	int height = *(int*)&byte[18];
	int width = *(int*)&byte[22];
	int bitDepth = *(int*)&byte[28];

	printf("width: %d\n",width);
	printf("height: %d\n",height );

	int size=height*width;								//calculate image size

	if(bitDepth<=8)										//if ColorTable present, extract it.
	{
		fread(colorTable,sizeof(unsigned char),1024,fIn);
		fwrite(colorTable,sizeof(unsigned char),1024,fOut);
	}

	unsigned char buffer[size];							//to store the image data

	fread(buffer,sizeof(unsigned char),size,fIn);		//read image data

	for(i=0;i<size;i++)									//store 0(black) and 255(white) values to buffer 
		{
			buffer[i] = (buffer[i] > THRESHOLD) ? WHITE : BLACK;
		}
	
	fwrite(buffer,sizeof(unsigned char),size,fOut);		//write back to the output image

	fclose(fIn);
	fclose(fOut);

    printf("%s", argv[4]);

	return 0;
}
