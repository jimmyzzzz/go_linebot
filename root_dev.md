
# root級開發者指南

目錄
1. 測試環境
2. 用戶指令
3. c-root 開發
4. python-root 開發

## 測試環境介紹

測試環境是為在上線到line之前給開發者除錯或測試而生的，使用命令行來運行測試環境:

```bash
python run_script.py demo.txt
```

### 對話文件

其中demo.txt為模擬用戶對話的腳本文件，下面是demo.txt的範例:
```

# l123 r123
今天天氣不錯！
可以出去打球

# l456 r123
沒錯～
# l456

機器人你好！
```

對話內容按順序輸入到line-bot中，下面line-bot接收到的具體內容。

用戶(賴id`l123`)，在房間(房間id`r123`)說道:
```
今天天氣不錯！\n可以出去打球\n\n
```

用戶(賴id`l456`)，在房間(房間id`r123`)說道:
```
沒錯～
```

用戶(賴id`l456`)，私訊line-bot說道:
```
\n機器人你好！
```

可以發現以`#`開頭的行用來表示用戶的基本資料，在`#`之間的所有行內容會被表示為用戶在line中的輸入對話，包括空白的行。並且最後一筆對話的範圍為`#`開頭行的下一行開始，到文件結尾為結束。

`＃`行的第一段文字為用戶的line-id，而不是用戶在賴上的名字。第二段文字為該對話所在的房間id，而不是房間在賴上的名字，且第二段為選填，如果沒填則視該段對話為用戶私訊line-bot的內容。

### 指令說明

可以使用`-h`選項來查看幫助:
```bash
python run_script.py -h
```

可以按順序一次測試多個對話文件:
```bash
python run_script.py demo1.txt demo2.txt
```

也可以用`-k`選項將kernal和root狀態保存至指定文件，方便下次運行時直接以上次的狀態接續運行。如果指定的文件已經存在，則會讀取該文件保存的keranl和root狀態來運行，並在結束時將新的狀態更新回原文件中。
```bash
python run_script.py demo1.txt -k=stat.pk
```

`注意:`保存root的狀態目前僅對python-root有效。


## 用戶指令介紹

用戶指令可以分為`短指令`跟`長指令`，短指令可以看成是長指令的一種簡化形式，短指令在實際運作中為被專門的kernal擷取並轉化成長指令，並重新被解析一次。

目前支援的短指令類型有:
1. $指令: 用於切換模式(`mod`)
2. !指令: 用於執行命令
3. ?指令: 用於為用戶提供使用幫助

目前支援的長指令類型只有`%指令`，也就是說目前所有的短指令最終都會被轉成長指令的形式然後才被kernal解析並執行。而目前用於轉換短指令的keranl為`dollar_kernal.DollarKernal`類的實例，該kernal為`HalfKernal`，可以通過`dk`模式來與其互動。

下面是短指令轉換成成指令的格式範例，我們預設用戶所在的模式為`env`。(切換模式可以通過指令:`$ mod env`)

### 指令轉換

---

$短指令:
```
$ uid jimmy
```
轉換後的長指令:
```
% dk :  uid jimmy %
```
---

!短指令:
```
! show hello, world
```
轉換後的長指令:
```
% env :  show hello, world %
```
---

?短指令:
```
? show
```
轉換後的長指令:
```
% env %
help: show
```
---

### 指令拆解

當用戶輸入了指令後，等到達root時會被root解析並拆解成func-cmd的形式。下面是範例:

指令內容:
```
% env : this is root cmd %
func1 : this is user cmd1
func2 : this is user cmd2
```

被拆解成:
1. root-cmd，內容為:`this is root cmd`
2. user-cmd，函數名為:`func1`，輸入為:`this is user cmd1`
3. user-cmd，函數名為:`func2`，輸入為:`this is user cmd2`

而當拆解完成後就會對名為`env`的root進行呼叫，並依次:
1. 輸入root-cmd: `this is root cmd`
2. 呼叫函數func1: `this is user cmd1`
3. 呼叫函數func2: `this is user cmd2`

## c root 開發介紹

所有的c-root須被編譯成`.so`文件並放置在`./CKeranl_root`資料夾內，如果kernal沒有在該資料夾內發現名為`env`的so文件則會失敗。

編譯指令可以使用:
```bash
gcc -fPIC -shared -o Sample.so Sample.c
```

### kernal-root運作介紹

負責c-root的kernal為`c_kernal.py`下的`CKernal`的實例。實際上，在keranl找尋`.so`文件後會通過`c_root_wrapper.py`中的`c_root_wapper`類來將其包裝成一個root來使用。目前支援兩種kernal-root運作流程，分別是:
1. SampleCKernal+sample_c_root_wapper
2. CKernal+c_root_wapper

