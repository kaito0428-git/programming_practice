
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

import pymupdf
doc = pymupdf.open("error.pdf")
page =doc[0]
text = page.get_text()
print(text)

doc.close()

#PDFの1ページを名前を変えて保存
doc = pymupdf.open("error.pdf")
doc.select([0])
doc.save("error_1page.pdf")
doc.close()

#PDFの角度を変える
doc = pymupdf.open("error_1page.pdf")
page = doc[0]
page.set_rotation(90)
doc.save("rotated.pdf")
doc.close()

#PDFの統合
doc_a = pymupdf.open("error.pdf")
doc_b = pymupdf.open("rotated.pdf")
doc_a.insert_file(doc_b)
doc_a.save("inserted.pdf")
doc_a.close()
doc_b.close()

#PDFのページの削除
doc = pymupdf.open("inserted.pdf")
doc.delete_page(2)
doc.save("delete.pdf")
doc.close()

