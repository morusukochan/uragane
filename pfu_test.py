import political_funds_utils as pfu

def main():
    # ExcelファイルをSQLiteデータベースに読み込む（更新が必要な場合はTrueを指定）
    pfu.load_excel_to_sqlite(update=True)
    
    # 検索したいURL
    search_url = r"https://www.soumu.go.jp/senkyo/seiji_s/seijishikin/contents/SK20190927/TK/0327203000115.pdf"
    
    # 指定されたURLをL列から検索し、該当行のG列、I列、K列を「→」で結合した結果を取得
    result = pfu.find_and_concatenate(search_url)
    
    # 結果を表示
    print(result)

if __name__ == "__main__":
    main()
