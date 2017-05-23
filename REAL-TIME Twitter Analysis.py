from matplotlib import use
use("Agg")
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag
import matplotlib.pyplot as plt
from pylab import *
from bs4 import BeautifulSoup
import numpy as np
from nltk.stem import WordNetLemmatizer
import re
import pandas as pd
import time
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import re
import matplotlib.animation as manimation

consumer_key = '12345'
consumer_secret = '12345'
access_token = '123-12345'
access_secret = '12345'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

term='trump'
number_tweets=20

t=0
fig=plt.figure(figsize=(8,6))
ax1 = fig.add_subplot(1,1,1)

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Real-Time Analysis of Twitter Streaming', artist='Rubens Zimbres',
                comment='Real-Time Analysis of Twitter Streaming')
writer = FFMpegWriter(fps=2, metadata=metadata,bitrate=-1,codec="libx264",extra_args=['-pix_fmt', 'yuv420p'])

with writer.saving(fig, "Twitter_REAL_Time_40.mp4", 100):
    while t<20:
        t=t+1
        data=[]
        for status in tweepy.Cursor(api.search,q=term).items(number_tweets):
            try:
                URLless_string = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', status.text)
                data.append(URLless_string)
            except:
                pass
        
        lemmatizer = WordNetLemmatizer()
        
        text=data
        
        sentences = sent_tokenize(str(text))
        sentences2=sentences
        
        tokens = word_tokenize(str(text))
        tokens=[lemmatizer.lemmatize(tokens[i]) for i in range(0,len(tokens))]
        
        tagged_tokens = pos_tag(tokens)
        
        ## NOUNS
        text2 = word_tokenize(str(text))
        is_noun = lambda pos: pos[:2] == 'NN'
        b=nltk.pos_tag(text2)
        nouns = [word for (word, pos) in nltk.pos_tag(text2) if is_noun(pos)] 
        V = set(nouns)
        long_words1 = [w for w in tokens if 4<len(w) < 10]
        fdist01 = nltk.FreqDist(long_words1)
        a1=fdist01.most_common(40)
        
        
        def lexical_diversity(text):
            return len(set(text)) / len(text)
        
        
        vocab = set(text)
        vocab_size = len(vocab)
        
        
        V = set(text)
        long_words = [w for w in tokens if 4<len(w) < 13]
        
        text2 = nltk.Text(word.lower() for word in long_words)
        
        fdist1 = nltk.FreqDist(long_words)
        a=fdist1.most_common(15)
        
        import logging
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        import matplotlib.pyplot as plt
        from gensim import corpora
        from string import punctuation
        def strip_punctuation(s):
            return ''.join(c for c in s if c not in punctuation)
        
        documents=[strip_punctuation(re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '',sentences2[i])) for i in range(0,len(sentences2))]
        
        stoplist = set('for a of the and to in is the he she on i will it its us as that at who be '.split())
        texts = [[word for word in document.lower().split() if word not in stoplist]
            for document in long_words]
        # remove words that appear only once
        from collections import defaultdict
        frequency = defaultdict(int)
        
        for text in texts:
            for token in text:
                frequency[token] += 1
        
        texts = [[token for token in text if frequency[token] > 1]
            for text in texts]
        
        dictionary = corpora.Dictionary(texts)
        dictionary.save('/tmp/deerwester4.dict')
        
        ## VETOR DAS FRASES
        corpus = [dictionary.doc2bow(text) for text in texts]
        corpora.MmCorpus.serialize('/tmp/deerwester4.mm', corpus)  # store to disk, for later use
        
        from gensim import corpora, models, similarities
        tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
        
        
        corpus_tfidf = tfidf[corpus]
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
        corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
            
        ## COORDENADAS DOS TEXTOS
        todas=[]
        for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
            todas.append(doc)
        
        from gensim import corpora, models, similarities
        dictionary = corpora.Dictionary.load('/tmp/deerwester4.dict')
        corpus = corpora.MmCorpus('/tmp/deerwester4.mm') # comes from the first tutorial, "From strings to vectors"
        
        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
        
        
        p=[]
        for i in range(0,len(documents)):
            doc1 = documents[i]
            vec_bow2 = dictionary.doc2bow(doc1.lower().split())
            vec_lsi2 = lsi[vec_bow2] # convert the query to LSI space
            p.append(vec_lsi2)
            
        index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it
        
        index.save('/tmp/deerwester4.index')
        index = similarities.MatrixSimilarity.load('/tmp/deerwester4.index')
        
        #################
        
        import gensim
        import numpy as np
        import matplotlib.colors as colors
        import matplotlib.cm as cmx
        import matplotlib as mpl
        
        matrix1 = gensim.matutils.corpus2dense(p, num_terms=4)
        matrix3=matrix1.T
        
        from sklearn import manifold, datasets, decomposition, ensemble,discriminant_analysis, random_projection
        
        def norm(x):
            return (x-np.min(x))/(np.max(x)-np.min(x))
        
        X=norm(matrix3)
        
        tsne = manifold.TSNE(n_components=2, init='pca', random_state=0,perplexity=50,verbose=1,n_iter=1500)
        X_tsne = X
        
        ### WORK HERE - COMO DESCOBRI QUE TINHA 3 CLUSTERS ???? SORT X_tsne
        ## DEFINE K-MEANS
        from sklearn.cluster import KMeans
        model3=KMeans(n_clusters=4,random_state=0)
        model3.fit(X_tsne)
        cc=model3.predict(X_tsne)
        
        ## ALSO TRY COM X PARA VER QUE TOPICO SELECIONA
        
        tokens2 = word_tokenize(str(sentences2))
        
        tokens2=[lemmatizer.lemmatize(tokens2[i]) for i in range(0,len(tokens2))]
        
        long_words12 = [w for w in tokens2 if len(w) > 5]
        fdist012 = nltk.FreqDist(long_words12)
        a12=fdist012.most_common(5)
        
        from matplotlib.colors import LinearSegmentedColormap
        
        n_classes=4
        colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1),(0,0,0)] 
        cm = LinearSegmentedColormap.from_list(
                cc, colors, N=4)
        cor=[colors[cc[i]] for i in range(0,len(cc))]
        model = models.LdaModel(corpus, id2word=dictionary, num_topics=4)
        
        ### ACCUMULATE FEELINGS
        
        from nltk.sentiment import SentimentAnalyzer
        from nltk.sentiment.util import *
        from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia
        sentim=sia()
        
        cc0=[]
        for sentence in documents:
            cc0.append(sentim.polarity_scores(sentence))
        
        neu=[]
        neg=[]
        for sentence in documents:
                ss = sentim.polarity_scores(sentence)
                for k in sorted(ss):
                    neg.append(ss[k])
                    neu.append(k)
        
        f=int(len(neg)/4)
        sent0=np.array(neu).reshape(f,4)
        sent=np.array(neg).reshape(f,4)
        comp0=sent.T[0]
        comp=np.fliplr([comp0])[0]
        
        
        positivos=len(np.where(np.array(comp)>0)[0])
        neutros=len(np.where(np.array(comp)==0)[0])
        negativos=len(np.where(np.array(comp)<0)[0])
        time.sleep(1)
        x = np.arange(0, len(comp), 1)
        ax1.plot(np.cumsum(comp),linewidth=3,color='blue')
        ax1.fill_between(x,np.cumsum(comp),0,where=np.cumsum(comp)<0,facecolor='red',alpha=.7)
        ax1.fill_between(x,np.cumsum(comp),0,where=np.cumsum(comp)>0,facecolor='lawngreen',alpha=.7)
        ax1.annotate('POSITIVE',(140,1.5),fontweight='bold')
        ax1.annotate('NEGATIVE',(140,-3),fontweight='bold')
        writer.grab_frame()
        ax1.clear()
        time.sleep(1.5)        