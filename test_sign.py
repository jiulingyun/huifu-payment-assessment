# -*- coding: utf-8 -*-
"""
签名功能测试脚本
用于验证RSA密钥配置是否正确

注意：本项目使用汇付官方SDK，SDK会自动处理签名和验签。
此脚本仅用于验证密钥文件配置是否正确。
"""

from config import PRIVATE_KEY, HUIFU_PUBLIC_KEY
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64


def sign_data(data: str, private_key_pem: str) -> str:
    """使用私钥签名数据"""
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    
    signature = private_key.sign(
        data.encode('utf-8'),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    return base64.b64encode(signature).decode('utf-8')


def verify_signature(data: str, signature: str, public_key_pem: str) -> bool:
    """使用公钥验证签名"""
    try:
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8'),
            backend=default_backend()
        )
        
        signature_bytes = base64.b64decode(signature)
        
        public_key.verify(
            signature_bytes,
            data.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


def test_sign():
    """测试签名和验签功能"""
    print("="*60)
    print("测试 RSA 密钥配置")
    print("="*60)
    
    print("\n【密钥说明】")
    print("根据汇付文档，您配置的密钥包括：")
    print("  1. sys_id 私钥 - 您的商户私钥（用于签名请求）")
    print("  2. sys_id 汇付公钥 - 汇付的公钥（用于验签汇付的响应）")
    print("\n⚠️ 注意：这两个密钥不是一对，所以不能直接互相验签")
    print("       实际使用时，您用私钥签名请求，汇付用您的公钥验签")
    print("       SDK会自动处理签名和验签过程")
    
    # 测试数据
    test_data = "test_message_for_signature_verification"
    
    print("\n" + "="*60)
    print("【测试1：验证私钥配置】")
    print("="*60)
    
    try:
        if not PRIVATE_KEY or len(PRIVATE_KEY) < 100:
            print("❌ 私钥未正确配置")
            return
        
        print("✅ 私钥已加载")
        print(f"私钥长度: {len(PRIVATE_KEY)} 字符")
        
        # 测试签名
        print("\n正在使用您的私钥签名测试数据...")
        signature = sign_data(test_data, PRIVATE_KEY)
        print(f"✅ 签名成功！")
        print(f"签名结果（前50字符）: {signature[:50]}...")
        
        # 从私钥提取公钥进行自验证
        print("\n" + "="*60)
        print("【测试2：自验证签名】")
        print("="*60)
        print("\n从您的私钥中提取公钥进行自验证...")
        
        # 加载私钥
        private_key = serialization.load_pem_private_key(
            PRIVATE_KEY.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
        
        # 从私钥提取公钥
        public_key = private_key.public_key()
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        
        # 用提取的公钥验签
        is_valid = verify_signature(test_data, signature, public_key_pem)
        
        if is_valid:
            print("✅ 自验证成功！您的私钥可以正常签名。")
        else:
            print("❌ 自验证失败！私钥可能有问题。")
        
        # 显示汇付公钥信息
        print("\n" + "="*60)
        print("【测试3：验证汇付公钥配置】")
        print("="*60)
        print("\n汇付公钥配置：")
        if HUIFU_PUBLIC_KEY and len(HUIFU_PUBLIC_KEY) > 100:
            print("✅ 汇付公钥已配置")
            print(f"公钥长度: {len(HUIFU_PUBLIC_KEY)} 字符")
            print("该公钥用于验证汇付返回的响应签名")
            print("（SDK会自动使用此公钥验证响应）")
        else:
            print("❌ 汇付公钥未正确配置")
            is_valid = False
        
        print("\n" + "="*60)
        print("【测试总结】")
        print("="*60)
        if is_valid:
            print("\n✅ 密钥配置正确！")
            print("\n可以开始使用：")
            print("  • 您的私钥会用于签名API请求（SDK自动处理）")
            print("  • 汇付的公钥会用于验证API响应（SDK自动处理）")
            print("\n运行主程序: python main.py")
        else:
            print("\n❌ 密钥配置有问题，请检查：")
            print("  • 确认私钥是完整的 sys_id 私钥")
            print("  • 确认公钥是完整的 sys_id 汇付公钥")
            print("  • 检查密钥文件格式是否正确")
            
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        print("\n请检查密钥文件配置是否正确。")
        print("提示：")
        print("  1. 确认 keys/private_key.txt 包含完整的私钥")
        print("  2. 确认 keys/public_key.txt 包含完整的汇付公钥")
        print("  3. 可以是纯 base64 格式或 PEM 格式")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_sign()
