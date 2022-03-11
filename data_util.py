import pandas as pd


def read_data(path):
    if path.endswith('excel'):
        return pd.read_excel(path)
    if path.endswith('csv'):
        return pd.read_csv(path, sep='\t')\

def rename_column(dfs):
    dfs = dfs[['技能', '一级分类', '标准问(必填)', '答案(最多10条)','扩展问(最多1000条)']]
    dfs_rename = dfs.rename(columns={'技能': 'skill', '一级分类': 'category1',
    '标准问(必填)': 'question', '扩展问(最多1000条)': 'alias', '答案(最多10条)':'answer'})
    return dfs_rename

def ffill_common_column(dfs):
    dfs_ffill = dfs[['skill', 'category1', 'question']].fillna(method='ffill', inplace=False)
    dfs_ffill.loc[:, 'alias'] = dfs.loc[:, 'alias']
    return dfs_ffill

def merge_data(dfs_list):
    dfs_merge = pd.concat(dfs_list, ignore_index=True)
    dfs_filter = dfs_merge.drop_duplicates(subset='alias', keep='first',ignore_index=True)
    return dfs_filter

def add_id_mapping(dfs, column_maps = ['skill', 'category1', 'question']):
    id_mapping = {}
    for column in column_maps:
        items = dfs[column].dropna().drop_duplicates().tolist()
        id_mapping[column] = dict(zip(items, range(1, len(items) + 1)))
        dfs.loc[:, column + '_' + 'id'] = dfs.loc[:, column].apply(lambda x: id_mapping[column][x])

    dfs.loc[:, 'index'] = dfs.index + 1
    return dfs

def output2file(dfs, path='faq_corpus_20220311.csv'):
    dfs.to_csv(path, index=False, sep='\t')


def main():
    pass


if __name__ == '__main__':
    pass