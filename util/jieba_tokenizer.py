# -*- coding: utf-8 -*-
import glob
import jieba
import jieba.analyse


class Jieba_Tokenizer(object):
    """Uses module jieba to tokenize input texts.

    Attributes:
    """

    @staticmethod
    def load_custom_dictionary(path):
        """Load all the custom dictionaries stored in the path.

        Args:
            path: the path of user's dictionaries.
        """
        jieba_userdicts = glob.glob("{}/*".format(path))
        for jieba_userdict in jieba_userdicts:
            jieba.load_userdict(jieba_userdict)

    @staticmethod
    def load_custom_idf(path):
        jieba.analyse.set_idf_path(path)

    @staticmethod
    def tokenize(text):
        tokens = [{"word": word, "start": start, "end": end}
                  for word, start, end in jieba.tokenize(text)]
        return tokens

    @staticmethod
    def cut(text):
        return jieba.cut(text)

    @staticmethod
    def extract_tags(text, topK=20):
        return jieba.analyse.extract_tags(text, topK=topK, withWeight=True)


if __name__ == "__main__":
    aa = Jieba_Tokenizer.tokenize('我喜欢你')
    aa = Jieba_Tokenizer.extract_tags('我喜欢你')
    print(aa)