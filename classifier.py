from req import s, News
import pickle
from math import log
from nltk.tokenize import wordpunct_tokenize
from nltk.stem.snowball import EnglishStemmer
from nltk import pos_tag


class Model:
    def __init__(self):
        self.words = {}
        self.classes = {'never': 0, 'maybe': 0, 'good': 0}
        self.stemmer = EnglishStemmer()

    def train(self, list):
        for piece in rows:
            label = piece.label
            word_list = self.__word_transfrom(piece.title)
            author = piece.author.lower()
            url = piece.url.lower()
            if label is not None:
                self.__add_vals(word_list, author, url, label)
        self.__to_freq()

    def save(self, filename):
        f = open(filename, 'wb')
        pickle.dump(self.words, f)

    def load(self, filename):
        try:
            f = open(filename, 'rb')
            self.words = pickle.load(f)
        except:
            print('Model loading error')

    def predict(self, piece):
        w_list = self.__word_transfrom(piece.title)
        w_list += [piece.author.lower()]
        w_list += [piece.url.lower()]
        probas = {}
        for label in self.classes.keys():
            probas[label] = self.classes[label]
        for word in w_list:
            if word not in self.words.keys():
                continue
            for label in self.classes.keys():
                probas[label] += self.words[word][label]
        return probas

    def classify(self, piece):
        probas = self.predict(piece)
        answer = 'never'
        min = probas['never']
        for key in probas.keys():
            if probas[key] >= min:
                min = probas[key]
                answer = key
        return answer

    def __word_transfrom(self, sentence):
        word_list = sentence.lower()
        word_list = wordpunct_tokenize(word_list)
        word_list = [word for word in word_list if self.__word_check(word)]
        word_list = [self.stemmer.stem(w) for w in word_list]
        return word_list

    def __word_check(self, word):
        tag = pos_tag([word])
        if tag[0][1] in \
            ('DT', 'EX', 'IN', 'LS', 'RP', 'TO', 'WDT', 'WP', 'WRB', 'CC') \
                or not tag[0][1].isalpha():
            return False
        return True

    def __add_vals(self, w_list, author, url, label):
        w_list.append(author)
        w_list.append(url)
        self.classes[label] += 1
        for word in w_list:
            if word not in self.words.keys():
                self.words[word] = {'never': 0, 'maybe': 0, 'good': 0}
            self.words[word][label] += 1

    def __to_freq(self):
        for word in self.words.keys():
            sum = 0
            for kw in self.words[word].keys():
                sum += self.words[word][kw]
            for kw in self.words[word].keys():
                if self.words[word][kw] != 0:
                    self.words[word][kw] = log(self.words[word][kw] / sum)
                else:
                    self.words[word][kw] = log(10 ** (-10))
        sum = 0
        for label in self.classes.keys():
            sum += self.classes[label]
        for label in self.classes.keys():
            if self.classes[label] != 0:
                self.classes[label] = log(self.classes[label] / sum)
            else:
                self.classes[label] = log(10 ** (-10))

if __name__ == '__main__':
    rows = s.query(News).all()
    naive = Model()
    naive.train(rows)
    naive.save('freq.pkl')
