from stopword import stopwords
def tokenize(data):
    doc_token = []
    from konlpy.tag import Okt
    okt = Okt()
    for sentence in data:
        sentence = okt.morphs(sentence, stem=True)
        sentence = ' '.join(sentence)
        doc_token.append(sentence)
    return doc_token


def token_counter(data):
    from collections import Counter
    count = Counter()
    for sentence in data:
        count.update(sentence)  # string 일때는 .split()추가

    word_set = sorted(count, key=count.get, reverse=True)
    word_to_int = {word: ii for ii, word in enumerate(word_set, 1)}
    return word_to_int


def doc_seq_maker(word_to_int, doc_token, seq_length=100):
    mapped_review = []
    for sentence in doc_token:
        mapped_review.append([word_to_int[word] for word in sentence])  # string 일때는 .split()추가
    doc_sequence = np.zeros((len(mapped_review), seq_length), dtype=int)
    for i, row in enumerate(mapped_review):
        review_arr = np.array(row)
        try:
            doc_sequence[i, -len(row):] = review_arr[-seq_length:]
        except:
            pass

    return doc_sequence


def noun_adj_sent(review):
    sentences_tag = []
    for sentence in review:
        morph = okt.pos(sentence)
        sentences_tag.append(morph)

    adj_list = []
    for sentence1 in sentences_tag:
        sent = [word for word, tag in sentence1 if tag in ['Noun', 'Adjective']]
        adj_list.append(sent)

    return adj_list


def noun_adj_sent_word(sent):
    sentences_tag = []
    morph = okt.pos(sent)
    sentences_tag.append(morph)

    noun_adj_list = []
    for sentence1 in sentences_tag:
        sent = [word for word, tag in sentence1 if tag in ['Noun', 'Adjective']]
        noun_adj_list.append(sent)

    return noun_adj_list[0]


def sent_to_altseq(sent, word2vec, count, seq_length=100):
    sent_int = []

    for word in sent:
        if word in count:
            sent_int.append(count[word])
        elif word not in count:
            try:
                alternative = [t[0] for t in w2v_model.wv.most_similar(positive=[word], topn=100)]
                alter_word = [word for word in alternative if word in count]
                # print(f'{word} changed to {alter_word[0]}')
                sent_int.append(count[alter_word[0]])
            except:
                sent_int.append(0)
    doc_sequence = np.zeros(seq_length, dtype=int)
    doc_sequence[-len(sent_int):] = sent_int[:100]
    return doc_sequence


def review_process(review):
    from konlpy.tag import Okt
    okt = Okt()
    mapped_review = []
    review_p = []
    for sentence in review:
        try:
            sent = noun_adj_sent_word(sentence)
            mapped_review.append(sent_to_altseq(sent, w2v_model, naver_count).tolist())
            review_p.append(sentence)
        except:
            pass
    return mapped_review, review_p

def makeFeatureVec(review, model, num_features):
    featureVec = np.zeros((num_features,), dtype='float32')
    word_index = model.wv.index2word

    word_n = 0
    for word in review:
        if word in word_index:
            word_n += 1
            featureVec = np.add(featureVec, model[word])
    featureVec = np.divide(featureVec, word_n)
    return featureVec

def sentiment(new_sentence):
    line = okt.morphs(new_sentence, stem=True)
    sentence = ''
    classes = {0: '부정적', 1: '긍정적'}
    for word in line:
        if word not in stopwords:
            sentence += ' ' + word
    vec = makeFeatureVec(sentence, model, 100)
    val = []
    val.append(vec)

    return pipe.predict_proba(val)[0][0]