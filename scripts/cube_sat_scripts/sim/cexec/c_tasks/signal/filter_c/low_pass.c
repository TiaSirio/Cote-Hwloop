#include "filter.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>


void low_pass_filter(int nOfIter)
{
    printf("========= Band pass filter example =========\n\n");
    BWLowPass* filter = create_bw_low_pass_filter(4, 250, 2);
    for(int i = 0; i < nOfIter; i++){
        printf("Output[%d]:%f\n", i, bw_low_pass(filter, i* 100));
    }
    free_bw_low_pass(filter);
    printf("========= Done. =========\n\n");
}


int main(int argc, char* argv[]) {
    if (argc != 2) {
	printf("ERROR");
	return -1;
    }

    int nOfIter = atoi(argv[1]);
    low_pass_filter(nOfIter);
    return 0;
}
