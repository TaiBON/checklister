namelist-generator
==================

## 名錄產生器

namelist-generator 會根據「基礎資料清單(baselist)」 及「樣本清單(sample) 」自動產生階層式的名錄，
植物名錄按照蕨類、裸子植物、「雙子葉植物」、單子葉植物四大類排序，下依照科名字母順序、物種名字母順序排列。
'data/twnamelist.csv'是基於 Flora of Taiwan 2nd Edition 以及近年來新發現或訂正之物種名錄。'data/sample.csv'
則是從 twnamelist.csv 中隨機產生的物種中名範例檔。目前 data/twnamelist_apg3.csv 及 data/twnamelist.csv 包含
臺灣目前原生、歸化及部分栽培維管束物種清單

### 開發語言及相依軟體

* [Python 3](https://www.python.org)
    + packages: sqlite, csv, subprocess, sys 
* [Pandoc](http://johnmacfarlane.net/pandoc/)


### 安裝

#### Unix, GNU/Linux, MacOS 的安裝

下列安裝可以透過第三方套件管理程式(GNU/Linux，以 Ubuntu 為例可使用 aptitude/apt-get，
Mac OS 則可以使用 [homebrew](http://brew.sh)，FreeBSD 可以使用 pkg 或 ports 安裝)

1. 安裝 [Python 3](https://www.python.org)
2. 安裝 [Pandoc](http://johnmacfarlane.net/pandoc/)
3. [Clone](https://github.com/mutolisp/namelist-generator.git)至你的桌面環境，或是直接下載[zip](https://github.com/mutolisp/namelist-generator/archive/master.zip)

#### Windows 平台的安裝

*設定 Python 路徑*
Windows 的安裝方法和上面相同，只是需要設定路徑，在安裝完之後，從「控制台」/「系統及安全性」/「系統」，
中選取進階系統設定，「進階」中選擇編輯「環境變數」，將變數 PATH 設定為
```
C:\Users\yourusername\AppData\Local\Pandoc;C:\Python34\
```
(前方的 Pandoc 是當你安裝完之後會自動設定，後面加上分號及新增的 Python 路徑，不加也沒關係，
只是需要多打幾個字)

![設定路徑](https://raw.github.com/mutolisp/namelist-generator/master/docs/setpath.png)


### 使用方法

#### 參數
```
-d 代表物種名彙資料表
-s 代表需產生名錄的物種中名
-f 檔案格式，預設會同時產生 markdown (md) 文字檔與 pandoc 所支援的檔案格式(例如 docx)
-o 輸出名錄檔案檔名，例如 output (不用加附檔名)
```

1. 將您要產生的物種名錄存成 txt 或 csv 檔案(每個物種一行，以 UTF-8 編碼)，例如：

```
台灣艾納香
玉山柳
濱旋花
渡邊氏萬年青
多花山柑
大野牡丹
泰來藻
山薔薇
翼柄崖爬藤
台灣海桐
日本灰木
黃花庭菖蒲
銳葉新木薑子
喜樹
萊氏線蕨
```
*WINDOWS 平台注意事項*
因為中文 Windows 預設為 CP950 (Big5 擴充字集) 編碼，但 namelist-generator 全部都是使用 UTF-8 編碼，
所以必須要將文字檔存成 UTF-8，如下圖：

![存成 UTF-8](https://raw.github.com/mutolisp/namelist-generator/master/docs/save_namelist.png)

2. 接下來開啟命令提示字元(cmd.exe)或終端機(Terminal)，輸入下方指令（假設您下載的原始碼在 C:\namelist-generator）：
*WINDOWS 使用者:*

```
    cd C:\namelist-generator
    python src\genlist.py -d data\twnamelist_apg3.csv -s data\sample.csv -f docx -o namelist
```

則會在 C:\namelist-generator 下產生 namelist.md 及 namelist.docx 兩個檔案，之後您就可以再次確認植物名錄了。
*GNU/Linux, MacOS 等 *nix 使用者*
```    
    cd path/to/namelist-generator;
    python3 src/genlist.py -d data/twnamelist_apg3.csv -s data/sample.csv -f docx -o namelist
```
接下來則會輸出 markdown 檔 output.md  及 Microsoft Office Word 檔 output.docx 


### 轉換文件格式

若有安裝 xelatex，則可以使用下列指令轉成 pdf 檔
```
    pandoc --latex-engine=xelatex -V mainfont='Times New Roman' --template pandoc.template output.md -o output.pdf
```

### 輸出範例

![Demo docx](https://github.com/mutolisp/namelist-generator/blob/master/demo/demo_docx.png)

### 同物異名或同名異物
namelist-generator 完全依賴 baselist (也就是 data/twnamelist.* )，所以只要 baselist 裡頭資料正確，產生的名錄即為正確名錄。
但仍會有一些中名相同的問題需要修正，
例如：

紫草科和禾本科中名皆有狗尾草，此時則需判斷是否為 _Heliotropium indicum_ 或 _Setaria viridis_。

發現資料檔案(twnamelist_apg3.csv & twnamelist.csv)有錯誤或是有使用上的問題歡迎直接 email 問我(mutolisp _AT_ gmail)
