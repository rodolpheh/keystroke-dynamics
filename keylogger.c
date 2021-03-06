#include "keylogger.h"

void printKbEvt(kbEvt theKbEvt) {
    const char * state = theKbEvt.state == 2 ? "REPEATED" : (
        theKbEvt.state ? "PRESSED " : "RELEASED"
    );
    printf("%ld%09ld %03d %s\n", theKbEvt.seconds, theKbEvt.nsec, theKbEvt.code, state);
}

void replaySample(sample * mySample) {
    int kbEvtNb = mySample->sampleSize;
    kbEvt * loggedKbEvts = mySample->kbEvts;

    // Open keyboard device event
    int kbdFileHandle = open(
        "/dev/input/by-path/platform-i8042-serio-0-event-kbd", O_WRONLY
    );

    // Start timestamp for first event to write
    struct timeval startTime;
    gettimeofday(&startTime, NULL);
    int kbEvtCount = 0;

    while (kbEvtCount < kbEvtNb) {
        kbEvt keyEvt = loggedKbEvts[kbEvtCount];

        struct timeval endTime;
        gettimeofday(&endTime, NULL);

        // Reconstructing time deltas of input events to replay
        struct timeval timeDiff;
        if (kbEvtCount == 0) {
            timeDiff.tv_sec = 0;
            timeDiff.tv_usec = 0;
        } else {
            timeDiff.tv_sec =
            keyEvt.seconds - loggedKbEvts[kbEvtCount - 1].seconds;
            timeDiff.tv_usec =
            keyEvt.nsec - loggedKbEvts[kbEvtCount - 1].nsec;
        }

        // Control sequence
        long int endTimestamp =
            (endTime.tv_sec * 1000000) + endTime.tv_usec;
        long int startTimestamp =
            (startTime.tv_sec * 1000000) + startTime.tv_usec;
        long int diffTimestamp =
            (timeDiff.tv_sec * 1000000) + timeDiff.tv_usec;

        // Replay keyboard event if the time delta has been observed
        if (endTimestamp - startTimestamp > diffTimestamp) {
            struct input_event forcedKey;

            // Write key event to device event file
            forcedKey.type = EV_KEY;
            forcedKey.value = keyEvt.state;
            forcedKey.code = keyEvt.code;
            gettimeofday(&forcedKey.time, NULL);
            write(kbdFileHandle, &forcedKey, sizeof(struct input_event));

            // Add event separator to device event file (REQUIRED)
            forcedKey.type = EV_SYN;
            forcedKey.value = 0;
            forcedKey.code = 0;
            gettimeofday(&forcedKey.time, NULL);
            write(kbdFileHandle, &forcedKey, sizeof(struct input_event));

            // Save start time for next event
            gettimeofday(&startTime, NULL);
            kbEvtCount++;
        }
    }
    close(kbdFileHandle);
}

void keylogSession(sample * emptySample) {
    struct input_event ev;

    _Bool isRecording = true;

    int kbEvtNb = 0;

    // Opening keyboard input file
    int kbdFileHandle = open(
        "/dev/input/by-path/platform-i8042-serio-0-event-kbd", O_RDONLY
    );

    while(isRecording) {
        // Reading one event from input file
        read(kbdFileHandle, &ev, sizeof (struct input_event));

        // TODO: cannot record again. Must free previous memory and restart
        if (ev.type == EV_KEY) {
            if (isRecording && ev.code != KEY_ENTER) {

                // If the first event is a key release, discard it
                if (kbEvtNb == 0 && ev.value == EV_KEY_RELEASED) {
                } else {
                    kbEvt newKbEvt = { ev.time.tv_sec, ev.time.tv_usec, ev.code, ev.value};
                    emptySample->kbEvts[kbEvtNb].seconds = newKbEvt.seconds;
                    emptySample->kbEvts[kbEvtNb].nsec = newKbEvt.nsec;
                    emptySample->kbEvts[kbEvtNb].code = newKbEvt.code;
                    emptySample->kbEvts[kbEvtNb].state = newKbEvt.state;
                    kbEvtNb++;
                    // Fixed size array guard
                    if (kbEvtNb >= MAX_KBEVTS) {
                        printf("More than max kbEvts, killing it\n");
                        exit(1);
                    }
                }
            }

            // Control sequences for start / stop / replay
            if (ev.code == KEY_ENTER && ev.value == EV_KEY_PRESSED) {
                isRecording = isRecording ? false : true;
                if (!isRecording) {
                    emptySample->sampleSize = kbEvtNb;
                }
            }
        } // End if ev.type == EV_KEY. All other events are ignored

        fflush(stdout);
        fflush(stdin);
    } // End of while loop

    // TODO : close file sooner
    close(kbdFileHandle);
} // End of keylogSession() function

int main() {
    _Bool isExitRequired = false;
    struct input_event ev;

    printf("Keylogger program\nInsert menu interactions here\n");
    //kbEvt * kbEvts = (kbEvt * ) calloc(MAX_KBEVTS, sizeof(kbEvt));
    sample mySample;
    //mySample.kbEvts = kbEvts;

    printf(
        "Start sample capture session [Press enter when done with capture]\n"
    );
    keylogSession(&mySample);
    printf("Capture session ended\n");

    // Opening keyboard input file
    int kbdFileHandle = open(
        "/dev/input/by-path/platform-i8042-serio-0-event-kbd", O_RDONLY
    );
    while(!isExitRequired) {

        read(kbdFileHandle, &ev, sizeof (struct input_event));

        if (ev.code == KEY_F3 && ev.value == EV_KEY_PRESSED) {
                printf("Replaying\n");
                replaySample(&mySample);
                printf("\nReplay done\n");

        }
    }

    close(kbdFileHandle);
    return 0;
}