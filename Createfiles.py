import os
import random

def generate_test_files(directory, file_count=20):
    # 确保目录存在，如果不存在则创建
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 生成指定数量和大小的文件
    for i in range(file_count):
        file_size = random.randint(5 * 1024, 100 * 1024 * 1024)  # 5KB to 100MB
        with open(os.path.join(directory, f"file_{i}.bin"), "wb") as file:
            file.write(os.urandom(file_size))

# 打印当前工作目录
print("当前工作目录:", os.getcwd())

# 生成文件
generate_test_files("test_files")
