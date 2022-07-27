'''
Project made possible by following the guides:
- https://developer.twitter.com/en/docs/twitter-api/v1
- https://www.tweepy.org/
- https://datascienceparichay.com/article/python-get-data-from-twitter-api-v2/
- https://towardsdatascience.com/step-by-step-twitter-sentiment-analysis-in-python-d6f650ade58d
- https://towardsdatascience.com/twitter-sentiment-analysis-in-python-1bafebe0b566
- https://github.com/yogeshnile/Twitter-Sentiment-Analysis-on-Python-GUI
- https://paulnelson.ca/posts/install-virtual-env-ipykernel-jupyter
- https://www.pythontutorial.net/tkinter/tkinter-matplotlib/
- https://blog.teclado.com/tkinter-scrollable-frames/
'''

# Import Libraries

#GUI
from tkinter import *
from tkinter import ttk
# Tweepy - Python library for accessing the Twitter API.
import tweepy
# TextBlob - Python library for processing textual data
from textblob import TextBlob
# WordCloud - Python linrary for creating image wordclouds
from wordcloud import WordCloud, STOPWORDS 
# Pandas - Data manipulation and analysis library
import pandas as pd
# Regular Expression Python module
import re
# Matplotlib - plotting library to create graphs and charts
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# Settings for Matplotlib graphs and charts
from pylab import rcParams
rcParams['figure.figsize'] = 12, 8

#Start of GUI
root = Tk()

#Title of Gui
root.title("Twitter Sentiment Analysis")

banner = Frame(root, padx=5, pady=5, bg='#A8B9BF')
banner.pack()
heding = Label(banner, text="Twitter Sentiment Analysis", font="Arial 20 bold")
heding.pack()

root.geometry("625x600")

#================Scrollbar Area Begin===================#

frame = Frame(root)
canvas=Canvas(frame,width=525,height=500,bg='#A8B9BF')
scrollbar =Scrollbar(frame,orient=VERTICAL,command=canvas.yview)
scrollable_frame = Frame(canvas,bg='#A8B9BF')
scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

#================Scrollbar Area End ===================#


#================User Input Part Begin ===================#

input_frame = Frame(scrollable_frame,padx=0,pady=30,bg='#A8B9BF')
input_frame.pack(anchor="w")

input_frame1 = Frame(scrollable_frame,padx=0,pady=0, bg="yellow")
input_frame1.pack()

hash_value = StringVar()
hashtag = Label(input_frame, text="Enter phrase to search with # :- ",font="comicsansms 10 bold", padx=30,bg='#A8B9BF').grid(row=4, column=1)
hashinput = Entry(input_frame, textvariable=hash_value).grid(row=4, column=2)

label=Label(scrollable_frame, text="", font=("Courier 22 bold"),bg='#A8B9BF')
label.pack()

#================User Input Part End ===================#


#================Sentiment Part Begin===================#.
f1 = Frame(scrollable_frame,padx=15,pady=14)
f1.pack()

f2 = Frame(scrollable_frame,padx=15,pady=14)
f2.pack(anchor="w")

error = Label(f1, text="Please enter any one", fg="red")
error2 = Label(f1, text="Both entry not valid", fg="red")

#================Sentiment Part End===================#
po = Label(f2, text="Positive:-",padx=15)
na = Label(f2, text="Negative:-",pady=5,padx=15)
nt = Label(f2, text="Neutral:-",padx=15)
df_L = Label(f2, text=f"")

#for pie chart
frameChartsPC = Frame(scrollable_frame)
frameChartsPC.pack(anchor="w")

#for wordcloud
frameChartsWC = Frame(scrollable_frame)
frameChartsWC.pack(anchor="w")

    #============================Insert here twitter API keys===========================
    
def r_twitterApiKey():
    config = pd.read_csv("config.csv")
    twitterApiKey = config['consumer_key'][0]
    return twitterApiKey
def r_twitterApiSecret():
    config = pd.read_csv("config.csv")
    twitterApiSecret = config['consumer_secret'][0]
    return twitterApiSecret
def r_twitterApiAccessToken():
    config = pd.read_csv("config.csv")
    twitterApiAccessToken = config['access_token'][0]
    return twitterApiAccessToken
