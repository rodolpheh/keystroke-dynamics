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

/**
 * Handle interrupt signals
 */
void intHandler(int dummy);

/**
 * Save in-memory sample to a CSV file
 */
void saveToFile();

/**
 * Print a sample
 *
 * Utility function to print a sample.
 */
void printSample(sample theSample);

/**
 * Replay a sample sequence
 *
 * Emit the keyboard events corresponding to a list of samples.
 * The events will correspond as closely as possible to the original
 * recorded sequence (release/press, press/release, etc).
 */
void replaySamples();

static sample samples[2000];
static struct timeval times[2000];
static int count = 0;
static int kbdFile;
