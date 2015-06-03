#!/usr/bin/python

from twitch import *
import os
import configparser
import subprocess

configpath = os.path.expanduser("~") + "/.pytwitch"
config = configparser.ConfigParser()
config.read(configpath)

try:
    config.add_section("Twitch Account")
except configparser.DuplicateSectionError:
    pass

try:
    twitch = TwitchTV()

    username = ""

    while len(username) == 0:
        try:
            username = sys.argv[1]
            print("Using username " + username)
            break
        except IndexError:
            pass

        try:
            username = config["Twitch Account"]["username"]
            break
        except (KeyError) as e:
            print("No preconfigured username.")
            pass

        username = input("Enter username : ")
        config["Twitch Account"]["username"] = username
        with open(configpath, 'w') as configfile:
            config.write(configfile)   


    following = []

    try:
        following = twitch.getFollowingStreams(username)
        
    except TwitchException:
        print("Invalid username. Exiting.")
        config.remove_section("Twitch Account")
        with open(configpath, 'w') as configfile:
            config.write(configfile)
        quit()

    

    following = following['live']

    if len(following) == 0:
        print("No streams are live. Exiting.")
        quit()

    print("")
    print("Please select a stream:")

    count = 0
    for f in following:
        stream = f['channel']['name']
        displayName = " " * 10 + "[" + str(count) + "]"
        if count == 0:
            displayName = displayName[:9] + '*' + displayName[10:]
        displayName += " " + stream
        print(displayName + " playing: " + f['game'])
        count += 1

    selection = 0
    streamName = ""

    while True:
        newSel = input("Selection [0] or stream name: ")
    
        if len(newSel) == 0:
            streamName = following[selection]['channel']['name']
            break
        try :
            selection = int(newSel)
            streamName = following[selection]['channel']['name']
            break
        except (IndexError) as e:
            print("Please enter a valid number or stream")
        except ValueError:
            streamName = newSel
            break

    print("Launching " + streamName + " stream...")

    try:
        subprocess.Popen(["mpv","--really-quiet", twitch.getLiveStream(streamName, 0), "--title=" + streamName])
        subprocess.Popen(["chromium", "--app=http://twitch.tv/" + streamName + "/chat?popout="])
    except IndexError:
        print("No stream selected. Exiting.")
    except TwitchException:
        print("Stream offline. Exiting.")

except KeyboardInterrupt:
    print("")
    print("Received keyboard interrupt. Exiting.")
    quit()
