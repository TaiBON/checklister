nmelist-generator
==================

## 名錄產生器

namelist-generator 會根據「基礎資料清單(baselist)」 及「樣本清單(sample) 」自動產生階層式的名錄，
植物名錄按照蕨類、裸子植物、「雙子葉植物」、單子葉植物四大類排序，下依照科名字母順序、物種名字母順序排列。
'data/twnamelist.csv'是基於 Flora of Taiwan 2nd Edition 以及近年來新發現或訂正之物種名錄。'data/sample.csv'
則是從 twnamelist.csv 中隨機產生的物種中名範例檔。

### 開發語言及相依軟體

* [Python 3](https://www.python.org)
    + packages: sqlite, csv, subprocess, sys 
* [Pandoc](http://johnmacfarlane.net/pandoc/)


### 使用方法

1. 安裝 [Python 3](https://www.python.org)
2. 安裝 [Pandoc](http://johnmacfarlane.net/pandoc/)
3. [Clone](https://github.com/mutolisp/namelist-generator.git)至你的桌面環境，或是直接下載[zip](https://github.com/mutolisp/namelist-generator/archive/master.zip)
4. 終端機輸入：
```    
    cd path/to/namelist-generator;
    python3 src/genlist.py data/twnamelist.csv data/sample.csv
```
接下來則會輸出 markdown 檔 output.md  及 Microsoft Office Word 檔 output.docx 



### 轉換文件格式

若有安裝 xelatex，則可以使用下列指令轉成 pdf 檔
```
    pandoc --latex-engine=xelatex -V mainfont='Times New Roman' --template pandoc.template output.md -o output.pdf
```

### 輸出範例

!(https://github.com/mutolisp/namelist-generator/blob/master/demo/demo_docx.png)

### 同物異名或同名異物
namelist-generator 完全依賴 baselist ，所以只要 baselist 裡頭資料正確，產生的名錄即為正確名錄。但仍會有一些中名相同
例如：

紫草科和禾本科中名皆有狗尾草，此時則需判斷是否為 _Heliotropium indicum_ 或 _Setaria viridis_。




