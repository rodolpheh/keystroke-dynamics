#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <linux/input.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>
#include <string.h>
#include <time.h>
#include <linux/input-event-codes.h>

typedef struct _sample {
    time_t seconds;
    long nsec;
    unsigned int code;
    int state;
} sample;

void intHandler(int dummy);
void saveToFile();
void printSample(sample theSample);

static int keepRunning = 1;
static sample samples[2000];
static struct timeval times[2000];
static int count = 0;
static int kbdFile;
