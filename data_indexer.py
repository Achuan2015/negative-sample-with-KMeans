from typing import DefaultDict
import pandas as pd
from collections import defaultdict
from alias import Alias


class Data_Indexer(object):

    def __init__(self):
        self.alias2skill = defaultdict()
        self.alias2category = defaultdict()
        self.alias2question = defaultdict()


    def read(self, path='data/faq_corpus_with_index.xlsx'):
        dfs = pd.read_excel(path)
        inputs = []
        for _, row in dfs.iterrows():
            input_instance = Alias(row['alias'],
                                   row['index'],
                                   row['question_id'],
                                   row['skill_id'],
                                   row['category_id'])
            self.alias2category[row['index']] = row['category_id']
            self.alias2question[row['index']] = row['question_id']
            self.alias2skill[row['index']] = row['skill_id']
        inputs.append(input_instance)
        return inputs

data_indexer = Data_Indexer()