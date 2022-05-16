from sample_generator import sample_generator
from bot_sample_generator import bot_sample_generator


def generate_ssc_sample():
    '''
    原始SSC-BOT语料支持的数据对构造方式

    数据格式要求较高，需要包含 question_id， skill_id 等字段
    '''
    #file_path = "data/faq_corpus_with_index.xlsx"
    file_path = 'output_data/faq_corpus_20220329.csv'
    #w2v_path = "data/vector.zhihu.word_100"
    w2v_path = "data/vector.zhihu.word"
    sample_generator.init(file_path, w2v_path)
    # sample_generator.generate_with_one_by_one(file_path)
    sample_generator.generate_with_random_sample(file_path, rate=1, n_cluster=50, is_save=True)

def generate_huaxiabank_sample():
    '''
    更加通用的数据对构造方式(2022.02.01)

    数据格式要求进一步简化，要求提供question 对应的意图名称，以及意图名称对应的大的分类（要支持只有一个分类的情况）
    '''
    file_path = "data/intent_corpus_with_index.csv"
    w2v_path = "data/vector.zhihu.word_100"
    sample_generator.init(file_path, w2v_path)
    # sample_generator_tool.generate_with_random_sample()

def generate_selfdefine_bot_sample():
    file_path = "data/bot_corpus_20220516.csv"
    # w2v_path = "data/vector.zhihu.word_100"
    output_path = "output_data/bot_train_20220516.csv"
    w2v_path = "data/vector.zhihu.word"
    bot_sample_generator.init(file_path, w2v_path)
    bot_sample_generator.generate_with_random_sample(file_path, output_path, rate=1, n_cluster=10, is_save=True)


if __name__ == '__main__':
    # generate_ssc_sample()
    generate_selfdefine_bot_sample()
