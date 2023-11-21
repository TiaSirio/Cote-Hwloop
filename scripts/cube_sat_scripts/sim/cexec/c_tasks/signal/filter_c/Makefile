CC=gcc

CFLAGS = -Wall -Wshadow -O3 -g -march=native
LDFLAGS = -lm

TARGETS = low_pass high_pass band_pass band_stop

SRCS_L = low_pass.c filter.c
OBJS_L = $(SRCS_L:.c=.o)

SRCS_H = high_pass.c filter.c
OBJS_H = $(SRCS_H:.c=.o)

SRCS_BP = band_pass.c filter.c
OBJS_BP = $(SRCS_BP:.c=.o)

SRCS_BS = band_stop.c filter.c
OBJS_BS = $(SRCS_BS:.c=.o)

all: $(TARGETS)

$(TARGETS): $(OBJS_L) $(OBJS_H) $(OBJS_BP) $(OBJS_BS)
	$(CC) -o low_pass $(OBJS_L) $(LDFLAGS)
	$(CC) -o high_pass $(OBJS_H) $(LDFLAGS)
	$(CC) -o band_pass $(OBJS_BP) $(LDFLAGS)
	$(CC) -o band_stop $(OBJS_BS) $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -f $(OBJS_L) $(OBJS_H) $(OBJS_BP) $(OBJS_BS) $(TARGETS)
