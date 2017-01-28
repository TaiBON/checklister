
物種名錄產生器 Checklister
====================

checklister 會根據「基礎資料清單(baselist)」 及「樣本清單(sample) 」自動產生階層式的名錄，
植物名錄按照蕨類、裸子植物、「雙子葉植物」、單子葉植物四大類排序，下依照科名字母順序、物種名字母順序排列。
'data/twnamelist.csv'是基於 Flora of Taiwan 2nd Edition 以及近年來新發現或訂正之物種名錄。'data/sample.csv'
則是從 twnamelist.csv 中隨機產生的物種中名範例檔。目前 data/twnamelist_pg.csv 及 data/twnamelist.csv 包含
臺灣目前原生、歸化及部分栽培維管束物種清單。

授權為通用公共授權第三版 (General Public License version 3; GPL v3)，也就是您可以自由複製、取得、散佈並修改。

### 執行檔下載

目前僅支援 windows 和 MacOS X：

* [Windows 平台; v0.4.0](https://github.com/TaiBON/checklister/releases/download/v0.4.0/checklister_v0.4.0.exe)
* [MacOS X](https://github.com/TaiBON/checklister/releases/download/v0.4.0/checklister_v0.4.0.app.zip)

### Supported checklist

1. 臺灣維管束植物名錄 (Vascular plants of Taiwan, APGIV / Flora of Taiwan 2nd Edition)。資料來源：[臺灣植物資訊整合查詢系統](http://tai2.ntu.edu.tw), [TaiBNET](http://taibnet.sinica.edu.tw)
    1. 收錄物種：6019 種 (v 0.4.0, 2016-09-08, 2017-01-08 資料更新)
2. 臺灣鳥類名錄 2014 (Bird list of Taiwan)。資料來源：[中華野鳥學會](www.bird.org.tw/index.php/works/lists)
3. Plants of Japan ("Ylist", 20103 records). Source: http://ylist.info

### Developing language and dependencies

* Developing language [Python 3](https://www.python.org)
    + libraries: codecs, csv, subprocess, sqlite, sys, etc.
    + Database: sqlite
    + GUI libraries: pyqt5 (Qt 5.6)
    + Convert python into standalone executable: pyinstaller 

* Document conversion [Pandoc](http://johnmacfarlane.net/pandoc/)

### Installation

* Supported platforms (platform-independant 32/64 bits)： 
    + MacOSX (Tested on 10.10， version 10.6+ should work)
    + Windows (Compiled with 32 bits MinGW，tested on Windows 10 x64, 8 x64, 7 x64)
    + GNU/Linux (Tested on Ubuntu 14.04), *BSD (not yet test)

* Supported languages: zh_TW (traditional Chinese), zh_CN (simplified Chinese), ja_JP (Japanese), ko_KR (Korean)

* Download executable binary：Latest version is [0.4.0](https://github.com/TaiBON/checklister/releases/latest)
    + Windows (*.exe), copy the executable file to whatever you like (even on USB disk)
    + MacOS X, copy, unarchive and put checklister.app in /Applications

* Compile by yourself (linux, macos)
    1. Install git, python3, pip, pyqt5, pandoc (視需求可能會需要安裝 zlib 之類的)
    2. pip install pypandoc
    3. Clone pyinstaller python3 branch: `git clone https://github.com/pyinstaller/pyinstaller.git`
    4. `cd pyinstaller; git checkout python3`
    5. Install bootloader: `cd pyinstaller; python3 waf configure; python3 waf all`
    6. Install pyinstaller: `cd ..; python3 setup.py install`
    7. `git clone https://github.com/TaiBON/checklister`
    8. `make binary; sudo cp dist/checklister /usr/local/bin/`

### How to use

![點選物種加入名錄清單中](https://raw.github.com/TaiBON/checklister/master/docs/NGenerator_v0.2.1.png)

有兩個方式可以建立物種名錄，第一個是手動一個個搜尋物種加入清單：

1. 在主畫面中，先選擇物種清單資料表(例：data/twnamelist_apg3.csv)、預計要輸出名錄的檔案(例：/path/to/mylist.docx)、
物種中名暫存檔等
2. 在中文俗名的文字輸入方塊中，只需要打該物種的中文名前幾個字即可在下方列出包含該字元的物種(輸入中名或學名皆可)，
點選後「加入清單」則會加到候選清單中
3. 若需要刪除，可以選擇想刪除的項目刪除
4. 確認無誤後，按下「產生名錄」即可

第二個方法則是批次產生名錄檔案，和第一方法步驟 1 相同，選擇好物種清單資料表以及輸出名錄的檔案，
再選擇要批次匯入的 csv 檔案(UTF-8 編碼，一個物種一行)，然後程式會自動將查詢批次匯入的物種科名、學名等，
若該物種不存在資料庫中則會出現警告及提示。最後再按下「產生名錄」即可。

#### 文字介面參數 (genlist.py)
```
-d 代表物種名彙資料表
-s 代表需產生名錄的物種中名
-f 檔案格式，預設會同時產生 markdown (md) 文字檔與 pandoc 所支援的檔案格式(例如 docx)
-o 輸出名錄檔案檔名，例如 output (不用加附檔名)
```

將您要產生的物種名錄存成 txt 或 csv 檔案(每個物種一行，以 UTF-8 編碼)，例如：

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

![存成 UTF-8](https://raw.github.com/TaiBON/checklister/master/docs/save_namelist.png)

### 輸出範例

![Demo docx](https://raw.github.com/TaiBON/checklister/master/demo/demo_docx.png)

### Synonyms 同物異名或同名異物
namelist-generator 完全依賴 baselist (也就是 data/twnamelist.* )，所以只要 baselist 裡頭資料正確，產生的名錄即為正確名錄。
但仍會有一些中名相同的問題需要修正，
例如：

紫草科和禾本科中名皆有狗尾草，此時則需判斷是否為 _Heliotropium indicum_ 或 _Setaria viridis_。

發現資料檔案(twnamelist_apg3.csv & twnamelist.csv)有錯誤或是有使用上的問題歡迎直接 email 問我(mutolisp _AT_ gmail)

### LICENSE
python, shell script 等採用 GPL v3
資料檔(即 *.csv, *.db)採用 public domain


### Discussion Group

[Facebook "checklist generator"](https://www.facebook.com/groups/1491667327794847/)
