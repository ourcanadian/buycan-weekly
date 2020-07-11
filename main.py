import praw
import os
import time
import json
import sys

WEEKLY_POST = "3d13b4c2-ba2d-11ea-abe0-0e79786e34f5"

POST_TEMPLATES = {
    "provinces": {
        "title": "Monday Reccomendation Thread", 
        "selftext": "Hello r/BuyCanadian!  \n\nHere's your weekly thread to recommend your favourite Canadian businesses in your province or territory. Find your location below and reply with the best your area has to offer.  \n\nIf you see room for improvement on our weekly posts, please message the mod team.", 
        "flair_id": WEEKLY_POST,
        "replyList": [
            "Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Northwest Territories", "Nova Scotia", "Nunuvat", "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan", "Yukon"
        ],
        "modRules": [
            "approve", "distinguish", "distinguish_comments", "sticky"
        ]
    },
    "iso": {
        "title": "Thursday 'In Search Of' Thread", 
        "selftext": "Hello r/BuyCanadian!  \n\nHere's your weekly thread to comment what you have been looking for, but just can't seem to find. If your search doesn't need its own post, or has been posted before without luck, this is the thread for you!  \n\nIf you see room for improvement on our weekly posts, please message the mod team.", 
        "flair_id": WEEKLY_POST,
        "modRules": [
            "approve", "distinguish", "sticky"
        ]
    },
    "mega_topic": {
        "title": "Friday MegaThread for ", 
        "selftext": "Hello r/BuyCanadian!  \n\nHere's your weekly thread to recommend your favourite Canadian products related to this week's topic!  \n\nIf you see room for improvement on our weekly posts, please message the mod team.", 
        "flair_id": WEEKLY_POST,
        "replyList": [
            "Reply to this comment with suggestions for a future Friday Megathread topic!"
        ],
        "modRules": [
            "approve", "distinguish", "distinguish_comments", "sticky", "sticky_comments"
        ],
        "varFile": "./var-files/mega_topic.json"
    }, 
    "none": {

    }
}

def slack(msg):
    if('BCWB_SLACK_URL' in os.environ.keys()): 
        SLACK_URL = os.environ['BCWB_SLACK_URL']
        command = os.popen('''curl -X POST -H 'Content-type: application/json' --data '{"text":"'''+msg+'''"}' '''+SLACK_URL)
        print(command.read())
        print(command.close())
    else:
        print("-No Slack access-")
        print(msg)

def updateMeta(meta):
    with open(meta['varFile']) as json_file:
        variables = json.load(json_file)
        if(not variables): return False
    var = variables.pop()
    meta['title'] += var
    with open(meta['varFile'], 'w') as json_file:
        json_file.write(json.dumps(variables, indent=1))
    return True

def submitPost(subreddit, key):
    '''
    Add a post object into the POST_TEMPLATES list to be called by a KEY

    python3 main.py KEY

    The object MUST include a title (String), self text (String), and flair_id (String).
    You may also include a replyList (List: String) for comments to append to the post.
    You may also include a modRules (List: String) for mod commands, such as:
        [approve, distinguish, distinguish_comments, sticky, sticky_comments]
    '''

    useModRules = True
    if('-nomod' in key):
        useModRules = False
        key = key[:-6]

    meta = POST_TEMPLATES[key]

    if('varFile' in meta.keys()):
        success = updateMeta(meta)
        if(not success): 
            print("Error loading variables")
            return

    post = subreddit.submit(
        meta['title'],
        selftext=meta['selftext'],
        flair_id=meta['flair_id']
    )

    dist_comments = False
    sticky_comments = False

    if(useModRules and 'modRules' in meta.keys()):
        rules = meta['modRules']
        if('approve' in rules): post.mod.approve()
        if('distinguish' in rules): post.mod.distinguish()
        if('sticky' in rules): post.mod.sticky()

        dist_comments = 'distinguish_comments' in rules
        sticky_comments = 'sticky_comments' in rules

    replyList = meta['replyList'] if ('replyList' in meta.keys()) else []
    for reply in replyList:
        comment = post.reply(prov)
        if(dist_comments): comment.mod.distinguish()
        if(sticky_comments): comment.mod.sticky()

    slack(post.url)

def main(key):
    # Create the Reddit instance and login using ./praw.ini or ~/.config/praw.ini
    reddit = praw.Reddit('threadcreator')
    reddit.validate_on_submit = True

    # Get our subreddit
    subreddit = reddit.subreddit('BuyCanadian')

    # This code will get you info about all your flair options
    # for temp in subreddit.flair.link_templates:
    #     print(json.dumps(temp, indent=2))

    submitPost(subreddit, key)    


if __name__ == "__main__":

    key = None
    options = POST_TEMPLATES.keys()

    if(len(sys.argv) > 1):
        key = sys.argv[1]
        
    if(key and (key in options or (len(key) > 6) and key[:-6] in options)):
        main(key)
    else:
        print("------")
        print("Missing or incorrect arguement")
        print("python3 main.py KEY")
        print("Where KEY is one of", options)
        print("------")