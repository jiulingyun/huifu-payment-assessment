# -*- coding: utf-8 -*-
"""
使用汇付官方Python SDK的API封装
文档: https://paas.huifu.com/open/doc/devtools/#/sdk_python
SDK名称: dg-sdk
"""

import json
import time
from datetime import datetime

try:
    import dg_sdk
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    print("警告: 汇付SDK未安装，请运行: pip install dg-sdk==v2.0.10")

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

from config import *


class HuifuSDKAPI:
    """汇付支付SDK API客户端"""
    
    def __init__(self):
        """初始化SDK客户端"""
        if not SDK_AVAILABLE:
            raise ImportError("汇付SDK未安装，请运行: pip install dg-sdk==v2.0.10")
        
        self.huifu_id = HUIFU_ID
        self.sys_id = SYS_ID
        self.product_id = PRODUCT_ID
        self.user_id = USER_ID
        
        # 根据文档初始化SDK
        # 使用 dg_sdk.MerConfig 配置商户参数（位置参数）
        # 文档示例：MerConfig(private_key, public_key, sys_id, product_id, huifu_id)
        # 但如果报错说参数太多，尝试只传4个：private_key, public_key, sys_id, product_id
        # huifu_id 会在请求对象上单独设置
        try:
            # 先尝试5个参数（按文档）
            dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(
                PRIVATE_KEY,
                HUIFU_PUBLIC_KEY,
                SYS_ID,
                PRODUCT_ID,
                HUIFU_ID
            )
        except TypeError:
            # 如果5个参数失败，尝试4个参数
            dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(
                PRIVATE_KEY,
                HUIFU_PUBLIC_KEY,
                SYS_ID,
                PRODUCT_ID
            )
        
        print("✅ 汇付SDK已初始化")
        print(f"   商户号: {HUIFU_ID}")
        print(f"   系统号: {SYS_ID}")
    
    def print_qr_code(self, url):
        """
        在终端中显示二维码
        
        :param url: 二维码链接
        """
        print(f"\n📱 支付二维码")
        print("="*60)
        
        if QRCODE_AVAILABLE:
            try:
                # 创建二维码对象
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=1,
                    border=1,
                )
                qr.add_data(url)
                qr.make(fit=True)
                
                # 生成矩阵，使用两个半角字符确保可扫描
                matrix = qr.get_matrix()
                print()  # 空行
                for row in matrix:
                    # 使用两个半角字符表示一个模块
                    line = ''.join(['██' if cell else '  ' for cell in row])
                    print(line)
                
                print()  # 空行
                
                print("="*60)
                print("💡 使用支付宝APP扫描上方二维码完成支付")
                print("="*60)
                
            except Exception as e:
                print(f"\n⚠️ 无法生成二维码: {e}")
                print(f"链接: {url}")
        else:
            print(f"\n⚠️ qrcode库未安装，请运行: pip install qrcode[pil]==7.4.2")
            print(f"链接: {url}")
    
    def generate_req_seq_id(self, prefix="PAY"):
        """
        生成请求流水号
        格式: 用户ID_日期_时间戳_前缀
        """
        date_str = datetime.now().strftime("%Y%m%d")
        timestamp = str(int(time.time() * 1000))[-6:]
        req_seq_id = f"{self.user_id}_{date_str}_{timestamp}_{prefix}"
        return req_seq_id
    
    def aggregate_pay(self, amount="1.00", auth_code=None):
        """
        聚合正扫支付（支付宝NATIVE扫码支付）- 使用dg-sdk
        
        :param amount: 支付金额（元），默认1.00
        :param auth_code: 支付授权码（可选，NATIVE支付不需要）
        :return: 支付结果
        """
        print("\n" + "="*50)
        print("开始执行聚合正扫支付（支付宝NATIVE扫码支付）...")
        print("="*50)
        
        # 生成请求流水号
        req_seq_id = self.generate_req_seq_id("PAY")
        req_date = datetime.now().strftime("%Y%m%d")
        
        # 根据文档，使用对象方法：创建请求对象
        request = dg_sdk.V3TradePaymentJspayRequest()
        
        # 设置请求参数
        request.req_seq_id = req_seq_id
        request.req_date = req_date
        request.huifu_id = self.huifu_id  # 商户号（在请求对象上设置）
        request.trade_type = "A_NATIVE"  # 支付宝NATIVE扫码支付
        request.trans_amt = amount
        request.goods_desc = "汇付商户考核测试"
        
        # NATIVE支付不需要auth_code，如果提供了则设置（兼容其他支付方式）
        if auth_code:
            request.auth_code = auth_code
        
        print(f"\n请求参数:")
        print(f"  req_seq_id: {req_seq_id}")
        print(f"  请求日期: {req_date}")
        print(f"  商户号: {self.huifu_id}")
        print(f"  交易类型: A_NATIVE (支付宝NATIVE扫码支付)")
        print(f"  支付金额: {amount} 元")
        if auth_code:
            print(f"  授权码: {auth_code} (已提供，但NATIVE支付不需要)")
        else:
            print(f"  授权码: 无需（NATIVE支付会返回二维码）")
        
        try:
            # 根据文档，调用 request.post() 发送请求
            # extend_infos 是所有非必填字段字典，如果不需要可传空字典
            extend_infos = {}  # 空字典表示没有非必填字段
            # SDK会自动处理签名、HTTP请求、验签等
            response = request.post(extend_infos)
            
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            # 检查响应（汇付响应码：0000开头表示成功）
            resp_code = response.get("resp_code", "")
            resp_desc = response.get("resp_desc", "")
            trans_stat = response.get("trans_stat", "")
            
            print(f"\n响应分析:")
            print(f"  响应码: {resp_code}")
            print(f"  响应描述: {resp_desc}")
            print(f"  交易状态: {trans_stat}")
            
            # 检查是否有二维码（需要用户扫码支付）
            qr_code = response.get("qr_code", "")
            if qr_code:
                # 在终端显示二维码
                self.print_qr_code(qr_code)
            
            # 判断交易状态
            # P = 处理中, S = 成功, F = 失败, C = 关闭
            if trans_stat == "S":
                print("\n✅ 支付成功！（交易已完成）")
                print(f"   汇付流水号: {response.get('hf_seq_id', 'N/A')}")
                return response
            elif trans_stat == "P":
                # 订单处理中，直接返回响应
                return response
            elif resp_code.startswith("0000"):
                print("\n✅ 下单成功！")
                print(f"   汇付流水号: {response.get('hf_seq_id', 'N/A')}")
                if trans_stat:
                    print(f"   交易状态: {trans_stat} (需要等待支付完成)")
                return response
            else:
                error_code = resp_code or "未知"
                error_msg = resp_desc or "未知错误"
                print(f"\n❌ 支付失败: [{error_code}] {error_msg}")
                return response
                
        except Exception as e:
            print(f"\n❌ SDK调用异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def query_order(self, req_seq_id=None, req_date=None, hf_seq_id=None, party_order_id=None):
        """
        查询订单状态
        
        :param req_seq_id: 请求流水号（可选，但需要至少提供一个标识）
        :param req_date: 请求日期（YYYYMMDD格式），如果不提供则从req_seq_id中提取
        :param hf_seq_id: 汇付流水号（推荐使用）
        :param party_order_id: 商户单号（支付宝/微信订单号）
        :return: 订单查询结果
        """
        # 至少需要提供一个订单标识
        if not req_seq_id and not hf_seq_id and not party_order_id:
            print("❌ 错误：至少需要提供一个订单标识（req_seq_id、hf_seq_id 或 party_order_id）")
            return None
        
        # 提取或设置请求日期
        if req_seq_id and not req_date:
            # 从req_seq_id中提取日期，格式：user_id_YYYYMMDD_xxx
            parts = req_seq_id.split("_")
            if len(parts) >= 2:
                req_date = parts[1]
            else:
                # 如果无法提取，使用当前日期
                req_date = datetime.now().strftime("%Y%m%d")
        elif not req_date:
            # 如果只有hf_seq_id或party_order_id，使用当前日期
            req_date = datetime.now().strftime("%Y%m%d")
        
        print(f"\n查询订单状态...")
        if req_seq_id:
            print(f"  请求流水号: {req_seq_id}")
        if hf_seq_id:
            print(f"  汇付流水号: {hf_seq_id}")
        if party_order_id:
            print(f"  商户单号: {party_order_id}")
        print(f"  请求日期: {req_date}")
        
        try:
            # 检查是否有查询接口
            if not hasattr(dg_sdk, 'V3TradePaymentScanpayQueryRequest'):
                print("⚠️ SDK中没有找到订单查询接口")
                return None
            
            request = dg_sdk.V3TradePaymentScanpayQueryRequest()
            request.huifu_id = self.huifu_id
            request.req_date = req_date
            
            # 设置必填字段（至少一个）
            if req_seq_id:
                request.req_seq_id = req_seq_id
            
            # 通过 extend_infos 传递其他标识
            extend_infos = {}
            if hf_seq_id:
                extend_infos["hf_seq_id"] = hf_seq_id
            if party_order_id:
                extend_infos["party_order_id"] = party_order_id
            
            response = request.post(extend_infos)
            
            resp_code = response.get("resp_code", "")
            trans_stat = response.get("trans_stat", "")
            
            print(f"  响应码: {resp_code}")
            if resp_code == "21000000":
                print(f"  ⚠️ 错误：订单标识不足，请提供 hf_seq_id 或 party_order_id")
            print(f"  交易状态: {trans_stat}")
            if resp_code.startswith("0000"):
                print(f"  ✅ 查询成功")
                if trans_stat == "S":
                    print(f"  💰 支付已完成（成功）")
            
            return response
            
        except Exception as e:
            print(f"\n❌ 查询订单异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def wait_for_payment(self, req_seq_id=None, req_date=None, hf_seq_id=None, party_order_id=None, max_wait_time=300, poll_interval=3):
        """
        轮询等待支付完成
        
        :param req_seq_id: 请求流水号（可选）
        :param req_date: 请求日期（YYYYMMDD格式）
        :param hf_seq_id: 汇付流水号（推荐使用）
        :param party_order_id: 商户单号（可选）
        :param max_wait_time: 最大等待时间（秒），默认300秒（5分钟）
        :param poll_interval: 轮询间隔（秒），默认3秒
        :return: 支付结果，如果超时或失败返回None
        """
        print(f"\n开始轮询支付状态...")
        print(f"  最大等待时间: {max_wait_time}秒")
        print(f"  轮询间隔: {poll_interval}秒")
        
        start_time = time.time()
        poll_count = 0
        
        while True:
            poll_count += 1
            elapsed_time = time.time() - start_time
            
            if elapsed_time >= max_wait_time:
                print(f"\n⏰ 等待超时（已等待 {int(elapsed_time)} 秒）")
                return None
            
            print(f"\n[第 {poll_count} 次查询] 已等待 {int(elapsed_time)} 秒...")
            result = self.query_order(req_seq_id, req_date, hf_seq_id, party_order_id)
            
            if not result:
                time.sleep(poll_interval)
                continue
            
            resp_code = result.get("resp_code", "")
            trans_stat = result.get("trans_stat", "")
            
            # 如果返回21000000错误，说明参数不足，尝试只使用hf_seq_id
            if resp_code == "21000000" and hf_seq_id:
                print(f"  尝试仅使用汇付流水号查询...")
                result = self.query_order(hf_seq_id=hf_seq_id, req_date=req_date)
                if result:
                    resp_code = result.get("resp_code", "")
                    trans_stat = result.get("trans_stat", "")
            
            if resp_code.startswith("0000"):
                if trans_stat == "S":
                    print(f"\n✅ 支付成功！")
                    print(f"   汇付流水号: {result.get('hf_seq_id', 'N/A')}")
                    print(f"   支付金额: {result.get('trans_amt', 'N/A')} 元")
                    return result
                elif trans_stat == "F":
                    print(f"\n❌ 支付失败")
                    print(f"   失败原因: {result.get('resp_desc', '未知')}")
                    return result
                elif trans_stat == "C":
                    print(f"\n⚠️ 订单已关闭")
                    return result
                elif trans_stat == "P":
                    # 仍在处理中，继续轮询
                    print(f"   交易状态: P (处理中，继续等待...)")
                    time.sleep(poll_interval)
                    continue
                else:
                    # 未知状态，继续轮询
                    print(f"   交易状态: {trans_stat} (继续等待...)")
                    time.sleep(poll_interval)
                    continue
            else:
                # 查询失败，继续尝试
                print(f"   查询异常，继续尝试...")
                time.sleep(poll_interval)
                continue
    
    def refund(self, org_req_seq_id=None, org_req_date=None, org_hf_seq_id=None, party_order_id=None, refund_amt="1.00"):
        """
        交易退款 - 使用dg-sdk
        
        :param org_req_seq_id: 原交易请求流水号
        :param org_req_date: 原交易请求日期（YYYYMMDD格式）
        :param org_hf_seq_id: 原交易汇付流水号（可选）
        :param party_order_id: 原交易微信/支付宝商户单号（可选）
        :param refund_amt: 退款金额（元）
        :return: 退款结果
        """
        print("\n" + "="*50)
        print("开始执行交易退款（使用汇付dg-sdk）...")
        print("="*50)
        
        # 生成退款流水号
        req_seq_id = self.generate_req_seq_id("REFUND")
        req_date = datetime.now().strftime("%Y%m%d")
        
        # 根据文档，使用对象方法：创建退款请求对象
        request = dg_sdk.V3TradePaymentScanpayRefundRequest()
        
        # 设置基础请求参数
        request.req_seq_id = req_seq_id
        request.req_date = req_date
        request.huifu_id = self.huifu_id
        request.ord_amt = refund_amt  # 退款金额
        
        # 设置原交易日期（SDK请求对象支持的属性）
        if org_req_date:
            request.org_req_date = org_req_date
        
        # 原交易标识通过 extend_infos 传递
        extend_infos = {}
        if org_req_date:
            extend_infos["org_req_date"] = org_req_date  # 也可能需要在extend_infos中传递
        if org_req_seq_id:
            extend_infos["org_req_seq_id"] = org_req_seq_id
        if org_hf_seq_id:
            extend_infos["org_hf_seq_id"] = org_hf_seq_id
        if party_order_id:
            extend_infos["party_order_id"] = party_order_id
        
        # 验证必需参数：至少需要一个原交易标识，且必须有原交易日期
        if not org_req_date:
            print("❌ 错误：原交易请求日期（org_req_date）是必需的")
            return None
        
        if not org_req_seq_id and not org_hf_seq_id and not party_order_id:
            print("❌ 错误：至少需要提供一个原交易标识（org_req_seq_id、org_hf_seq_id 或 party_order_id）")
            return None
        
        print(f"\n请求参数:")
        print(f"  req_seq_id: {req_seq_id}")
        print(f"  请求日期: {req_date}")
        print(f"  商户号: {self.huifu_id}")
        if org_req_date:
            print(f"  原交易日期: {org_req_date}")
        print(f"  退款金额: {refund_amt} 元")
        print(f"\nextend_infos (原交易标识):")
        if extend_infos:
            for k, v in extend_infos.items():
                print(f"  {k}: {v}")
        else:
            print("  无")
        
        try:
            # 根据文档，调用 request.post() 发送请求
            # extend_infos 包含原交易标识等非必填字段
            # SDK会自动处理签名、HTTP请求、验签等
            response = request.post(extend_infos)
            
            print(f"\n响应结果:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            # 检查响应（汇付响应码：0000开头表示成功）
            resp_code = response.get("resp_code", "")
            resp_desc = response.get("resp_desc", "")
            
            if resp_code.startswith("0000"):
                print("\n✅ 退款成功！")
                print(f"   响应码: {resp_code}")
                print(f"   响应描述: {resp_desc}")
                print(f"   汇付流水号: {response.get('hf_seq_id', 'N/A')}")
                return response
            else:
                error_code = resp_code or "未知"
                error_msg = resp_desc or "未知错误"
                print(f"\n❌ 退款失败: [{error_code}] {error_msg}")
                return response
                
        except Exception as e:
            print(f"\n❌ SDK调用异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return None


# 如果SDK不可用，提示安装
if not SDK_AVAILABLE:
    raise ImportError("汇付SDK未安装，请运行: pip install dg-sdk==v2.0.10")

