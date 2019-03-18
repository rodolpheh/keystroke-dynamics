from keylogger import Sample, keylog_session, replay_sample

if __name__ == "__main__":

    print("Start sample collecting program")

    collected_sample = keylog_session()

    # Loop to replay evts with the help of the library
    # Empty stdin from previous keystrokes
    sample_str = input();

    res = "rubbishplaceholder"
    while(res[-1] is not "n"):
        print("Typed string:  \"{}\"".format(sample_str))
        print(collected_sample)
        res = input("Do you want to retake ? [y/n] ")

        while(res[-1] is not "y" and res[-1] is not "n"):
            res = input(
                "It is a yes or no question really... "
                + "Do you want to retake ? [y/n] "
            )

        if (res[-1] is "y"):
            collected_sample = keylog_session()
            sample_str = input()
            # Add newline char
            # print("")

    print("Exiting program")