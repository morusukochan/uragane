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

def create_table(conn):
    """通常のテーブルを作成します。"""
    try:
        c = conn.cursor()
        # FTSテーブルではなく通常のテーブルを作成
        c.execute('''CREATE TABLE IF NOT EXISTS docs (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
    except sqlite3.Error as e:
        print(e)

def insert_doc(conn, doc):
    """ドキュメントをデータベースに挿入します。"""
    sql = '''INSERT INTO docs(title,content) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, doc)
    conn.commit()
    return cur.lastrowid

# FTS5に依存しない検索関数
def search_docs(conn, query, max_results):
    """複数のキーワードでAND条件を使用してデータベースを検索し、結果を返します。"""
    cur = conn.cursor()
    keywords = query.split()  # スペースでクエリを分割し、キーワードのリストを作成
    like_queries = [f"%{keyword}%" for keyword in keywords]  # 各キーワードに対してLIKE検索用の文字列を作成
    query_placeholders = ' AND '.join(['content LIKE ?' for _ in keywords])  # プレースホルダーを生成
    try:
        # 複数のLIKE条件をANDで結合し、すべての条件を満たす行を検索
        cur.execute(f"SELECT title, content FROM docs WHERE {query_placeholders} LIMIT ?", (*like_queries, max_results))
        return cur.fetchall()
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
        return []

# 検索結果表示関数の変更（snippet関数を使用しない）
def display_search_results(results):
    """検索結果を表示します。"""
    if not results:
        print("該当する検索結果無し")
        return False
    for idx, (title, content) in enumerate(results, start=1):
        # コンテンツの一部を表示する簡易的な方法
        print(f"{idx}. File: {title}\nContext: {content[:100]}...\n")
    return True

def tokenize_japanese_text(text):
    """日本語テキストをトークナイズします。"""
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(text, wakati=True)
    return " ".join(tokens)

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

def display_associated_png_files(directory_path, title):
    """関連するPNGファイルを表示します。"""
    base_name = os.path.splitext(title)[0]
    png_file = os.path.join(directory_path, f"{base_name}_boxes.png")
    if os.path.exists(png_file):
        print(f"PNG File: {png_file}")
        webbrowser.open(png_file)
    else:
        print(f"PNG File Not Exist: {png_file}")

def display_associated_pdf_files(directory_path, title, opened_files):
    """関連するPDFファイルを表示します。"""
    base_name = os.path.splitext(title)[0]
    png_file = os.path.join(directory_path, f"{base_name}_boxes.png")
    pdf_file = png_file.rsplit("_page", 1)[0] + ".pdf"

    if os.path.exists(pdf_file) and pdf_file not in opened_files:
        print(f"PDF File: {pdf_file}")
        webbrowser.open(pdf_file)
        opened_files.add(pdf_file)  # ファイルを開いたとして追跡
    else:
        print(f"PDF File Not Exist or Already Opened: {pdf_file}")

def display_matched_lines(documents, query):
    """検索にマッチした文書の内容から、クエリにマッチする行とその行番号を表示します。
    マッチする行があればTrue、なければFalseを返します。"""
    keywords = query.split()  # クエリをキーワードに分割
    matched = False  # マッチした行があるかどうかを追跡

    for title, content in documents:
        content_matched = all(keyword in content for keyword in keywords)  # コンテンツがすべてのキーワードを含むかチェック
        if not content_matched:
            continue  # すべてのキーワードにマッチしない場合はスキップ

        line_number = 0  # 行番号の初期化
        for line in content.split('\n'):
            line_number += 1
            if all(keyword in line for keyword in keywords):  # すべてのキーワードにマッチする行のみをチェック
                if not matched:  # 最初のマッチでTrueに設定
                    matched = True
                # ファイル名と行番号を含めてマッチした行を表示
                print(f"File: {title}, Line: {line_number}")
                print(f"Matched Line: {line}\n")
                
    if not matched:
        print("該当する検索結果無し")
    return matched

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
        create_table(conn)
        
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
            opened_files = set()  # 開いたファイルを追跡するセット
            search_query = input("Enter search keyword (or type 'exit' to quit): ")
            if search_query.lower() == 'exit':
                break
            results = search_docs(conn, search_query, max_results)  # ユーザーが指定した上限数を使用
            if display_matched_lines(results, search_query):
                if input("Display associated PNG files? (y/n): ").lower() == 'y':
                    for title, _ in results:
                        display_associated_png_files(directory_path, title)
                if input("Display associated PDF files? (y/n): ").lower() == 'y':
                    for title, _ in results:
                        display_associated_pdf_files(directory_path, title, opened_files)
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()