import praw
import os
import time
import json

def slack(msg):
    if('BCWB_SLACK_URL' in os.environ.keys()): 
        SLACK_URL = os.environ['BCWB_SLACK_URL']
        command = os.popen('''curl -X POST -H 'Content-type: application/json' --data '{"text":"'''+msg+'''"}' '''+SLACK_URL)
        print(command.read())
        print(command.close())
    else:
        print("-No Slakc access-")
        print(msg)

def main():
    # Create the Reddit instance and login using ./praw.ini or ~/.config/praw.ini
    reddit = praw.Reddit('threadcreator')
    reddit.validate_on_submit = True

    # Get the top 20 values from our subreddit
    subreddit = reddit.subreddit('BuyCanadian')

    # This code will get you info about all your flair options
    # for temp in subreddit.flair.link_templates:
    #     print(json.dumps(temp, indent=2))

    post = subreddit.submit(
        "Weekly -In Search Of- Thread", 
        selftext="Looking for something Canadian-made, but you're worried it doesn't deserve its own thread? Post it here, any Thursday!", 
        flair_id="cd3ac86c-7e23-11e8-a564-0e214a49b15e" # Discussion Flair
    )

    # post.mod.approve()
    # post.mod.distinguish(sticky=True)

    for prov in PROVS:
        reply = post.reply(prov)
        # reply.mod.distinguish()

    slack(post.url)
    


if __name__ == "__main__":
    main()