from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import urllib
from bs4 import BeautifulSoup

class FrequencySummarizer:
  def __init__(self, min_cut=0.1, max_cut=0.9):

    self._min_cut = min_cut
    self._max_cut = max_cut 
    self._stopwords = set(stopwords.words('english') + list(punctuation))

  def _compute_frequencies(self, word_sent):

    freq = defaultdict(int)
    for s in word_sent:
      for word in s:
        if word not in self._stopwords:
          freq[word] += 1
    # frequencies normalization and fitering
    m = float(max(freq.values()))
    for w in list(freq):
      freq[w] = freq[w]/m
      if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
        del freq[w]
    return freq

  def summarize(self, text, n):
    """
      Return a list of n sentences 
      which represent the summary of text.
    """
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

def get_only_text_url(url):
    
    page = urllib.request.urlopen(url).read().decode('utf8')
    # we download the URL
    soup = BeautifulSoup(page, "html5lib")
    
    text = ' '.join(map(lambda p: p.text, soup.find_all('article')))
    
    soup2 = BeautifulSoup(page, "html5lib")
    # find all the paragraph tage <p>
    text = ' '.join(map(lambda p: p.text, soup2.find_all('p')))
    return [soup.title.text, text]

textOfUrl = get_only_text_url("https://cloud.google.com/appengine/docs/standard/python/getting-started/python-standard-env")
fs = FrequencySummarizer()
# we instantiate the frequency summarizer class and get an object of this class

summary = fs.summarize(textOfUrl[1], 10)
print(textOfUrl[0])
print(summary)
#print (get_only_text_url("https://www.washingtonpost.com/powerpost/shutdown-looms-as-senate-democrats-dig-in-against-gop-spending-plan/2018/01/19/f4370868-fccd-11e7-a46b-a3614530bd87_story.html"))