def r_twitterApiAccessTokenSecret():
    config = pd.read_csv("config.csv")
    twitterApiAccessTokenSecret = config['access_secret'][0]
    return twitterApiAccessTokenSecret
    #============================End twitter API keys section===========================

def click():  
    hash_name = hash_value.get()
    string= hash_value.get()
    label.configure(text=string)

    # Authenticate
    auth = tweepy.OAuthHandler(r_twitterApiKey(), r_twitterApiSecret())
    auth.set_access_token(r_twitterApiAccessToken(), r_twitterApiAccessTokenSecret())
    api = tweepy.API(auth)
    
    if hash_name == "":
        error.grid_remove()
        global number
        if number > 1:
            po.grid_remove()
            na.grid_remove()
            nt.grid_remove()
    msgs = []
    msg =[]
    #set number of tweets to return
    for tweet in tweepy.Cursor(api.search_tweets, q=hash_name,lang='en').items(10):
        msg = [tweet.text] 
        msg = tuple(msg)                    
        msgs.append(msg)
     

    def cleanTxt(text):
        text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
        text = re.sub('#', '', text) # Removing '#' hash tag
        text = re.sub('RT[\s]+', '', text) # Removing RT
        text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
        return text
    df = pd.DataFrame(msgs)
    df['Tweets'] = df[0].apply(cleanTxt)
    df.drop(0, axis=1, inplace=True)
    
    #calculate the subjectivity and polarity of tweets.
    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity
    def getPolarity(text):
        return TextBlob(text).sentiment.polarity
    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
    df['Polarity'] = df['Tweets'].apply(getPolarity)
    
    # negative, nautral, positive analysis
    def getAnalysis(score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'
 
    #getting percentages from results
    df['Analysis'] = df['Polarity'].apply(getAnalysis)
    positive = df.loc[df['Analysis'].str.contains('Positive')]
    negative = df.loc[df['Analysis'].str.contains('Negative')]
    neutral = df.loc[df['Analysis'].str.contains('Neutral')]

    positive_per = round((positive.shape[0]/df.shape[0])*100, 1)
    negative_per = round((negative.shape[0]/df.shape[0])*100, 1)
    neutral_per = round((neutral.shape[0]/df.shape[0])*100, 1)
    number +=1

    #show tweets
    Label(f2, text=f"{df['Tweets']}%",justify=LEFT, wraplength=500,bg='#d5dde0').grid(row=5, column=1)
   
    #assign to pie chart. 
    fig = Figure(figsize = (3, 3),dpi = 100) # create a figure object
    ax = fig.add_subplot(111) # add an Axes to the figure
    sizes = [positive_per, neutral_per, negative_per]
    colors = ['green','blue','red']
    labels  = ['Positive ['+str(positive_per)+'%]' , 'Neutral ['+str(neutral_per)+'%]','Negative ['+str(negative_per)+'%]']
    ax.pie(sizes,colors=colors, startangle=90)
    ax.legend(labels)  
    chart1 = FigureCanvasTkAgg(fig,frameChartsPC)
    chart1.get_tk_widget().pack()

    #Function to Create Wordcloud
    def create_wordcloud(text): 
        stopwords = set(STOPWORDS)
        wc = WordCloud(background_color="white", max_words=3000, stopwords=stopwords, repeat=False).generate(str(text))
        wc_f = Figure(figsize = (3, 3),dpi = 100) # create a figure object
        axes = wc_f.add_subplot()
        axes.imshow(wc)
        chart2 = FigureCanvasTkAgg(wc_f,frameChartsWC)
        chart2.get_tk_widget().pack()
        #plt.show()

    #Creating wordcloud for all tweets
    create_wordcloud(positive.values)

    #Creating wordcloud for positive sentiment
    create_wordcloud(negative.values)

    #Creating wordcloud for positive sentiment
    create_wordcloud(neutral.values)

    
frame.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

#Begin
number=0
button = Button(input_frame1,text="Get Analysis", command=click, fg="blue",height = 1, width = 15)
button.grid(row=1, column=1)

# Function for closing window
exit_button = Button(root, text="Quit", command=root.destroy).pack()


mainloop()