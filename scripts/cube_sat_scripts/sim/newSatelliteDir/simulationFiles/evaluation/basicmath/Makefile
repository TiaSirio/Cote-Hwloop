FILE2 = basicmath_large.c   rad2deg.c  cubic.c   isqrt.c

all: basicmath_large

basicmath_large: ${FILE2} Makefile
	gcc -static -O3 -g ${FILE2} -o basicmath_large -lm

clean:
	rm -rf basicmath_large output*
