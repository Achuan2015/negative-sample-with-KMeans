from typing import DefaultDict
import pandas as pd
from collections import defaultdict
from alias import Alias, Sentence


class Data_Indexer(object):

    def __init__(self):
        self.alias2skill = defaultdict()
        self.alias2category = defaultdict()
        self.alias2question = defaultdict()
        self.alias2content = defaultdict()
        self.question2alias = defaultdict(list)
    
    def init(self, path='data/faq_corpus_with_index.xlsx'):
        if path.endswith('xlsx'):
            dfs = pd.read_excel(path)
        else:
            dfs = pd.read_csv(path, sep='\t')
        self.alias2category = dict(zip(dfs['index'], dfs['category1_id']))
        self.alias2question = dict(zip(dfs['index'], dfs['question_id']))
        self.alias2skill = dict(zip(dfs['index'], dfs['skill_id']))
        self.alias2content = dict(zip(dfs['index'], dfs['alias']))
        for question_id in dfs['question_id'].drop_duplicates().tolist():
            self.question2alias[question_id] = dfs[dfs['question_id'] == question_id]['index'].tolist()

    def generate_inputs(self, path='data/faq_corpus_with_index.xlsx'):
        if path.endswith('xlsx'):
            dfs = pd.read_excel(path)
        else:
            dfs = pd.read_csv(path, sep='\t')
        #inputs = dfs[['alias', 'index', 'question_id', 'skill_id', 'category1_id']].apply(lambda x: Alias(x[0], x[1], x[2], x[3], x[4])).tolist()
        inputs = dfs.apply(lambda row: Alias(row['alias'], row['index'], row['question_id'], row['skill_id'], row['category1_id']), axis=1).tolist()
        return inputs
    
    def get_alias_ques(self, qusetion_id):
        return self.question2alias[qusetion_id]
    
    def get_alias(self, alias_id):
        return self.alias2content[alias_id]


class Sentence_Index(object):

    def __init__(self):
        self.index2dimension = defaultdict()
        self.index2intent = defaultdict()
        self.index2content = defaultdict()
        self.intent2index = defaultdict(list)

    def init(self, path='data/intent_corpus_with_index.csv'):
        dfs = pd.read_csv(path, sep='\t')
        self.index2dimension = dict(zip(dfs['index'], dfs['dimension']))
        self.index2intent = dict(zip(dfs['index'], dfs['intent']))
        self.index2content = dict(zip(dfs['index'], dfs['content']))
        for intent in dfs['intent'].drop_duplicates().tolist():
            self.intent2index[intent] = dfs[dfs['intent'] == intent]['index'].tolist()
    
    def generate_inputs(self, path='data/intent_corpus_with_index.csv'):
        dfs = pd.read_csv(path, sep='\t')
        return dfs[['content', 'index', 'intent', 'dimension']]

data_indexer = Data_Indexer()
sentence_index = Sentence_Index()
