import os
import pymupdf

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 条件分岐の練習
weather = "晴れ"
if weather == "晴れ":
    print("お買い物へ行ってきます")

weather = "雨"
if weather == "晴れ":
    print("お買い物へ行ってきます")
elif weather == "雨":
    print("お家でゴロゴロします")

weather = "曇り"
if weather == "晴れ":
    print("お買い物へ行ってきます")
elif weather == "雨":
    print("お家でゴロゴロします")
else:
    print("近所をお散歩します")

# PDFの1ページ目のテキストを表示
doc = pymupdf.open("sample.pdf")
page = doc[0]
text = page.get_text()
print(text)
doc.close()

# PDFの1ページ目だけを別名で保存
doc = pymupdf.open("sample.pdf")
doc.select([0])
doc.save("output_1page.pdf")
doc.close()

# PDFの向きを90度回転
doc = pymupdf.open("output_1page.pdf")
page = doc[0]
page.set_rotation(90)
doc.save("output_rotated.pdf")
doc.close()

# PDFの結合
doc_a = pymupdf.open("sample.pdf")
doc_b = pymupdf.open("output_rotated.pdf")
doc_a.insert_file(doc_b)
doc_a.save("output_inserted.pdf")
doc_a.close()
doc_b.close()

# PDFのページを削除
doc = pymupdf.open("output_inserted.pdf")
doc.delete_page(2)
doc.save("output_deleted.pdf")
doc.close()