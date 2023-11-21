#include "filter.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>


void high_pass_filter(int nOfIter)
{
    printf("========= Band pass filter example =========\n\n");
    BWHighPass* filter = create_bw_low_pass_filter(4, 250, 45);
    for(int i = 0; i < nOfIter; i++){
        printf("Output[%d]:%f\n", i, bw_high_pass(filter, i* 100));
    }
    free_bw_high_pass(filter);
    printf("========= Done. =========\n\n");
}


int main(int argc, char* argv[]) {
    if (argc != 2) {
	printf("ERROR");
	return -1;
    }

    int nOfIter = atoi(argv[1]);
    high_pass_filter(nOfIter);
    return 0;
}
