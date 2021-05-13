from typing import DefaultDict
import pandas as pd
from collections import defaultdict
from alias import Alias


class Data_Indexer(object):

    def __init__(self):
        self.alias2skill = defaultdict()
        self.alias2category = defaultdict()
        self.alias2question = defaultdict()
        self.alias2content = defaultdict()
        self.question2alias = defaultdict(list)
    
    def init(self, path='data/faq_corpus_with_index.xlsx'):
        dfs = pd.read_excel(path)
        self.alias2category = dict(zip(dfs['index'], dfs['category_id']))
        self.alias2question = dict(zip(dfs['index'], dfs['question_id']))
        self.alias2skill = dict(zip(dfs['index'], dfs['skill_id']))
        self.alias2content = dict(zip(dfs['index'], dfs['alias']))
        for question_id in dfs['question_id'].drop_duplicates().tolist():
            print('question_id', question_id)
            self.question2alias[question_id] = dfs[dfs['question_id'] == question_id]['index'].tolist()

    def generate_inputs(self, path='data/faq_corpus_with_index.xlsx'):
        dfs = pd.read_excel(path)
        inputs = dfs[['alias', 'index', 'question_id', 'skill_id', 'category_id']].apply(lambda x: Alias(x[0], x[1], x[2], x[3], x[4])).tolist()
        return inputs
    
    def get_alias_ques(self, qusetion_id):
        return self.question2alias[qusetion_id]
    
    def get_alias(self, alias_id):
        return self.alias2content[alias_id]

data_indexer = Data_Indexer()
