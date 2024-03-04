import pandas as pd
from sqlalchemy import create_engine

def load_excel_to_sqlite(db_path='sqlite:///political_funds.db', excel_path='政治資金収支報告書一覧表.xlsx', update=False):
    engine = create_engine(db_path)
    # header=Noneを指定して列名がない状態で読み込み、列に名前を付ける
    df = pd.read_excel(excel_path, header=None, skiprows=1)  # 最初の行がヘッダでない場合はskiprowsを調整
    df.columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']  # 必要な数だけ列名を付ける

    if update:
        try:
            existing_df = pd.read_sql('select * from political_funds', con=engine)
            updated_df = pd.concat([existing_df, df]).drop_duplicates()
            updated_df.to_sql('political_funds', con=engine, if_exists='replace', index=False)
        except Exception as e:
            df.to_sql('political_funds', con=engine, if_exists='replace', index=False)
    else:
        df.to_sql('political_funds', con=engine, if_exists='replace', index=False)

def find_and_concatenate(url, db_path='sqlite:///political_funds.db'):
    engine = create_engine(db_path)
    # 修正したクエリ: 列名を使用
    query = """
    SELECT G, I, K FROM political_funds
    WHERE L = :url
    """
    df = pd.read_sql(query, con=engine, params={'url': url.strip()})
    if not df.empty:
        return ' → '.join(df.iloc[0].values)
    else:
        return "該当するデータが見つかりません。"


# 使用例
# load_excel_to_sqlite(update=True)  # データベースを更新（テーブルが存在しない場合は新規作成）
# result = find_and_concatenate('指定されたURL')
# print(result)
