import praw
import datetime
import random
import time
from keep_alive import keep_alive
REPLY_MESSAGES = ["feliz dia de la torta /u/{}!  [esp]🍰",
                  "bonne journée de gâteau /u/{}! 🍰 [fr]",
                  "幸せなケーキの日 /u/{}! 🍰  [jap]",
                  ".... .- .--. .--. -.-- / -.-. .- -.- . / -.. .- -.- /u/{}! 🍰",
                  "蛋糕日快乐 /u/{}! 🍰  [chn]",
                  "buona giornata della torta /u/{}! 🍰 [it]",
                  "beatus crustulam diem /u/{}! 🍰  [latin]",
                  "fröhlicher Kuchentag /u/{}! 🍰  [gr]",
                  "diwrnod cacen hapus /u/{}! 🍰  [wel]",
                  "fijne taartdag /u/{}! 🍰  [dut]",
                  "हैप्पी केक डे /u/{}! 🍰  [hin]",
                  "šťastný tortový deň /u/{}! 🍰  [slo]",
                  "χαρούμενη μέρα τούρτας /u/{}! 🍰  [greek]",
                  "szczęśliwy dzień ciasta /u/{}! 🍰  [pol]",
                  "mutlu pasta günü /u/{}! 🍰  [tur]",
                  "يوم كعكة سعيد /u/{}! 🍰  [arab]",
                 ]

def authenticate():
  print("Authenticating...")
  reddit=praw.Reddit(
    username = 'cakeday___bot',
    password = '',
    client_id = '',
    client_secret = '',
    user_agent = "CakeDay Bot"
  )
  return reddit

def main():
    reddit = authenticate()
    congratulated_users = get_congratulated_users()

    remove_downvoted_comments(reddit)
    run_bot(reddit, congratulated_users)


def run_bot(reddit, congratulated_users):
    current_date = datetime.datetime.today().strftime('%y/%m/%d')
    print("Getting comments...")
    subreddit = reddit.subreddit("gaming+aww+pics+worldnews+music+movies+food+asksciece+jokes+gifs+wtf+Whatcouldgowrong+nextfuckinglevel+cars+facepalm+formula1+formuladank+valorant+askreddit+bettafish+abruptchaos+absoluteunits+damnthatisinteresting+f1technical+hyderabad+linustechtips+natureisfuckinglit+natureismetal+mademesmile+meme+memes+nonononoyes+pcmasterrace+perfectlycutscreams+samsung+animals+space+dogs+cats")
    for comment in subreddit.comments(limit=999999999999999999999999999999999999999999999999999999999999999999999):
        
        account_created_date = datetime.datetime.fromtimestamp(int(comment.author.created)).strftime('%y/%m/%d')
        if comment.author not in congratulated_users:
          if current_date != account_created_date \
                  and current_date[3:] == account_created_date[3:] :
              print("Cake day found! " + comment.author)
              try:
                comment.reply(random.choice(REPLY_MESSAGES).format(comment.author))
              except Exception as e:
                e=str(e)
                res = [int(i) for i in e.split() if i.isdigit()]
                print("sleeping for "+ str(res[0]+2)+" minutes")
                time.sleep(60*(res[0]+2))
                comment.reply(random.choice(REPLY_MESSAGES).format(comment.author))
                print("woke up and replied to the comment " + comment.author)
              congratulated_users.append(comment.author)
              with open("congratulated_users.txt", "a") as file:
                  file.write("{}\n".format(comment.author.name))
    


def get_congratulated_users():
    with open("congratulated_users.txt", "r") as file:
        return file.read().split("\n")


def remove_downvoted_comments(reddit):
    print("Checking for comments with negative karma")

    for comment in reddit.redditor("cakeday___bot").comments.new(limit=20):
        print("Comment Score: {}".format(comment.score))
        if comment.score <= 0:
            print("Deleting comment...")
            comment.delete()

keep_alive()
if __name__ == "__main__":
    main()
