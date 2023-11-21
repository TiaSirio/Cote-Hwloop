CC=gcc

LDFLAGS=-lm

mandelbrot_set: mandelbrot_set.c
	$(CC) -g -o mandelbrot_set mandelbrot_set.c $(LDFLAGS)

.PHONY: clean
clean:
	rm -f mandelbrot_set
