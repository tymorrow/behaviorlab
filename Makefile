SRCS = $(wildcard build/*/*.c)

PROGS = $(patsubst %.c,%,$(SRCS))

all: $(PROGS)

%: %.c

		$(CC) $(CFLAGS)  -o $@ $<
