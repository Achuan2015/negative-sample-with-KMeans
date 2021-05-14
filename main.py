from sample_generator import sample_generator


if __name__ == "__main__":
    file_path = "data/faq_corpus_with_index.xlsx"
    w2v_path = "data/vector.zhihu.word_100"
    sample_generator.init(file_path, w2v_path)
    # sample_generator.generate_with_one_by_one(file_path)
    sample_generator.generate_with_random_sample(file_path, rate=1, n_cluster=50, is_save=True)
