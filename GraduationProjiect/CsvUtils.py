# CSV文件工具类，负责加载和生成CSV文件

# 读文件，返回文件的每一行
def loadFile(filename):
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i == 0:  # 去掉文件第一行的title
                continue
            yield line.strip('\r\n')
    print('Load %s success!' % filename)