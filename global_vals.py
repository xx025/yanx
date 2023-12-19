# 定义全局变量
import random

# 通过session 存储的数据 不知道稳什么丢失了一部分


global_vals = dict(
    mllb={},  # 门类代码
    xklb={},  # 学科类别
    save_name=''  # 保存的文件名
)


# 产生一个15000-25535 的高位随机端口
port = random.randint(15000, 25535)
