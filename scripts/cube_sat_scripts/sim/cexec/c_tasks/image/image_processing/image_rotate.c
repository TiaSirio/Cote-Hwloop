/**
* @file image_rotate.c
* @brief C program to rotate the image by 180-degree. ( Flipping)
* @author Priya Shah
* @version v1
* @date 2018-01-10
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[])
{
	if (argc != 6) {
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

	int i,j,choice;
	unsigned char byte[54],colorTable[1024];
	
	if(fIn==NULL)											// check if the input file has not been opened succesfully.
	{											
		printf("File does not exist.\n");
        return 1;
	}

	for(i=0;i<54;i++)										//read the 54 byte header from fIn
	{									
		byte[i] = getc(fIn);								
	}

	fwrite(byte,sizeof(unsigned char),54,fOut);				//write the header back

	// extract image height, width and bitDepth from imageHeader 
	int height = *(int*)&byte[18];
	int width = *(int*)&byte[22];
	int bitDepth = *(int*)&byte[28];

	printf("width: %d\n",width);
	printf("height: %d\n",height );

	int size = height*width;								//calculate image size

	if(bitDepth <= 8)										//if ColorTable present, extract it.
	{
		fread(colorTable,sizeof(unsigned char),1024,fIn);
		fwrite(colorTable,sizeof(unsigned char),1024,fOut);
	}

	unsigned char buffer[width][height];					//to store the image data
	unsigned char out_buffer[width][height];

	fread(buffer,sizeof(unsigned char),size,fIn);			//read the image data

	//printf("Enter your choice :\n");
	//printf("1. Rotate right\n");
	//printf("2. Rotate left\n");
	//printf("3. Rotate 180\n");

	//scanf("%d",&choice);
	choice = atoi(argv[5]);


	switch(choice)												//to rotate image in 3 direction
	{												
		case 1:
			for(i=0;i<width;i++)								//to rotate right
			{
				for(j=0;j<height;j++)
				{
					out_buffer[j][height-1-i]=buffer[i][j];
				}
			}
			break;
		case 2:
			for(i=0;i<width;i++)								//to rotate left
			{
				for(j=0;j<height;j++)
				{
					out_buffer[j][i]=buffer[i][j];
				}
			}
			break;
		case 3:
			for(i=0;i<width;i++)								//to rotate 180 degree
			{
				for(j=0;j<height;j++)
				{
					out_buffer[width-i][j]=buffer[i][j];
				}
			}
			break;
		default:
			break;
	}
	
	fwrite(out_buffer,sizeof(unsigned char),size,fOut);		//write back to the output image

	fclose(fIn);
	fclose(fOut);

    printf("%s", argv[4]);

	return 0;
}
