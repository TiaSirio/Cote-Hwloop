CC=gcc

CFLAGS=-g

all: black_white image_bright image_dark image_rgbtogray image_rotate negative_image

black_white: black_white.c
	$(CC) $(CFLAGS) -o black_white black_white.c

image_bright: image_bright.c
	$(CC) $(CFLAGS) -o image_bright image_bright.c

image_dark: image_dark.c
	$(CC) $(CFLAGS) -o image_dark image_dark.c

image_rgbtogray: image_rgbtogray.c
	$(CC) $(CFLAGS) -o image_rgbtogray image_rgbtogray.c

image_rotate: image_rotate.c
	$(CC) $(CFLAGS) -o image_rotate image_rotate.c

negative_image: negative_image.c
	$(CC) $(CFLAGS) -o negative_image negative_image.c

.PHONY: clean
clean:
	rm -f black_white image_bright image_dark image_rgbtogray image_rotate negative_image
