# 研招网院校库和专业信息爬取


### 说明
1. `main.py`脚本：从研招网院校库爬取院校信息并标注A区或B区和学校是否是985或211院校
2. `getExamSubjects.py`脚本：获取某个学校某个专业考试和招生人数信息

### 参考资料
```angular2html
A、B区：https://yzc.hsi.com.cn/kyzx/jybzc/202009/20200904/1972918872.html
211工程名单：http://www.moe.gov.cn/srcsite/A22/s7065/200512/t20051223_82762.html
985工程名单：http://www.moe.gov.cn/srcsite/A22/s7065/200612/t20061206_128833.html
```
整理后的学校目录在：[eduList.py](uinnfo/eduList.py)

### 整理资料下载

一般情况下只需要下载其中一个就好了

[院校库.xlsx](https://github.com/xx025/yzw-spider/raw/main/documentation/%E9%99%A2%E6%A0%A1%E5%BA%93.xlsx)

[院校库(edudata.json)](https://github.com/xx025/yzw-spider/raw/main/documentation/edudata.json)

### 在线脚本
在此之前我也写了一个油猴脚本：前往[安装](https://greasyfork.org/zh-CN/scripts/423952)

### 其他

[github搜索'考研'](https://github.com/search?q=%E8%80%83%E7%A0%94)

---
请慎重对待和使用，程序逻辑可能产生了错误的结果，请您仔细详查院校信息

