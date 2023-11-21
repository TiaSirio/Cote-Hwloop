/**
* @file image_rgbtogray.c
* @brief C program to convert an RGB image to grayscale.
* @author Priya Shah
* @version v1
* @date 2018-01-10
*/
#include <stdio.h>
#include <time.h>
#include <string.h>

int main(int argc, char* argv[]){

    if (argc != 5) {
        printf("ERROR");
        return -1;
    }

	clock_t start, stop;

	start = clock();											// Note the start time for profiling purposes.

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

	int i,j,y;
	unsigned char byte[54];
	
	if(fIn==NULL)												// check if the input file has not been opened succesfully.
	{											
		printf("File does not exist.\n");
        return 1;
	}

	for(i=0;i<54;i++)											//read the 54 byte header from fIn
	{									
		byte[i] = getc(fIn);								
	}

	fwrite(byte,sizeof(unsigned char),54,fOut);					//write the header back

	// extract image height, width and bitDepth from imageHeader 
	int height = *(int*)&byte[18];
	int width = *(int*)&byte[22];
	int bitDepth = *(int*)&byte[28];

	printf("width: %d\n",width);
	printf("height: %d\n",height );

	int size = height*width;									//calculate image size

	unsigned char buffer[size][3];								//to store the image data
	
			
	for(i=0;i<size;i++)											//RGB to gray
	{
		y=0;
		buffer[i][2]=getc(fIn);									//blue
		buffer[i][1]=getc(fIn);									//green
		buffer[i][0]=getc(fIn);									//red
			
		y=(buffer[i][0]*0.3) + (buffer[i][1]*0.59)	+ (buffer[i][2]*0.11);			//conversion formula of rgb to gray

		putc(y,fOut);
		putc(y,fOut);
		putc(y,fOut);
	}
	
	fclose(fOut);
	fclose(fIn);

	stop = clock();
	printf("\nCLOCKS_PER_SEC = %ld\n",stop-start); 
	printf("%lf ms\n",((double)(stop-start) * 1000.0)/CLOCKS_PER_SEC );

    printf("%s", argv[4]);

	return 0;
}
