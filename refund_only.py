# -*- coding: utf-8 -*-
"""
独立退款脚本
如果您已经完成了支付，想单独执行退款，使用此脚本

使用方法：
1. 交互式运行：python refund_only.py
2. 命令行参数：
   python refund_only.py --req-seq-id "xxx" --req-date "20251106" --hf-seq-id "xxx" --refund-amt "1.00"
"""

import sys
from huifu_sdk_api import HuifuSDKAPI


def main():
    """独立退款主函数"""
    print("\n" + "="*60)
    print(" " * 20 + "汇付交易退款工具（SDK版本）")
    print("="*60)
    
    try:
        # 初始化SDK API客户端
        api = HuifuSDKAPI()
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)
    
    # 从命令行参数获取信息
    org_req_seq_id = None
    org_req_date = None
    org_hf_seq_id = None
    party_order_id = None
    refund_amt = None
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--req-seq-id" and i + 1 < len(args):
            org_req_seq_id = args[i + 1]
            i += 2
        elif args[i] == "--req-date" and i + 1 < len(args):
            org_req_date = args[i + 1]
            i += 2
        elif args[i] == "--hf-seq-id" and i + 1 < len(args):
            org_hf_seq_id = args[i + 1]
            i += 2
        elif args[i] == "--party-order-id" and i + 1 < len(args):
            party_order_id = args[i + 1]
            i += 2
        elif args[i] == "--refund-amt" and i + 1 < len(args):
            refund_amt = args[i + 1]
            i += 2
        else:
            i += 1
    
    # 如果传入了req_seq_id但没有req_date，自动提取日期
    if org_req_seq_id and not org_req_date:
        parts = org_req_seq_id.split("_")
        if len(parts) >= 2:
            org_req_date = parts[1]
            print(f"从请求流水号自动提取日期: {org_req_date}")
    
    # 如果没有命令行参数，则交互式输入
    if not org_req_seq_id and not org_hf_seq_id and not party_order_id:
        print("\n此脚本用于对已支付的订单进行退款操作")
        print("\n请选择输入方式:")
        print("1. 输入请求流水号（推荐，会自动提取日期）")
        print("2. 输入汇付流水号")
        print("3. 输入商户单号")
        
        choice = input("\n请输入选项 (1/2/3): ").strip()
        
        if choice == "1":
            org_req_seq_id = input("\n请输入原交易请求流水号: ").strip()
            if not org_req_seq_id:
                print("❌ 请求流水号不能为空！")
                sys.exit(1)
            # 自动提取日期
            parts = org_req_seq_id.split("_")
            if len(parts) >= 2:
                org_req_date = parts[1]
                print(f"自动提取请求日期: {org_req_date}")
        elif choice == "2":
            org_hf_seq_id = input("\n请输入原交易汇付流水号: ").strip()
            if not org_hf_seq_id:
                print("❌ 汇付流水号不能为空！")
                sys.exit(1)
            org_req_date = input("请输入原交易请求日期 (YYYYMMDD): ").strip()
            if not org_req_date:
                print("❌ 请求日期不能为空！")
                sys.exit(1)
        elif choice == "3":
            party_order_id = input("\n请输入商户单号: ").strip()
            if not party_order_id:
                print("❌ 商户单号不能为空！")
                sys.exit(1)
            org_req_date = input("请输入原交易请求日期 (YYYYMMDD): ").strip()
            if not org_req_date:
                print("❌ 请求日期不能为空！")
                sys.exit(1)
        else:
            print("❌ 无效选项")
            sys.exit(1)
    
    # 获取退款金额
    if not refund_amt:
        refund_amt = input("请输入退款金额（元，默认1.00）: ").strip()
        if not refund_amt:
            refund_amt = "1.00"
    
    try:
        float_refund = float(refund_amt)
        if float_refund <= 0:
            print("❌ 退款金额必须大于 0")
            sys.exit(1)
    except ValueError:
        print("❌ 金额格式错误！")
        sys.exit(1)
    
    # 确认退款
    print(f"\n准备退款:")
    print(f"  退款金额: {refund_amt} 元")
    if org_req_seq_id:
        print(f"  原交易请求流水号: {org_req_seq_id}")
    if org_hf_seq_id:
        print(f"  原交易汇付流水号: {org_hf_seq_id}")
    if party_order_id:
        print(f"  商户单号: {party_order_id}")
    if org_req_date:
        print(f"  原交易请求日期: {org_req_date}")
    
    confirm = input("\n确认执行退款？(y/n): ").strip().lower()
    if confirm != 'y':
        print("\n已取消退款操作")
        sys.exit(0)
    
    # 执行退款
    refund_result = api.refund(
        org_req_seq_id=org_req_seq_id,
        org_req_date=org_req_date,
        org_hf_seq_id=org_hf_seq_id,
        party_order_id=party_order_id,
        refund_amt=refund_amt
    )
    
    if not refund_result:
        print("\n❌ 退款失败，请检查错误信息")
        sys.exit(1)
    
    # 检查退款结果（汇付响应码：0000开头表示成功）
    resp_code = refund_result.get("resp_code", "")
    if not resp_code.startswith("0000"):
        print(f"\n❌ 退款失败: {refund_result.get('resp_desc', '未知错误')}")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ 退款成功！")
    print("="*60)
    print(f"\n退款流水号: {refund_result.get('req_seq_id', 'N/A')}")
    print(f"汇付流水号: {refund_result.get('hf_seq_id', 'N/A')}")
    print(f"退款金额: {refund_amt} 元")
    print("\n资金将原路返回到支付账户")
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

