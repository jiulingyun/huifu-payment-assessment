# -*- coding: utf-8 -*-
"""
配置向导脚本
帮助用户快速配置 config.py
"""

import os


def print_banner():
    """打印横幅"""
    print("\n" + "="*60)
    print(" " * 18 + "汇付商户配置向导")
    print("="*60)


def main():
    """配置向导主函数"""
    print_banner()
    
    print("\n欢迎使用配置向导！")
    print("本向导将帮助您配置商户信息和RSA密钥")
    
    # 读取当前配置
    config_file = "config.py"
    if not os.path.exists(config_file):
        print(f"\n❌ 错误: 找不到 {config_file} 文件")
        return
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config_content = f.read()
    
    print("\n" + "="*60)
    print("当前商户信息:")
    print("="*60)
    print("商户号 (huifu_id): 6666000109133323")
    print("系统号 (sys_id):   6666000108840829")
    print("产品号 (product_id): YYZY")
    print("用户ID:           1435964137120268288")
    
    print("\n" + "="*60)
    print("密钥配置:")
    print("="*60)
    
    # 检查私钥
    if "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgw" in config_content:
        print("⚠️  私钥: 未配置（示例值）")
    else:
        print("✅ 私钥: 已配置")
    
    # 检查公钥
    if "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkmF" in config_content:
        print("⚠️  公钥: 未配置（示例值）")
    else:
        print("✅ 公钥: 已配置")
    
    print("\n" + "="*60)
    print("配置步骤:")
    print("="*60)
    
    print("\n1️⃣  获取密钥:")
    print("   - 登录汇付商户平台")
    print("   - 进入「开发配置」→「密钥管理」")
    print("   - 找到 sys_id = 6666000108840829")
    print("   - 下载或复制对应的私钥和汇付公钥")
    
    print("\n2️⃣  配置私钥:")
    print("   - 编辑文件: keys/private_key.txt")
    print("   - 直接粘贴从汇付平台复制的纯 base64 字符串即可")
    print("   - 程序会自动添加 PEM 格式标记，无需手动操作")
    
    print("\n3️⃣  配置公钥:")
    print("   - 编辑文件: keys/public_key.txt")
    print("   - 直接粘贴汇付公钥的纯 base64 字符串即可")
    print("   - 同样支持自动格式转换")
    
    print("\n4️⃣  支持的格式:")
    print("   - 格式1: 纯 base64 字符串（推荐，直接复制粘贴）")
    print("   - 格式2: 完整 PEM 格式（包含 -----BEGIN/END----- 标记）")
    print("   - 程序会自动检测并处理")
    
    print("\n5️⃣  测试配置:")
    print("   - 保存文件后运行: python test_sign.py")
    print("   - 看到「签名验证成功」表示配置正确")
    
    print("\n" + "="*60)
    print("密钥格式示例:")
    print("="*60)
    
    print("\n【方式1：纯 base64 字符串（推荐）】")
    print("直接从汇付平台复制，无需添加任何标记：")
    print("""
keys/private_key.txt 内容:
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDJ...（一长串）

keys/public_key.txt 内容:
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy8Dbv...（一长串）
""")
    
    print("\n【方式2：完整 PEM 格式】")
    print("如果密钥包含 BEGIN/END 标记，也支持：")
    print("""
keys/private_key.txt 内容:
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDJ...
（多行）
-----END PRIVATE KEY-----
""")
    
    print("="*60)
    print("⚠️  注意事项:")
    print("="*60)
    print("• 支持纯 base64 和 PEM 两种格式，程序会自动识别")
    print("• 推荐直接复制粘贴 base64 字符串，最简单")
    print("• 确保使用正确的 sys_id 对应的密钥")
    print("• 妥善保管私钥，不要泄露")
    
    print("\n✅ 配置完成后，运行主程序:")
    print("   python main.py")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()

