# Buy Canadian Thread Creator (thread-creator)


This is a Reddit bot that creates weekly threads on [/r/BuyCanadian](https://www.reddit.com/r/BuyCanadian/)

To install and run the Thread-Creator you need have [git](https://git-scm.com/downloads), [python3](https://www.python.org/downloads/), and [pip3](https://vgkits.org/blog/pip3-windows-howto/) installed (these are all included in Mac dev-tools but will need to be added manually on Windows).

Open your command terminal in the directory in which you would like to Ocwa and clone the repo.
```
git clone https://github.com/ourcanadian/wiki-replier.git
```

Enter the repo and install the neccassary libraries.
```
cd thread-creator
pip3 install -r requirements.txt
```

In order to get to the good stuff, you will need the API Token and login info, which are kept private to prevent security risks. These things are only ever stored in local `praw.ini` files. Request the `praw.ini` content from an admin or via rylancole@ourcanadian.ca. Once you have the content, create a `praw.ini` file in the `thread-creator/` directory, and don't worry `.gitignore` will make sure you don't push the `praw.ini` file up to github. That would be trouble.

Now you can run the bot from within the directory giving it a key to access the post metadata
```
python3 main.py KEY
```

---

## How does the bot message slack?

It won't from your local instance unless you have a Slack web hook saved as an eviroment variable named `BCWB_SLACK_URL`