兩種模式的差異在於root_wapper會不會自動執行`指令拆解`，sample_c_root_wapper並不會自動幫開發者完成指令拆，需要開法者自己去解析user-cmd。但這也給了開發者更多自由度，而不需要受限於給定的func-cmd的形式。

目前僅支援CKernal+c_root_wapper，kernal的工作目錄在`./CKeranl_root`。

目前並沒有SampleCKernal+sample_c_root_wapper的流程運作實例，如需要添加可以修改文件`init_kernal.py`中的kernal樹，來添加SampleCKernal的實例，並指定一個kernal的工作目錄。

### 呼叫流程

下面分別針對兩種kernal-root運作流程來介紹其root呼叫流程:

SampleCKernal+sample_c_root_wapper:

1. 呼叫 get_user_id 函數
2. 呼叫 get_group_id 函數
3. 呼叫 get_uid 函數
4. 呼叫 get_root_cmd 函數
5. 呼叫 get_user_cmds 函數
6. 呼叫 root_return 函數

CKernal+c_root_wapper:

1. 呼叫 get_user_id 函數
2. 呼叫 get_group_id 函數
3. 呼叫 get_uid 函數
4. 呼叫 get_root_cmd 函數
5. 呼叫 run_start 函數
6. 依序呼叫 user-cmd 中呼叫的函數
7. 呼叫 run_end 函數
8. 呼叫 root_return 函數


所有的函數都會被傳入一個`char`類型的指針，並且需要回傳一個`char`類型的指針。下面以一個使用CKernal+c_root_wapper的實際例子來認識呼叫流程。

用戶(line-id='a1b2c3', uid='jimmy')在房間(id='r4556')中輸入指令為:
```
% env : root cmd %
f1:  this is first cmd
f2 : this is second cmd
```
呼叫流程:

1. 呼叫 get_user_id 函數。若該函數呼叫成功，傳入'a1b2c3'，回傳值會被忽略。若該函數呼叫失敗，則被忽略。
2. 呼叫 get_group_id 函數。若該函數呼叫成功，傳入'r4556'，回傳值會被忽略。若該函數呼叫失敗，則被忽略。
3. 呼叫 get_uid 函數。若該函數呼叫成功，傳入'jimmy'，回傳值會被忽略。若該函數呼叫失敗，則被忽略。
4. 呼叫 get_root_cmd 函數。若該函數呼叫成功，傳入'root cmd'，回傳值會被忽略。若該函數呼叫失敗，則被忽略。
5. 呼叫 run_start 函數。若該函數呼叫成功，傳入' '，回傳值會被忽略。若該函數呼叫失敗，則被忽略。
6. 呼叫 f1 函數。若該函數呼叫成功，傳入'this is first cmd'，回傳值會被忽略。若該函數呼叫失敗，則呼叫流程直接停止並顯示錯誤訊息。
7. 呼叫 f2 函數。若該函數呼叫成功，傳入'this is second cmd'，回傳值會被忽略。若該函數呼叫失敗，則呼叫流程直接停止並顯示錯誤訊息。
8. 呼叫 run_end 函數。若該函數呼叫成功，傳入' '，回傳值會被忽略。若該函數呼叫失敗，則被忽略。
9. 呼叫 root_return 函數。若該函數呼叫成功，傳入' '，回傳值會被顯示給用戶。若該函數呼叫失敗，則呼叫流程直接停止並顯示錯誤訊息。

### 呼叫函數

下面介紹呼叫函數的其他細節。

#### get_group_id

當用戶在房間內下指令時會輸入房間的id，而當用戶是私訊line-bot時，則會輸入'PERSON_ROOM'。

#### get_uid

當沒有找到用戶的uid時會輸入''，但是這通常不會發生，`DollarKernal`會在用戶第一次使用時就給其一個預設的用戶名，通常是'new_user_{id}'的格式。

#### get_root_cmd

用戶可能會有3種形式的root-cmd呼叫，三種形式所會產生的輸入是不同的。

**類型一:無呼叫root-cmd**

如下:
```
% env %
```
輸入為: ''

**類型二:呼叫root-cmd但無輸入**

如下:
```
% env :  %
```
輸入為: ' '

**類型二:呼叫root-cmd且有輸入**

如下:
```
% env : this is root cmd %
```
輸入為: 'this is root cmd'，可以發現兩端的空白會被刪除。

#### user-cmd函數

如下:
```
% env %
f1: this is a cmd
```
輸入f1函數的內容為: 'this is a cmd'，可以發現兩端的空白會被刪除。

## python root 開發介紹

敬請期待。