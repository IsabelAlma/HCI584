# Overview

This program is aimed at allowing the user to run an analysis on a given hashtaag using Twitter.


The program is run directly through either TwitterSent1 - Essential Version.ipynb or TwitterSent1 - GUI version.py in the downloaded code. Online connection is necessary to pull from Twitter.

# Modules Installation
Python v3.6 or newer
- python3 -m pip install tkinter
- python3 -m pip install tweepy
- python3 -m pip install textblob
- python3 -m pip install wordcloud
- python3 -m pip install pandas
- python3 -m pip install re
- python3 -m pip install matplotlib
- python3 -m pip install pylab

# User Flow Walkthrough

- Users opens program to the GUI showing a search bar
- User can type in a hashtag to search
- User clicks "Get Analysis" button to run the functions and create a thread of the most recent tweets, a barchart graph, and three wordclouds (for positive, negative, and neutral sentiment)
- When completed the user can press the "Quit" button to exit

# Code Flow Walkthrough

# TwitterSent1 - Essential Version.ipynb

Jupyter note book allowing user to see each working component. This is ran using the essential version of the Twitter API, which is free on dign up for Twitter Developer. 


# TwitterSent1 - GUI version.py

GUI version of program. This needs Elevated access of the Twitter API to run. This is still a free version, but requires an additional application. 

## GUI Layout

- Import Modules
- create default dataframe 'df' from Twitter
  - msgs = []
    msg =[]
    #set number of tweets to return
    for tweet in tweepy.Cursor(api.search_tweets, q=hash_name,lang='en').items(10):
        msg = [tweet.text] 
        msg = tuple(msg)                    
        msgs.append(msg)
- create visuals via wordcloud and figures for GUI


### Graph Functions

Displaying tweets from searched hashtag

    Label(f2, text=f"{df['Tweets']}%",justify=LEFT, wraplength=500,bg='#d5dde0').grid(row=5, column=1)

Pie Chart
    
    labels  = ['Positive ['+str(positive_per)+'%]' , 'Neutral ['+str(neutral_per)+'%]','Negative ['+str(negative_per)+'%]']
    ax.pie(sizes,colors=colors, startangle=90)
    ax.legend(labels)  
    chart1 = FigureCanvasTkAgg(fig,frameChartsPC)
    chart1.get_tk_widget().pack()

Wordcloud (here a function is created to call for the different sentiments creating three wordclouds)

    def create_wordcloud(text): 
        stopwords = set(STOPWORDS)
        wc = WordCloud(background_color="white", max_words=3000, stopwords=stopwords, repeat=False).generate(str(text))
        wc_f = Figure(figsize = (3, 3),dpi = 100) # create a figure object
        axes = wc_f.add_subplot()
        axes.imshow(wc)
        chart2 = FigureCanvasTkAgg(wc_f,frameChartsWC)
        chart2.get_tk_widget().pack()

### Known Issues

- Graphs are alligned to the left, ideally want centralized
- Currently, there is no way to remove previous graphs when ran. User must close out and rerun to have cleared view

### Future Work

- Centralize all graphs
- Have a refresh option
- Clean up GUI
- Allow more search options (such as userhandle or retweets)

### Ongoing Development

- All development is final at this time
