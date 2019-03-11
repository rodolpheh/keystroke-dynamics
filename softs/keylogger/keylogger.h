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

#define MAX_KBEVTS 2000

typedef struct _kbEvt {
    time_t seconds;
    long nsec;
    unsigned int code;
    int state;
} kbEvt;

/**
 * Save in-memory sample to a CSV file
 */
void exportToCSV();

/**
 * Print a kbEvt
 *
 * Utility function to print a kbEvt.
 */
void printkbEvt(kbEvt thekbEvt);

/**
 * Capture keylog sample
 */
void keylogSession();

/**
 * Replay a sample
 *
 * Emit the keyboard events sequence corresponding to a sample.
 * The events will correspond as closely as possible to the original
 * recorded sequence (release/press, press/release, etc).
 */
void replaySample(
    int kbEvtNb,
    kbEvt * loggedkbEvts);
