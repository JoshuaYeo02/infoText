#Help

help_message = "TEXT: [wikipedia (topic)] for information search. TEXT: [news] for news. TEXT: [exchange (currency)(currency)]"

#News

from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
message = ""
message_final_news = ""
class FrequencySummarizer:
  def __init__(self, min_cut=0.1, max_cut=0.9):
    """
     Initilize the text summarizer.
     Words that have a frequency term lower than min_cut 
     or higer than max_cut will be ignored.
    """
    self._min_cut = min_cut
    self._max_cut = max_cut 
    self._stopwords = set(stopwords.words('english') + list(punctuation))

  def _compute_frequencies(self, word_sent):
    """ 
      Compute the frequency of each of word.
      Input: 
       word_sent, a list of sentences already tokenized.
      Output: 
       freq, a dictionary where freq[w] is the frequency of w.
    """
    freq = defaultdict(int)
    for s in word_sent:
      for word in s:
        if word not in self._stopwords:
          freq[word] += 1
    # frequencies normalization and fitering
    m = float(max(freq.values()))
    for w in freq.keys():
      freq[w] = freq[w]/m
      if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
        del freq[w]
    return freq

  def summarize(self, text, n):
    """Return a list of n sentences which represent thxe summary of text."""
    sents = sent_tokenize(text)
    assert n <= len(sents)
    word_sent = [word_tokenize(s.lower()) for s in sents]
    self._freq = self._compute_frequencies(word_sent)
    ranking = defaultdict(int)
    for i,sent in enumerate(word_sent):
      for w in sent:
        if w in self._freq:
          ranking[i] += self._freq[w]
    sents_idx = self._rank(ranking, n)    
    return [sents[j] for j in sents_idx]

  def _rank(self, ranking, n):
    """ return the first n sentences with highest ranking """
    return nlargest(n, ranking, key=ranking.get)
import urllib2
from bs4 import BeautifulSoup

def get_only_text(url):
 """return the title and the text of the article at the specified url"""
 page = urllib2.urlopen(url).read().decode('utf8')
 soup = BeautifulSoup(page, "html.parser")
 text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
 return soup.title.text, text
feed_xml = urllib2.urlopen('http://feeds.bbci.co.uk/news/rss.xml').read()
feed = BeautifulSoup(feed_xml.decode('utf8'), "html.parser")
to_summarize = map(lambda p: p.text, feed.find_all('guid'))

fs = FrequencySummarizer()
for article_url in to_summarize[:2]:
  title, text = get_only_text(article_url)
  message = message + 'NEW ARTICLE:'
  message = message + title
  for s in fs.summarize(text, 2):
   message = message + s

#split string from output to phone
  
split_string = lambda x, n: [x[i:i+n] for i in range(0, len(x), n)]
message_final_news = split_string(message,90)
len_msg_news = len(message_final_news)
   
#Currency Exchange

def currencyexchange(original, final):
    from forex_python.converter import CurrencyRates
    c = CurrencyRates()
    z = c.get_rate(original, final)
    return z

#Wikipedia Search
  
def wikipedia(search):
    import wikipedia
    wiki_msg = search
    z = wikipedia.summary(wiki_msg, sentences=5)
    return z
  
#sending and reciving Message

from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse

app = Flask(__name__)

@app.route('/sms', methods=['POST'])

def sms():
    number = request.form['From']
    message_body = request.form['Body']
    resp = MessagingResponse()
    if message_body.lower() == "news":
      for i in range(0, len_msg_news):
        resp.message(message_final_news[i])
    if "wikipedia" in message_body.lower():
      x = message_body.lower()
      wiki = x.replace("wikipedia ","")
      split_string = lambda x, n: [x[i:i+n] for i in range(0, len(x), n)]
      wiki_message = split_string(wikipedia(wiki),90)
      len_msg_wiki = len(wiki_message)
      for i in range(0,len_msg_wiki):
        resp.message(wiki_message[i])
    if "exchange" in message_body.lower():
      split_string = lambda x, n: [x[i:i+n] for i in range(0, len(x), n)]
      msg = message_body.upper()
      msg = msg.replace('EXCHANGE', "")
      msg = msg.replace(' ','')
      currency = split_string(msg,3)
      x = currency[0]
      y = currency[1]
      amount = currencyexchange(x,y)
      amount_msg = str(amount)
      resp.message(amount_msg)
    if "support" in message_body.lower():
      resp.message(help_message)
    return str(resp)
if __name__ == '__main__':
    app.run()                
