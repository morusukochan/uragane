import sqlite3
import os
from janome.tokenizer import Tokenizer
import webbrowser
from tqdm import tqdm
import argparse
import sys

def create_connection(db_file):
    """データベース接続を作成し、接続を返します。"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_fts_table(conn):
    """FTSテーブルを作成します。"""
    try:
        c = conn.cursor()
        c.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5(title, content)''')
    except sqlite3.Error as e:
        print(e)

def tokenize_japanese_text(text):
    """日本語テキストをトークナイズします。"""
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(text, wakati=True)
    return " ".join(tokens)

def insert_doc(conn, doc):
    """トークナイズされたドキュメントをデータベースに挿入します。"""
    sql = ''' INSERT INTO docs(title,content) VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, doc)
    conn.commit()
    return cur.lastrowid

def update_database_from_files(conn, directory_path):
    """指定されたディレクトリ内の全てのテキストファイルをトークナイズしてデータベースに追加します。"""
    text_files = [f for f in os.listdir(directory_path) if f.endswith(".txt")]
    for filename in tqdm(text_files, desc="Inserting files into database"):
        filepath = os.path.join(directory_path, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            tokenized_content = tokenize_japanese_text(content)
            insert_doc(conn, (filename, tokenized_content))
    print("All files have been inserted into the database.")

def escape_fts_query(query):
    """FTS5クエリで解釈される特別な記号をエスケープします。"""
    # 特別な記号をエスケープするために、ダブルクォーテーションで囲みます
    # ダブルクォーテーション自体もエスケープが必要です
    escape_chars = ['"', '*', '(', ')', ':', "'", '-']
    for char in escape_chars:
        if char in query:
            # ダブルクォーテーションは特別な処理が必要です
            if char == '"':
                query = query.replace(char, '""')
            else:
                query = query.replace(char, f'"{char}"')
    return query

def search_docs(conn, query, max_results):
    """エスケープ処理を施したクエリでデータベースを検索し、結果を返します。"""
    # トークナイズされたクエリを取得
    tokenized_query = tokenize_japanese_text(query)
    
    # FTS5クエリの特別な記号をエスケープ
    escaped_query = escape_fts_query(tokenized_query)
    
    cur = conn.cursor()
    try:
        # SQLクエリでmax_resultsを使用
        cur.execute("SELECT title, snippet(docs, 1, '<b>', '</b>', '...', 10) FROM docs WHERE docs MATCH ? LIMIT ?", (escaped_query, max_results))
        return cur.fetchall()
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
        return []

def display_search_results(results):
    """検索結果を表示します。"""
    if not results:
        print("該当する検索結果無し")
        return False  # 検索結果がない場合はFalseを返します
    for idx, (title, context) in enumerate(results, start=1):
        print(f"{idx}. File: {title}\nContext: {context}\n")
    return True  # 検索結果がある場合はTrueを返します

def display_associated_files(directory_path, title):
    """関連するPDFとPNGファイルを表示します。"""
    base_name = os.path.splitext(title)[0]
    png_file = os.path.join(directory_path, f"{base_name}_boxes.png")
    if os.path.exists(png_file):
        print(f"PNG File: {png_file}")
        webbrowser.open(png_file)
    else:
        print(f"PNG File Not Exist: {png_file}")

def main():
    parser = argparse.ArgumentParser(description="Search and display text files, PDFs, and PNGs.")
    parser.add_argument("--update", action="store_true", help="Update the database with new files from the specified directory.")
    
    args = parser.parse_args()
    
    database = "pythonsqlite.db"
    conn = create_connection(database)

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    directory_path = os.path.join(application_path, 'files')

    if conn is not None:
        create_fts_table(conn)
        
        if args.update:
            update_database_from_files(conn, directory_path)
            print("Database updated.")
        else:
            if input("データベースを更新しますか? (y/n): ").lower() == 'y':
                update_database_from_files(conn, directory_path)
                print("Database updated.")
            else:
                print("Skipping database update.")
        
        # ユーザーに検索結果の上限数を尋ねる
        try:
            max_results = int(input("検索結果の表示上限数を入力してください（デフォルトは10）: "))
        except ValueError:
            print("無効な入力です。デフォルト値の10を使用します。")
            max_results = 10
        
        while True:
            search_query = input("Enter search keyword (or type 'exit' to quit): ")
            if search_query.lower() == 'exit':
                break
            results = search_docs(conn, search_query, max_results)  # ユーザーが指定した上限数を使用
            if display_search_results(results):
                if input("Display associated PNG files? (y/n): ").lower() == 'y':
                    for title, _ in results:
                        display_associated_files(directory_path, title)
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()