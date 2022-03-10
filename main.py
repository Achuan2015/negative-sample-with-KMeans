from sample_generator import sample_generator


def generate_ssc_sample():
    '''
    原始SSC-BOT语料支持的数据对构造方式
    '''
    file_path = "data/faq_corpus_with_index.xlsx"
    w2v_path = "data/vector.zhihu.word_100"
    sample_generator.init(file_path, w2v_path)
    # sample_generator.generate_with_one_by_one(file_path)
    sample_generator.generate_with_random_sample(file_path, rate=1, n_cluster=50, is_save=True)

def generate_huaxiabank_sample():
    '''
    更加通用的数据对构造方式
    '''
    file_path = "data/intent_corpus_with_index.csv"
    w2v_path = "data/vector.zhihu.word_100"
    sample_generator.init(file_path, w2v_path)
    sample_generator_tool.generate_with_random_sample()


if __name__ == '__main__':
    generate_huaxiabank_sample()