  ![裏金発見器の使い方-1](https://github.com/morusukochan/uragane/assets/128382257/0844d53b-fc73-45ab-90a5-c9d80b9142ae)  
  
  ![裏金発見器の使い方-3](https://github.com/morusukochan/uragane/assets/128382257/3fd97eca-576b-40ac-b5f2-39eafd6032e2)  

  すぐに始めたい人はここからダウンロードすればすぐに始められます  
      ### 政治資金収支報告書テキスト検索ツール（すぐに使えるパック）
      ギガファイル便　  
      政治資金収支報告書のみ版　ダウンロード期限：2024年6月2日(日)  
      https://47.gigafile.nu/0602-f90649ecf25e0c25e90822b8ef682df98  
  
      政治資金収支報告書&政党交付金使途等報告書版　ダウンロード期限：2024年6月12日(水) 
     [https://16.gigafile.nu/0612-f9f321c86df0da713f32332bfde7b00f3](https://16.gigafile.nu/0612-f9f321c86df0da713f32332bfde7b00f3)  
  

# 政治資金収支報告書のデータ化

  ## プロジェクトの概要
    本プロジェクトは、**総務省の政治資金収支報告書及び政党交付金使途等報告書**に関連するデータを取り扱います。現状、これらの収支報告書は紙で提出された後、スキャンデータとしてPDF形式で公開されていますが、サイトの構成が不親切で、一覧性に欠けています。

    このプロジェクトの目的は、全てのPDFデータをテキストデータ化し公開することにより、日本の政治資金の不正を多くの人が監視し、不正を告発することが可能になる環境を作り出すことです。これにより、より公正な政治活動へと変化していくことを目指しています。
![説明](https://github.com/morusukochan/uragane/assets/128382257/8817a6b1-86d4-44b4-8350-8a140c93659f)



  ## 政治資金収支報告書及び政党交付金使途等報告書スプレッドシート
    https://docs.google.com/spreadsheets/d/1LDCPJHwAqR2aIFU27a9HF81LtlTdhSeLXwfurvXfsUQ/edit?usp=sharing

   参照リンク
[総務省 政治資金収支報告書及び政党交付金使途等報告書](https://www.soumu.go.jp/senkyo/seiji_s/seijishikin/)

  ## PDF一括ダウンロード&OCRデータ
    ### 政治資金収支報告書
      ギガファイル便　ダウンロード期限：2024年5月26日(日)  
      https://83.gigafile.nu/0526-gf5a1e40d60e2461c60f80f8e97943073  

    ### 政治資金収支報告書テキスト検索ツール（すぐに使えるパック）
      ギガファイル便  
      政治資金収支報告書のみ版　ダウンロード期限：2024年6月2日(日)  
      https://47.gigafile.nu/0602-f90649ecf25e0c25e90822b8ef682df98  

      政治資金収支報告書のみ版　ダウンロード期限：2024年6月12日(水)   
      https://16.gigafile.nu/0612-f9f321c86df0da713f32332bfde7b00f3  
      

  ## テキストファイル一括検索ツール
    上記のPDF一括ダウンロード&OCRデータには収支報告書PDFをGoogle Vision APIによるOCR(光学的文字認識)により書き起こしたテキストデータと
    その時に文字として認識したエリアを赤枠で表示した画像ファイルが含まれています。
    膨大なテキストファイルを横断して、任意の文字列を一括検索し、画像ファイルも表示することができる一括検索ツールを作成しました。  
    (検索スピードを重視したモードしか作っていないので部分一致などは対応できていない。今後部分一致検索等も対応した精密な検索モードも作る予定)

    １．ダウンロード
      https://github.com/morusukochan/uragane/blob/main/dist  
      ・searchText.exe  
          初期のメディア向けリリース仕様 FTS5による全文検索は早いが完全一致のみであるため検索漏れがある  
      ・searchTextFTS5.exe   
          janomeを導入し日本語でも高速で部分一致検索を可能にしたデータベース更新に時間がかかる。3年分の収支報告書のデータベース化で1時間半（Corei9）  
      ・searchTextLike.exe  
         FTS5ではなくテーブルによるデータベース化とLIKE検索。部分一致検索はできるが検索にものすごく時間がかかる  

     ダウンロードはこのボタン  
![説明2](https://github.com/morusukochan/uragane/assets/128382257/ac7f02c1-0072-4675-81c4-93ffbc3095c5)

    ２．初回起動時のデータベース読み込み（win11の場合）  
      ダウンロードしたsearchText.exeファイルをfileフォルダと同じ階層に置く 
      fileフォルダはコレ→https://83.gigafile.nu/0526-gf5a1e40d60e2461c60f80f8e97943073  
      まずはサンプルデータとして少量のデータが入ったfilesフォルダをgithubにアップしたのでそちらで試してみることをお勧めします。
![image](https://github.com/morusukochan/uragane/assets/128382257/4b7e3562-daea-4b3d-851f-9ec4dbffa59d)


      searchText.exeをダブルクリックして起動　（Windowsセキュリティが出るので　詳細をおして→実行ボタンをおす）  
![実行1](https://github.com/morusukochan/uragane/assets/128382257/ff433f44-4396-42ad-bea1-3867fae46e10)
![実行](https://github.com/morusukochan/uragane/assets/128382257/1df92cab-449c-4115-8f4d-30801c58b1ad)  

      初回起動時のみデータベース更新をする  
        ↓yを入力してエンター（2回目以降の起動時はデータベース更新は不要ですnを押してスキップしてください）  
![image](https://github.com/morusukochan/uragane/assets/128382257/2f9d0d1b-7633-4ade-bebc-0044425bbeab)  
       （ここで1時間以上かかる）

     ３．一括テキスト検索
       検索結果の最大数を設定する（デフォルトは10）  
       任意の検索キーを入力  
![image](https://github.com/morusukochan/uragane/assets/128382257/22c26d4c-df6e-4ed8-826c-5ac0b7fe4c31)  
  
        マッチしたら返す（最大10に設定しています）　もっと増やしてほしいとか使い勝手の提案あればください  
        画像を表示するかどうかynをこたえる（半角のyだから気を付けて）  
        yでエンターを押すと検索にマッチした画像ファイルが表示される  

      以下ループ。おわりたければ検索キーの入力時にexitと入れるか窓を×で消す  

    ## このプロジェクトのライセンス
      OCRによる一括読み取りデータやテキスト検索ツール等このオープンソースプロジェクトによる成果物は全て
      MITライセンスで広く提供します

    ## 今後の予定(2~3週間ぐらいでやること)  
     ・政党交付金使途等報告書のPDF一括ダウンロード  
     ・政党交付金使途等報告書をGoogle Vision APIでテキスト化  
     ・政党交付金使途等報告書データベースに追加  
     ・一般公開（配信で寄付募る　膨大な数の画像データを有料サービスGoogle Visionで読み取っている４～５万円かかる見通し　過去分入れたらもっと？）  
