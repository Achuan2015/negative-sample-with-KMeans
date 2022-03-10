

from sample_generator import Sample_Generator


class Sample_Generator_Tool(object):

    def __init__(self):
        self.compute_embedding = compute_embedding
        self.data_indexer = data_indexer
        self.cluster_points = defaultdict(list)


sample_generator_tool = Sample_Generator_Tool()