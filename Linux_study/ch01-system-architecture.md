Linuxsコマンド

・基本動作
コマンド/項目		用途

bash			代表的なシェル(コマンドを解釈・実行するプログラム)
echo $変数名		環境変数の値を表示(例:echo $PATH)
export 変数名=値	環境変数を設定
env			現在の環境変数一覧を表示

*, ?, [ ]		ワイルドカード(*=任意の文字列、?=任意の1文字)
ls *.txt      		# 拡張子がtxtのファイルすべて
ls file?.txt   		# file1.txt, fileA.txt など、?の位置が1文字なら何でも
ls file[123].txt  	# file1.txt, file2.txt, file3.txt のいずれか

クォート(', ")による違い
name="Kaito"
echo "こんにちは $name"   	# → こんにちは Kaito(変数が展開される)
echo 'こんにちは $name'  	# → こんにちは $name(展開されず、そのまま表示)


エスケープ(\)
echo "価格は $100 です"      	# $1が変数として展開されようとしてしまう
echo "価格は \$100 です"     	# \でエスケープすると、$がそのまま文字として表示される

aliasコマンド
1. alias(一覧表示)
alias grep='grep --color=auto'
alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'


2. alias ll='ls -l' を再定義
bash
$ alias ll='ls -l'
$ ll

3. alias rm='rm -i'　rmを押すと警告文が出るように変更
bash
$ alias rm='rm -i'
$ rm
rm: missing operand


４．消そうとすると警告文が表示され（ｙ）でＹＥＳ（ｎ）でＮＯを選択することができる
$ rm file1.txt
rm: remove regular empty file 'file1.txt'? n


５．永続化について
ログアウトすると消えてしまうため固定化する

echo "alias ll='ls -l'" >> ~/.bashrc


pwdコマンド

pwd	現在のディレクトリを表示(シンボリックリンクがあれば解決済みのものを表示することが多い)
pwd -P	シンボリックリンクを完全に解決した「物理的な」実際のパスを表示
pwd -L	シンボリックリンクをそのまま(論理パスとして)表示


cdコマンド
cd /etc → ルート直下のetcディレクトリへ移動、pwdが/etcを表示
cd / → ルートディレクトリ(最上位)へ移動、pwdが/を表示
cd ~ → ホームディレクトリへ移動、pwdが/home/kaitoを表示


コマンド	用途

grep		文字列検索
sort		行の並べ替え
wc -l		行数カウント
cat		ファイル内容の表示・結合
tee -a		画面表示とファイル保存を同時に行う(追記)


テキストデータ処理/標準入出力

名称			略称		番号
標準入力		stdin		0
標準出力		stdout		1
標準エラー出力		stderr		2


リダイレクトとパイプ

記号	意味				実機確認結果

>	標準出力を上書きでファイルへ	echo "A" > f.txt
>>	標準出力を追記でファイルへ	echo "B" >> f.txt
2>	標準エラー出力だけをファイルへ	ls /etc /nonexistent 2> error.txt
|	前のコマンドの出力を次へ渡す	cat f.txt | grep 1



~/.bashrc		シェルの環境設定ファイル(起動時に読み込まれる)

・ファイル操作
コマンド	用途

ls		ファイル・ディレクトリ一覧表示
ls -l		詳細情報付きで表示(パーミッション、所有者など)
ls -a		隠しファイルも含めて表示
cd		ディレクトリ移動
pwd		現在のディレクトリを表示(絶対パス)
mkdir		ディレクトリ作成
touch		空ファイル作成、タイムスタンプ更新
cp		ファイルコピー
mv		ファイル移動・名前変更
rm		ファイル削除
rm -r		ディレクトリごと再帰的に削除
tar -cvf	アーカイブ作成(圧縮なし)
tar -xvf	アーカイブ展開
tar -czvf	gzip圧縮しながらアーカイブ作成
gzip / gunzip	ファイルの圧縮/展開


・テキストデータ処理
コマンド/記号		用途

>			標準出力をファイルに上書きリダイレクト
>>			標準出力をファイルに追記リダイレクト
<			標準入力をファイルからリダイレクト
|			パイプ(あるコマンドの出力を次のコマンドの入力に渡す)
grep			文字列検索(フィルタコマンド)
sort			行の並べ替え
uniq			重複行の削除
wc			行数・単語数・文字数のカウント
cat			ファイル内容を表示・結合
tee			標準出力をファイルに保存しつつ、画面にも表示(パイプの途中で分岐)





