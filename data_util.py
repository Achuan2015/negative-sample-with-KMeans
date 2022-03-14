import pandas as pd
from pathlib import Path


def read_previous_data(path, common_columns = ['skill', 'category1', 'question', 'alias']):
    dfs = pd.read_csv(path, sep='\t')
    dfs_common = dfs[common_columns]
    return dfs_common
    

def read_data(path):
    return pd.read_excel(path)

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
    dfs_filter = dfs_merge.dropna().drop_duplicates(subset='alias', keep='first',ignore_index=True)
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
    dir = 'input_data'
    dir = Path(dir)
    data_dfs = []
    for path in dir.glob('*20220311.xlsx'):
        dfs = read_data(path)
        dfs_rename = rename_column(dfs)
        dfs_ffill = ffill_common_column(dfs_rename)
        data_dfs.append(dfs_ffill)
    dfs_previous = read_previous_data('data/faq_corpus_with_index.csv')
    data_dfs.append(dfs_previous)
    print('data_dfs length:', len(data_dfs))
    dfs_merge = merge_data(data_dfs)
    dfs_output = add_id_mapping(dfs_merge)
    output2file(dfs_output)

if __name__ == '__main__':
    main()
