import keylogger_api

if __name__ == "__main__":

    print("Start sample collecting program")

    collected_sample = keylogger_api.keylog_session()

    # Loop to replay evts with the help of the library
    # Empty stdin from previous keystrokes
    input();
    res = "rubbishplaceholder"
    while(res[-1] is not "n"):
        res = input("Do you want to replay ? [y/n] ")

        while(res[-1] is not "y" and res[-1] is not "n"):
            res = input(
                "It is a yes or no question really... "
                + "Do you want to replay ? [y/n] "
            )

        if (res[-1] is "y"):
            keylogger_api.replay_sample(collected_sample)
            # Add newline char
            print("")

    print("Exiting program")