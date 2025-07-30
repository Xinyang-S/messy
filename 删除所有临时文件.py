#!/usr/bin/env python3
import os
from typing import List
from utils.logger_config import get_logger

# 使用前面已有的日志器
log = get_logger("myapp")

# 临时文件后缀列表
TARGET_SUFFIXES = (
    ".$ea.user.mtime",
    ".$ea.user.orictime",
    ".$ea.user.redundancy",
)

def _should_delete(filename: str) -> bool:
    """判断文件是否以指定后缀结尾"""
    return any(filename.endswith(suffix) for suffix in TARGET_SUFFIXES)

def clean_and_list_files(root_path: str) -> List[str]:
    """
    扫描 root_path 下所有文件，删除匹配后缀的文件，返回删除后的文件完整路径列表。
    :param root_path: 要扫描的根目录
    :return: 删除后剩余文件的绝对路径列表（按字典序）
    """
    if not os.path.isdir(root_path):
        raise log.warning(f"路径不存在或不是目录: {root_path}")

    # 用于存储所有文件路径
    all_files = []

    # 遍历获取所有文件完整路径
    for root, dirs, files in os.walk(root_path):
        for file in files:
            full_path = os.path.join(root, file)
            all_files.append(full_path)

    remaining_files = []
    deleted_count = 0
    for file_path in all_files:
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        full_path = os.path.join(dir_name, base_name)
        if _should_delete(base_name):
            try:
                os.remove(full_path)
                deleted_count += 1
                log.info(f"[DELETED] {full_path}")
            except Exception as e:
                log.warning(f"[ERROR] 无法删除 {full_path}: {e}")
        else:
            remaining_files.append(full_path)

    log.info(f"\n扫描完成，共删除 {deleted_count} 个文件，剩余 {len(remaining_files)} 个文件")
    return sorted(remaining_files)


if __name__ == "__main__":
    path = r"E:\恢复"
    file_list = clean_and_list_files(path)