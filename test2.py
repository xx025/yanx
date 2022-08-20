from con_db import cur

shenfenxianzhi = ['辽宁省', '北京市']

data = []
for i in shenfenxianzhi:
    cursor = cur.execute("SELECT *  FROM zhaoshengyuanxiao where local=?", (i,))
    [data.append(i) for i in cursor]

for i in data:
    print(i)

# for i in data:
#     u1 = get_majors_of_edu(url=i[-1])
#     u1.req_data()
