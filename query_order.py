# -*- coding: utf-8 -*-
"""
订单查询功能测试
查看订单状态是否已支付完成

使用方法：
1. 使用汇付流水号查询（推荐）：
   python query_order.py --hf-seq-id "002900TOP1A251106141456P102ac139caf00000"

2. 使用商户单号查询：
   python query_order.py --party-order-id "03242511065129633711868"

3. 使用请求流水号查询：
   python query_order.py --req-seq-id "1435964137120268288_20251106_309379_PAY"
"""

import sys
from huifu_sdk_api import HuifuSDKAPI

def main():
    """主函数"""
    print("="*60)
    print(" " * 15 + "订单查询工具")
    print("="*60)
    
    try:
        api = HuifuSDKAPI()
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)
    
    # 从命令行参数获取查询信息
    req_seq_id = None
    hf_seq_id = None
    party_order_id = None
    req_date = None
    
    # 简单的命令行参数解析
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--req-seq-id" and i + 1 < len(args):
            req_seq_id = args[i + 1]
            i += 2
        elif args[i] == "--hf-seq-id" and i + 1 < len(args):
            hf_seq_id = args[i + 1]
            i += 2
        elif args[i] == "--party-order-id" and i + 1 < len(args):
            party_order_id = args[i + 1]
            i += 2
        elif args[i] == "--req-date" and i + 1 < len(args):
            req_date = args[i + 1]
            i += 2
        else:
            i += 1
    
    # 如果没有命令行参数，则交互式输入
    if not req_seq_id and not hf_seq_id and not party_order_id:
        print("\n请选择查询方式:")
        print("1. 使用汇付流水号查询（推荐）")
        print("2. 使用商户单号查询")
        print("3. 使用请求流水号查询")
        
        choice = input("\n请输入选项 (1/2/3): ").strip()
        
        if choice == "1":
            hf_seq_id = input("请输入汇付流水号: ").strip()
            if not hf_seq_id:
                print("❌ 汇付流水号不能为空")
                sys.exit(1)
        elif choice == "2":
            party_order_id = input("请输入商户单号: ").strip()
            if not party_order_id:
                print("❌ 商户单号不能为空")
                sys.exit(1)
        elif choice == "3":
            req_seq_id = input("请输入请求流水号: ").strip()
            if not req_seq_id:
                print("❌ 请求流水号不能为空")
                sys.exit(1)
            req_date = input("请输入请求日期 (YYYYMMDD，留空自动提取): ").strip()
            if not req_date:
                req_date = None
        else:
            print("❌ 无效选项")
            sys.exit(1)
    
    # 执行查询
    result = api.query_order(
        req_seq_id=req_seq_id,
        req_date=req_date,
        hf_seq_id=hf_seq_id,
        party_order_id=party_order_id
    )
    
    if result:
        import json
        print("\n" + "="*60)
        print("查询结果详情:")
        print("="*60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        resp_code = result.get("resp_code", "")
        trans_stat = result.get("trans_stat", "")
        
        print("\n" + "="*60)
        if resp_code.startswith("0000"):
            if trans_stat == "S":
                print("✅ 订单状态: 支付成功")
            elif trans_stat == "P":
                print("⏳ 订单状态: 处理中")
            elif trans_stat == "F":
                print("❌ 订单状态: 支付失败")
            elif trans_stat == "C":
                print("⚠️  订单状态: 订单已关闭")
            else:
                print(f"⚠️  订单状态: {trans_stat}")
        else:
            print(f"❌ 查询失败: {resp_code}")
            print(f"   错误描述: {result.get('resp_desc', '未知错误')}")
    else:
        print("\n❌ 查询失败，请检查参数")


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

