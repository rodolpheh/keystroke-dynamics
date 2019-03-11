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
#include <stdbool.h>

#ifndef EV_KEY_PRESSED
#define EV_KEY_PRESSED 1
#endif

#ifndef EV_KEY_RELEASED
#define EV_KEY_RELEASED 0
#endif

#define MAX_KEY_EV_SAMPLES 2000

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
 *
 * 
 */
void replaySamples(
    int sampleNb,
    sample * loggedSamples,
    struct timeval * loggedTimes
    );
