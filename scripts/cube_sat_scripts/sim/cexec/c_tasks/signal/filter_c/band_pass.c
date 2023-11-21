#include "filter.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

void band_pass_filter(int nOfIter)
{
    printf("========= Band pass filter example =========\n\n");
    BWBandPass* filter = create_bw_band_pass_filter(4, 250, 2, 45);
    for(int i = 0; i < nOfIter; i++){
        printf("Output[%d]:%f\n", i, bw_band_pass(filter, i* 100));
    }
    free_bw_band_pass(filter);
    printf("========= Done. =========\n\n");
}


int main(int argc, char* argv[]) {
    if (argc != 2) {
	printf("ERROR");
	return -1;
    }

    int nOfIter = atoi(argv[1]);
    band_pass_filter(nOfIter);
    return 0;
}
