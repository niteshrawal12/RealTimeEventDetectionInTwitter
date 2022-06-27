import json
import re
import string
import timeit
import nltk
from nltk import tokenize
from nltk.chunk import ne_chunk
from nltk.corpus import stopwords
from nltk.corpus.reader import chunked
from nltk.stem import PorterStemmer,WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

complete_stopwords = set(stopwords.words("english"))
complete_stopwords.update(('n','gd','hmmm','yet','ur','u','ayu','ht','dis','dat','it3','yup','htt','amp','aka','herez','thats','cant','guyz'))

start = timeit.default_timer()
infp = open('/home/shubham/Desktop/project/code/ExtractData/RishabhPant.json','r')

lines = infp.readlines()
def preprocessing(tweet_text):
    tweet_text = tweet_text.replace("\n", " ").replace("\r", " ")
    tweet_text = tweet_text.replace('RT', "") # replace retweet
    tweet_text = tweet_text.lower()
    tweet_text = re.sub('((www\.[\s]+)|(https://[^\s]+)|(http.*[^\x00-\x7f]+[^\s]*))', "", tweet_text) #link
    # tweet_text = re.sub('#([^\s]+)', r'\1', tweet_text)  # removal of hash symbol from hashtags

    #tweet_text = re.sub('@[^\s]+', '', tweet_text) # removal of @user mentions
    #tweet_text = re.sub('[\s]+', ' ', tweet_text)  # removal of white space
    tweet_text = re.sub('([^\x00-\x7f]+)', "", tweet_text) #replace Non-ASCII characters
    
    #tweet_text = re.sub('\s+', ' ', tweet_text).strip()
    # nopunc = [char for char in tweet_text if char not in string.punctuation]
    # tweet_text = ''.join(nopunc)
    
    #tweet_text = tweet_text.translate(str.maketrans('#','#',string.punctuation))

    # tweet_text = tweet_text.translate(str.maketrans("m","R"), string.punctuation)

    

    #tweet_text = ("".join(pun for pun in tweet_text if pun not in  string.punctuation )).strip()
    tweet_text =re.sub('[^a-zA-Z0-9#\s]','',tweet_text).strip() #remove all punctuation from string except #
    #tweet_text = "".join(pun for pun in tweet_text if re.match(r'^#',tweet_text)).strip
    tweet_text = ' '.join([word for word in tweet_text.split() if word not in complete_stopwords])

    
    #removal of repeated words
    uni_words = tweet_text.split()
    tweet_text = ' '.join(sorted(set(uni_words), key=uni_words.index))
    ##########################
    tweet_text = re.sub(r'\d+', '', tweet_text) #removal of numbers
    tweet_text = ' '.join([w for w in tweet_text.split() if len(w) > 2]) #removal of words less than 2 characters
    return tweet_text

def returnhashtag(tweet_text):
    hashtag =re.findall(r"#(\w+)",tweet_text)
    return hashtag


def get_named_entity(tweet_text):
    chunked = ne_chunk(pos_tag(word_tokenize(tweet_text)))
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(' '.join([token for token, pos in i.leaves()]))
            if current_chunk:
                named_entity=' '.join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk.append(named_entity)
                    current_chunk =[]
            else:
                continue
    return continuous_chunk





def Lemmatize(t):
    tokens = word_tokenize(t)
    # print(tokens)
    #tokens_pos = pos_tag(tokens)
    # stemmer = PorterStemmer()
    lemmatiser = WordNetLemmatizer()
    ltweetl =[]
    for i in range(0,len(tokens)):
        ltweetl.append(lemmatiser.lemmatize(tokens[i],pos='v'))
    ltweet = " ".join(ltweetl)
    return ltweet

for i in range(0,len(lines)):
    if lines[i] not in ('\n','\r\n') :
        jtweet = json.loads(lines[i])
        created_time = jtweet["created_at"]
        if "id" in jtweet:
            tweet_id = jtweet["id"]
            # created_time = jtweet["id"]      #for creation time --------------
            user_id = jtweet["user"]["id_str"]
            tweet_text = jtweet["text"]
            pre_processed_tweet_text = preprocessing(tweet_text)
            hash_tag = returnhashtag(tweet_text)
            ner = get_named_entity(tweet_text)
            # processed_tweet_text = remove_adjectives(pre_processed_tweet_text)
            processed_tweet_text = Lemmatize(pre_processed_tweet_text)
            if processed_tweet_text:
                outfp = open('/home/shubham/Desktop/project/code/ProcessedData/RishabPant.txt','a', encoding="utf-8")                # outfp.write(str(created_at)+"\t")
                outfp.write(str(tweet_id)+"\t")
                outfp.write(str(user_id) + "\t")

                # outfp.write(created_time+"\t")
                outfp.write(processed_tweet_text+"\t")
                outfp.write(str(hash_tag)+"\t")
                outfp.write(str(ner)+"\n")
                # outfp.write(str(user_id) + "\t")
    else:
        continue

infp.close()
outfp.close()
stop = timeit.default_timer()
print("Total Execution time:", stop - start)
