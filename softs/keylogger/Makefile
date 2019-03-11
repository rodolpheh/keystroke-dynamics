BIN = keylogger.bit

SRCS = keylogger.c

OBJS = $(SRCS:.c=.o)
DEPS = $(SRCS:.c=.d)

CC = gcc

CFLAGS = -Wshadow -Wall -pedantic -Wextra -g -O3 -flto -march=native

LDLIBS = -lm

LDFLAGS =

dll : keylogger.c Makefile
	$(CC) $(CFLAGS) -shared -Wl,-soname,keylogger -o keylogger.so -fPIC keylogger.c

$(BIN): $(OBJS) $(DEPS)
	$(CC) $(OBJS) $(LDFLAGS) $(LDLIBS) -o $(BIN)

%.o : %.c %.d Makefile
	$(CC) $(CFLAGS) -MMD -MP -MT $@ -MF $*.d -c $<

-include *.d

%.d : ;

.PHONY: clean

clean:
	rm -f $(BIN) $(OBJS) $(DEPS)
