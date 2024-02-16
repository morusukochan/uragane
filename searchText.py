import sqlite3
import os
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

def insert_doc(conn, doc):
    """ドキュメントをデータベースに挿入します。"""
    sql = ''' INSERT INTO docs(title,content) VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, doc)
    conn.commit()
    return cur.lastrowid

def update_database_from_files(conn, directory_path):
    """指定されたディレクトリ内の全てのテキストファイルをデータベースに追加します。"""
    text_files = [f for f in os.listdir(directory_path) if f.endswith(".txt")]
    for filename in tqdm(text_files, desc="Inserting files into database"):
        filepath = os.path.join(directory_path, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            insert_doc(conn, (filename, content))
    print("All files have been inserted into the database.")

def search_docs(conn, query):
    """データベースで検索クエリを実行し、結果を返します。"""
    cur = conn.cursor()
    cur.execute("SELECT title, snippet(docs, 1, '<b>', '</b>', '...', 10) FROM docs WHERE docs MATCH ? LIMIT 10", (query,))
    return cur.fetchall()

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

    # 実行可能ファイルのディレクトリを取得
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    # 相対パスを絶対パスに変換
    directory_path = os.path.join(application_path, 'files')
    #directory_path = r"C:\Users\satof\sato\ocr\google\release_1\files"
    #directory_path = r"C:\Users\satof\sato\ocr\google\test3"

    if conn is not None:
        create_fts_table(conn)
        
        if args.update:#開発者用
            update_database_from_files(conn, directory_path)
            print("Database updated.")
        else:
            if input("データベースを更新しますか? (y/n): ").lower() == 'y':#ユーザー用
                update_database_from_files(conn, directory_path)
                print("Database updated.")
            else:
                print("Skipping database update.")
    
        while True:
            search_query = input("Enter search keyword (or type 'exit' to quit): ")
            if search_query.lower() == 'exit':
                break
            results = search_docs(conn, search_query)
            if display_search_results(results):
                if input("Display associated PDF and PNG files? (y/n): ").lower() == 'y':
                    for title, _ in results:
                        display_associated_files(directory_path, title)
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
