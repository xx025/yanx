### 前往默认分支：

[YanX-研招网硕士专业目录下载](https://github.com/xx025/YanX)


----
**打包**：
```shell
pyinstaller -D -w -i favicon.ico main.py --add-data "favicon.ico;.\\" 
```

```shell

pip install pipreqs
```

```shell

pipreqs  --encoding=utf8 --force
```


---

v3.1.15
> 下载 YanX_Setup_*.exe 安装 打开运行
>- 注意：文件导出到桌面，导出文件为CSV格式，这个文件可用Excel打开（WPS亦可）

**更新：**
单独选择某个省市地区
修正对院校库不存在的院校专业输出
去掉同时导出多个
保留所有列信息
