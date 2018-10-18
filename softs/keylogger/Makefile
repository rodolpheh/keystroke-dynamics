CC=gcc
CFLAGS=-c -Wall -pedantic -Wextra
LDFLAGS=
EXEC=keylogger

all: $(EXEC)

keylogger: keylogger.o
	$(CC) $(LDFLAGS) $^ -o $@

%.o: %.c
	$(CC) $(CFLAGS) $<

clean:
	rm -rf *.o
