# -*- coding: utf-8 -*-
"""
汇付商户考核 - 支付宝正扫+退款场景
使用汇付官方Python SDK
主程序
"""

import sys
from huifu_sdk_api import HuifuSDKAPI


def print_banner():
    """打印横幅"""
    print("\n" + "="*60)
    print(" " * 10 + "汇付商户考核自动化工具（SDK版本）")
    print(" " * 15 + "支付宝正扫 + 退款场景")
    print("="*60)


def print_instructions():
    """打印使用说明"""
    print("\n【考核要求】")
    print("1. 聚合正扫：调用聚合正扫API，trade_type = A_NATIVE")
    print("   - 向个人账户内支付 ≥ 1.00 元")
    print("   - 如需分账需设置分账相关参数")
    print("\n2. 交易退款：调用交易退款API")
    print("   - 将支付款退还给用户")
    print("   - 退款成功后资金原路返回")
    print("\n【考核题目】")
    print("- API请求流水号 req_seq_id 必须包含用户ID和请求日期")
    print("- 示例格式: 1435964137120268288_20251106_500937")
    print("- 所有API调用正确，考核通过")


def main():
    """主函数"""
    print_banner()
    print_instructions()
    
    # 初始化SDK API客户端
    try:
        api = HuifuSDKAPI()
    except ImportError as e:
        print(f"\n❌ 错误: {e}")
        print("\n请先安装汇付SDK:")
        print("  pip install dg-sdk==v2.0.10")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("【步骤 1】聚合正扫支付（支付宝NATIVE扫码支付）")
    print("="*60)
    
    print("\n💡 说明：")
    print("   NATIVE支付方式会生成收款二维码，您使用支付宝APP扫码即可完成支付")
    print("   无需输入付款码")
    
    # 获取支付金额
    amount = input("\n请输入支付金额（元，默认1.00）: ").strip()
    if not amount:
        amount = "1.00"
    
    try:
        float_amount = float(amount)
        if float_amount < 1.0:
            print("❌ 考核要求支付金额必须 ≥ 1.00 元！")
            sys.exit(1)
    except ValueError:
        print("❌ 金额格式错误！")
        sys.exit(1)
    
    # 执行支付（NATIVE支付不需要auth_code）
    pay_result = api.aggregate_pay(amount=amount)
    
    if not pay_result:
        print("\n❌ 支付失败，请检查错误信息")
        sys.exit(1)
    
    # 检查支付结果
    resp_code = pay_result.get("resp_code", "")
    trans_stat = pay_result.get("trans_stat", "")
    
    if not resp_code.startswith("0000"):
        print(f"\n❌ 支付失败: {pay_result.get('resp_desc', '未知错误')}")
        sys.exit(1)
    
    # 获取原交易信息（退款需要，需要提前获取用于轮询）
    org_req_seq_id = pay_result.get("req_seq_id")  # 原交易请求流水号
    org_req_date = pay_result.get("req_date")  # 原交易请求日期
    org_hf_seq_id = pay_result.get("hf_seq_id")  # 原交易汇付流水号
    party_order_id = pay_result.get("party_order_id")  # 原交易支付宝商户单号
    
    # 检查是否有二维码（NATIVE支付）
    qr_code = pay_result.get("qr_code", "")
    
    # 检查交易状态
    if trans_stat == "S":
        print("\n✅ 支付成功！（交易已完成）")
    elif trans_stat == "P":
        if qr_code:
            # 询问是否等待支付完成
            wait_payment = input("\n是否等待支付完成？（输入y将自动轮询订单状态，输入n直接继续）(y/n): ").strip().lower()
            
            if wait_payment == 'y':
                print("\n开始等待支付完成...")
                final_result = api.wait_for_payment(
                    req_seq_id=org_req_seq_id,
                    req_date=org_req_date,
                    hf_seq_id=org_hf_seq_id,
                    party_order_id=party_order_id,
                    max_wait_time=300,
                    poll_interval=3
                )
                
                if final_result:
                    final_stat = final_result.get("trans_stat", "")
                    if final_stat == "S":
                        print("\n✅ 支付已完成，可以继续退款流程")
                        pay_result = final_result  # 更新为最终结果
                        # 更新交易信息
                        org_hf_seq_id = final_result.get("hf_seq_id", org_hf_seq_id)
                        party_order_id = final_result.get("party_order_id", party_order_id)
                    else:
                        print(f"\n⚠️ 支付状态: {final_stat}，请检查后再决定是否继续")
                else:
                    print("\n⚠️ 未能确认支付状态，请稍后手动查询")
    else:
        print("\n✅ 下单成功！")
        print(f"交易状态: {trans_stat}")
    
    print(f"\n原交易信息:")
    print(f"  请求流水号: {org_req_seq_id}")
    print(f"  请求日期: {org_req_date}")
    print(f"  汇付流水号: {org_hf_seq_id}")
    print(f"  商户单号: {party_order_id}")
    
    # 询问是否继续退款
    print("\n" + "="*60)
    print("【步骤 2】交易退款")
    print("="*60)
    
    confirm = input("\n是否继续执行退款？(y/n): ").strip().lower()
    if confirm != 'y':
        print("\n已取消退款操作")
        print(f"\n如需稍后退款，请使用原交易汇付流水号: {org_hf_seq_id}")
        sys.exit(0)
    
    # 获取退款金额
    refund_amount = input(f"请输入退款金额（元，原支付金额: {amount}）: ").strip()
    if not refund_amount:
        refund_amount = amount
    
    try:
        float_refund = float(refund_amount)
        if float_refund <= 0 or float_refund > float(amount):
            print(f"❌ 退款金额必须 > 0 且 ≤ 原支付金额（{amount}元）")
            sys.exit(1)
    except ValueError:
        print("❌ 金额格式错误！")
        sys.exit(1)
    
    # 执行退款
    # 注意：SDK的退款请求对象需要 org_req_date（原交易日期）
    # 原交易标识通过 extend_infos 传递
    refund_result = api.refund(
        org_req_seq_id=org_req_seq_id,
        org_req_date=org_req_date,  # 原交易日期（必需）
        org_hf_seq_id=org_hf_seq_id,  # 汇付流水号（推荐）
        party_order_id=party_order_id,  # 商户单号
        refund_amt=refund_amount
    )
    
    if not refund_result:
        print("\n❌ 退款失败，请检查错误信息")
        sys.exit(1)
    
    # 检查退款结果（汇付响应码：0000开头表示成功）
    resp_code = refund_result.get("resp_code", "")
    if not resp_code.startswith("0000"):
        print(f"\n❌ 退款失败: {refund_result.get('resp_desc', '未知错误')}")
        sys.exit(1)
    
    print("\n✅ 退款成功！")
    
    # 完成考核
    print("\n" + "="*60)
    print("【考核完成】")
    print("="*60)
    print("\n✅ 聚合正扫支付 - 已完成")
    print("✅ 交易退款 - 已完成")
    print("\n请将以下信息填写到考核页面：")
    print(f"\n聚合正扫 req_seq_id: {org_req_seq_id}")
    print(f"交易退款 req_seq_id: {refund_result.get('req_seq_id', 'N/A')}")
    print("\n所有API调用正确，考核应该通过！🎉")
    print("\n" + "="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序异常: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

