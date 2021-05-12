from sample_generator import sample_generator


if __name__ == "__main__":
    file_path = "data/faq_corpus_with_index.xlsx"
    w2v_path = "data/vector.zhihu.word"
    sample_generator.init(file_path, w2v_path)
    sample_generator.generate(file_path)