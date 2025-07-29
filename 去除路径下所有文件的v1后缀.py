import os
import time

from utils.logger_config import get_logger

# 任何地方直接获取同一个 logger
log = get_logger("myapp")

def process_path(input_path):
    """
    处理指定路径下的所有文件，重命名.v数字后缀的文件
    :param input_path: 要处理的根路径
    """
    if not os.path.exists(input_path):
        log.warning(f"路径不存在: {input_path}")
        return

    # 用于存储所有文件路径
    all_files = []

    # 遍历获取所有文件完整路径
    for root, dirs, files in os.walk(input_path):
        for file in files:
            full_path = os.path.join(root, file)
            all_files.append(full_path)

    # log.info("发现以下文件：")
    # for file in all_files:
    #     log.info(file)

    # 处理需要重命名的文件
    renamed_count = 0
    for file_path in all_files:
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)

        # 检查是否以.v数字结尾
        dot_index = base_name.rfind('.')
        if dot_index != -1:
            suffix = base_name[dot_index:]
            # 检查是否是.v1, .v2等格式
            if suffix.startswith('.v') and suffix[2:].isdigit():
                new_name = base_name[:dot_index]
                new_path = os.path.join(dir_name, new_name)

                try:
                    os.rename(file_path, new_path)
                    log.info(f"重命名: {file_path} -> {new_path}")
                    renamed_count += 1
                except Exception as e:
                    log.info(f"重命名失败: {file_path} -> {new_path}, 错误: {e}")

    log.info(f"\n处理完成！共重命名 {renamed_count} 个文件")


if __name__ == "__main__":
    # 获取用户输入
    path = r"E:\恢复"
    # 处理路径
    process_path(path)
