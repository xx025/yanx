# 研招网院校库和专业信息爬取

### 说明

1. [`main.py`](main.py)脚本：从研招网院校库爬取院校信息并标注A区或B区和学校是否是985或211院校,文件输出在[`uinnfo/edudata.json`](uinnfo/edudata.json)
2. [`get_college_majors.py`](get_college_majors.py)脚本：获取某个学校某类专业目录,输出json文件保存至[`university_majors/`](university_majors/)
3. [`get_college_majors_exam_scope.py`](get_college_majors_exam_scope.py)
   获取某个学校的具体专业的考试科目招生人数等一些备注信息,文件输出在[`college_majors_exam_scope/`](college_majors_exam_scope/)
4. 其他
    - [`rtcookies.py`](rtcookies.py) 借助selenium实时获取新的cookies、
    - [`output_excel.py`](output_to_excel/yxk.py)将[`main.py`](main.py)脚本输出文件整理成表格形式,
    - [`uinnfo/`](uinnfo/)包含大学的名单列表和一个效验脚本，
    - [`university_majors_url/umu.json`](university_majors_url/umu.json)在(3）运行时生成一个保存保存考试范围链接的中间文件
    - [`output_to_excel/major_exam_info.py`](output_to_excel/major_exam_info.py)将院校专业详细信息输出到表格
### 参考资料

```angular2html
A、B区：https://yzc.hsi.com.cn/kyzx/jybzc/202009/20200904/1972918872.html
211工程名单：http://www.moe.gov.cn/srcsite/A22/s7065/200512/t20051223_82762.html
985工程名单：http://www.moe.gov.cn/srcsite/A22/s7065/200612/t20061206_128833.html
```

整理后的学校目录在：[eduList.py](uinnfo/loc_ab_uni_985211.py)

### 整理资料下载

一般情况下只需要下载点击下载就好了

1. 全部院校[院校库.xlsx](documentation/院校库.xlsx)

   ![](https://cdn.jsdelivr.net/gh/xx025/cloudimg/img/20210329220249.png)

2. 重点院校（985，211）0812专业详细信息:[院校专业0812.xlsx](documentation/院校专业0812.xlsx)
   
   ![](https://cdn.jsdelivr.net/gh/xx025/cloudimg/img/20210329220536.png)

### 在线脚本

在此之前我也写了一个油猴脚本：前往[安装](https://greasyfork.org/zh-CN/scripts/423952)

### 其他

[github搜索'考研'](https://github.com/search?q=%E8%80%83%E7%A0%94)

---
请慎重对待和使用，程序逻辑可能产生了错误的结果，请您仔细详查院校信息

