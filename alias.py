class Alias:

    def __init__(self, content, alias_id, question_id, field_id, category_id, vector=None):
        self.content = content
        self.alias_id = alias_id
        self.question_id = question_id
        self.category_id = category_id
        self.vector = vector
        self.field_id = field_id 

class Sentence:

    def __init__(self, content, index, intent, dimension):
        self.content = content
        self.index = index
        self.intent = intent
        self.dimension = dimension
