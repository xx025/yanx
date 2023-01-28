### 前往默认分支：

[YanX-研招网硕士专业目录下载](https://github.com/xx025/YanX)



**Github下载**



**蓝奏云下载**
https://wwqg.lanzouf.com/b00qky81a
密码:37md



----
**打包**：
```shell
pyinstaller -D -w -i favicon.ico main.py --add-data "favicon.ico;.\\"  --add-data ".\\imgs\\*;.\\imgs"
```

```shell

pip install pipreqs
```

```shell

pipreqs  --encoding=utf8 --force
```



---
v3.1.28
**更新**
安装包不再负载数据库文件，数据库安装后第一次打开时创建
数据库中院校库在第一次下载时下载，当研招网出现新的年份时会更新院校库




---

v3.1.15

**更新：**
单独选择某个省市地区
修正对院校库不存在的院校专业输出
去掉同时导出多个
保留所有列信息
