# -*- coding: utf-8 -*-
"""
汇付商户考核配置文件
"""

import os

# 尝试加载 .env 文件（如果存在且安装了 python-dotenv）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # 如果没有安装 python-dotenv，跳过（不影响使用系统环境变量）
    pass

# 商户信息（从环境变量读取，如果未设置则使用默认值）
HUIFU_ID = os.getenv("HUIFU_ID", "")  # 商户号
SYS_ID = os.getenv("SYS_ID", "")  # 系统号
PRODUCT_ID = os.getenv("PRODUCT_ID", "")  # 产品号
USER_ID = os.getenv("USER_ID", "")  # 用户ID

# 密钥文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRIVATE_KEY_FILE = os.path.join(BASE_DIR, "keys", "private_key.txt")
PUBLIC_KEY_FILE = os.path.join(BASE_DIR, "keys", "public_key.txt")


def load_key_file(file_path, key_type='private'):
    """
    读取密钥文件，自动处理PEM格式
    
    :param file_path: 密钥文件路径
    :param key_type: 密钥类型，'private' 或 'public'
    :return: PEM格式的密钥字符串
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"密钥文件不存在: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # 检查是否已经是PEM格式（包含BEGIN标记）
    if '-----BEGIN' in content:
        return content
    
    # 如果是纯base64字符串，自动添加PEM格式标记
    print(f"检测到纯base64格式密钥，自动转换为PEM格式...")
    
    # 移除所有空白字符和换行符
    clean_content = ''.join(content.split())
    
    # 按照标准PEM格式，每64字符一行
    formatted_lines = []
    for i in range(0, len(clean_content), 64):
        formatted_lines.append(clean_content[i:i+64])
    
    # 添加PEM头尾标记
    if key_type == 'private':
        pem_content = '-----BEGIN PRIVATE KEY-----\n'
        pem_content += '\n'.join(formatted_lines)
        pem_content += '\n-----END PRIVATE KEY-----'
    else:  # public
        pem_content = '-----BEGIN PUBLIC KEY-----\n'
        pem_content += '\n'.join(formatted_lines)
        pem_content += '\n-----END PUBLIC KEY-----'
    
    return pem_content


# RSA 私钥（sys_id 私钥）
# 从文件 keys/private_key.txt 读取
# 支持PEM格式或纯base64格式，程序会自动处理
try:
    PRIVATE_KEY = load_key_file(PRIVATE_KEY_FILE, key_type='private')
except FileNotFoundError as e:
    print(f"警告: {e}")
    print("请将您的私钥内容保存到 keys/private_key.txt 文件中")
    print("支持两种格式：")
    print("  1. 完整PEM格式（包含 -----BEGIN/END----- 标记）")
    print("  2. 纯base64字符串（程序会自动添加PEM格式标记）")
    PRIVATE_KEY = ""

# RSA 汇付公钥（sys_id 汇付公钥）
# 从文件 keys/public_key.txt 读取
# 支持PEM格式或纯base64格式，程序会自动处理
try:
    HUIFU_PUBLIC_KEY = load_key_file(PUBLIC_KEY_FILE, key_type='public')
except FileNotFoundError as e:
    print(f"警告: {e}")
    print("请将汇付公钥内容保存到 keys/public_key.txt 文件中")
    print("支持两种格式：")
    print("  1. 完整PEM格式（包含 -----BEGIN/END----- 标记）")
    print("  2. 纯base64字符串（程序会自动添加PEM格式标记）")
    HUIFU_PUBLIC_KEY = ""

# 注意：使用SDK版本时，API地址由SDK自动管理，无需手动配置

