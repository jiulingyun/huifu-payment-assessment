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
    try:
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
    except ValueError as e:
        error_msg = str(e)
        if "Could not deserialize key data" in error_msg or "unsupported" in error_msg.lower():
            raise ValueError("私钥格式错误：无法解析私钥数据。请检查密钥格式是否正确。") from e
        elif "password" in error_msg.lower():
            raise ValueError("私钥可能需要密码，但当前不支持密码保护的私钥。") from e
        else:
            raise ValueError(f"私钥解析失败：{error_msg}") from e
    except Exception as e:
        raise ValueError(f"签名失败：{str(e)}") from e


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
            print("\n💡 解决方案：")
            print("  1. 检查 keys/private_key.txt 文件是否存在")
            print("  2. 确认文件内容不为空")
            print("  3. 确认密钥内容完整（至少100字符）")
            return
        
        print("✅ 私钥已加载")
        print(f"私钥长度: {len(PRIVATE_KEY)} 字符")
        
        # 检查密钥格式
        has_begin_marker = "-----BEGIN" in PRIVATE_KEY
        has_end_marker = "-----END" in PRIVATE_KEY
        
        if has_begin_marker and has_end_marker:
            print("✅ 检测到PEM格式密钥")
        elif not has_begin_marker and not has_end_marker:
            print("✅ 检测到base64格式密钥（程序已自动转换）")
        else:
            print("⚠️ 警告：密钥格式可能不完整")
            print("   建议检查密钥文件是否包含完整的 BEGIN/END 标记")
        
        # 测试签名
        print("\n正在使用您的私钥签名测试数据...")
        signature = None
        try:
            signature = sign_data(test_data, PRIVATE_KEY)
            print(f"✅ 签名成功！")
            print(f"签名结果（前50字符）: {signature[:50]}...")
        except ValueError as e:
            print(f"\n❌ {str(e)}")
            print("\n💡 可能的原因：")
            print("  1. 密钥格式不正确（不是有效的RSA私钥）")
            print("  2. 密钥内容不完整（缺少部分字符）")
            print("  3. 密钥文件编码问题（应使用UTF-8编码）")
            print("  4. 密钥类型不匹配（需要RSA私钥，不是其他类型）")
            print("\n💡 解决方案：")
            print("  1. 从汇付平台重新下载 sys_id 私钥")
            print("  2. 确认复制时没有遗漏任何字符")
            print("  3. 如果使用base64格式，确保是完整的base64字符串")
            print("  4. 如果使用PEM格式，确保包含完整的 BEGIN/END 标记")
            return
        
        # 从私钥提取公钥进行自验证
        is_valid = False
        if signature:
            print("\n" + "="*60)
            print("【测试2：自验证签名】")
            print("="*60)
            print("\n从您的私钥中提取公钥进行自验证...")
            
            try:
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
            except Exception as e:
                print(f"❌ 自验证过程出错: {str(e)}")
                is_valid = False
        
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
            print("\n💡 解决方案：")
            print("  1. 检查 keys/public_key.txt 文件是否存在")
            print("  2. 确认文件内容不为空")
            print("  3. 从汇付平台下载 sys_id 汇付公钥")
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
            
    except ValueError as e:
        print(f"\n❌ 密钥格式错误: {str(e)}")
        print("\n💡 详细解决方案：")
        print("  1. 确认 keys/private_key.txt 包含完整的私钥")
        print("  2. 确认 keys/public_key.txt 包含完整的汇付公钥")
        print("  3. 支持两种格式：")
        print("     • 纯 base64 格式（程序会自动转换）")
        print("     • 完整 PEM 格式（包含 -----BEGIN/END----- 标记）")
        print("  4. 从汇付平台重新下载密钥，确保完整复制")
    except Exception as e:
        print(f"\n❌ 发生未知错误: {str(e)}")
        print("\n💡 请检查：")
        print("  1. 密钥文件是否存在且可读")
        print("  2. 密钥文件编码为 UTF-8")
        print("  3. 密钥内容完整且格式正确")
        print("\n如需查看详细错误信息，请检查上面的错误提示。")


if __name__ == "__main__":
    test_sign()
