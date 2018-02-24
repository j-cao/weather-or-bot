import praw
import config
import time
import os

# insert applicable information in config
def bot_login():
    print("Logging in")
    r = praw.Reddit(username = config.username,
        password = config.password,
        client_id = config.client_id,
        client_secret = config.client_secret,
        user_agent = “weather_or_bot”)
    print("Logged in!")

    return r

def run_bot(r, comments_replied_to):
    print("obtaining last 50 comments...")

    # in the last 50 comments of the subreddit ‘Houston’
    for comment in r.subreddit("Houston").comments(limit=50):

        # search for the string “weather” to comment with the current weather and traffic conditions
        if "weather" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
            print("String with \"route\" found!! " + comment.id)
            comment.reply(
                “For current conditions, check out:”
                "[Rain Gauge Map](https://www.harriscountyfws.org/), "
                "[Road Conditions](http://traffic.houstontranstar.org/layers/layers_ve.aspx?&inc=true&rc=true), "
                "[Base Reflectivity Map](http://weather.cod.edu/satrad/nexrad/index.php?type=HGX-N0Q-1-12#)")


            print("Replied to comment " + comment.id)

            # add to list to avoid replying to same comments
            comments_replied_to.append(comment.id)
            comments_replied_to = list(comments_replied_to)


            with open ("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")

    print("Sleeping for 10 seconds")
    # Sleep for 10 seconds
    time.sleep(600)

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
            comments_replied_to = []
    else:
            with open("comments_replied_to.txt", "r") as f:
                comments_replied_to = f.read()
                comments_replied_to = comments_replied_to.split("\n")
                comments_replied_to = filter(None, comments_replied_to)

    return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
print(comments_replied_to)

while True:
    run_bot(r, comments_replied_to)