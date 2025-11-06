# 汇付商户考核 - 支付宝正扫+退款场景

自动化完成汇付商户平台开通考核，实现"支付宝正扫+退款场景"的考核要求。

## 📋 考核要求

根据 [汇付考核文档](https://paas.huifu.com)，需要完成以下两个步骤：

1. **聚合正扫**：调用[聚合正扫API](https://paas.huifu.com/open/doc/api/)
   - `trade_type = A_NATIVE`（支付宝NATIVE扫码支付）
   - 向个人账户支付 ≥ 1.00 元
   - 如需分账需设置分账相关参数

2. **交易退款**：调用[交易退款API](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tk?id=ewm)
   - 将支付款退还给用户
   - 退款成功后资金原路返回

### 考核题目要点

- API 请求流水号 `req_seq_id` 必须包含您的用户ID (1435964137120268288) 和请求日期
- 示例格式：`1435964137120268288_20251106_500937`
- 将 `req_seq_id` 填入下方输入框点击【我已完成考核】
- 斗拱将校验此次请求是否返回正确内容，所有 API 调用正确，考核通过

## 🚀 快速开始

### 0. 创建并激活虚拟环境（推荐）

**Windows:**
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate
```

**Linux/Mac:**
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

激活后，命令行提示符前会显示 `(venv)` 标记。

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置商户信息（可选）

商户信息可以通过环境变量配置，如果未设置环境变量，将使用默认值。

#### 方式一：使用环境变量（推荐）✨

**方法A：使用 .env 文件（推荐）**

1. 复制示例文件：
```bash
# Windows
copy env.example .env

# Linux/Mac
cp env.example .env
```

2. 编辑 `.env` 文件，修改为您的实际值：
```env
HUIFU_ID=6666000182573147
SYS_ID=6666000182558527
PRODUCT_ID=XLSISV
USER_ID=1435964137120268288
```

3. 确保已安装 `python-dotenv`（已包含在 `requirements.txt` 中）：
```bash
pip install python-dotenv
```

> 💡 **注意**：
> - `.env` 文件已加入 `.gitignore`，不会被提交到版本控制
> - 如果未安装 `python-dotenv`，程序仍可使用系统环境变量或默认值

**方法B：直接在系统中设置环境变量**

**Windows (PowerShell):**
```powershell
$env:HUIFU_ID="6666000182573147"
$env:SYS_ID="6666000182558527"
$env:PRODUCT_ID="XLSISV"
$env:USER_ID="1435964137120268288"
```

**Windows (CMD):**
```cmd
set HUIFU_ID=6666000182573147
set SYS_ID=6666000182558527
set PRODUCT_ID=XLSISV
set USER_ID=1435964137120268288
```

**Linux/Mac:**
```bash
export HUIFU_ID="6666000182573147"
export SYS_ID="6666000182558527"
export PRODUCT_ID="XLSISV"
export USER_ID="1435964137120268288"
```

#### 方式二：使用默认值

如果不设置环境变量，程序会使用 `config.py` 中的默认值。如需修改默认值，可以直接编辑 `config.py` 文件。

#### 环境变量说明

- `HUIFU_ID`: 商户号
- `SYS_ID`: 系统号
- `PRODUCT_ID`: 产品号
- `USER_ID`: 用户ID（考核要求必须包含在 `req_seq_id` 中）

### 3. 配置密钥 ⚠️ 重要

密钥使用独立文件存储，更安全方便。**支持两种格式，直接粘贴即可！**

#### 方式一：直接复制粘贴（最简单，推荐！）✨

**从汇付平台直接复制纯 base64 字符串，无需添加任何格式标记：**

1. 编辑 `keys/private_key.txt`，粘贴私钥的 base64 字符串：
```
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDFOYOjLTndQiYA...（一长串字符）
```

2. 编辑 `keys/public_key.txt`，粘贴公钥的 base64 字符串：
```
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkmP0eyQVeGHVxk/4+Zq9...（一长串字符）
```

> 💡 **程序会自动检测并添加 PEM 格式标记，您无需手动操作！**

#### 方式二：使用完整 PEM 格式

如果您的密钥已经包含 PEM 格式标记，也可以直接粘贴：

1. `keys/private_key.txt`：
```
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgw...
（多行）
-----END PRIVATE KEY-----
```

2. `keys/public_key.txt`：
```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB...
（多行）
-----END PUBLIC KEY-----
```

#### 方式三：查看配置向导

运行配置向导查看详细配置说明：
```bash
python setup_config.py
```

#### 如何获取密钥

1. 登录汇付商户平台
2. 进入**开发配置** → **密钥管理**
3. 找到 `sys_id = 6666000108840829`
4. 下载或复制对应的：
   - **sys_id 私钥**（您的商户私钥，用于签名请求）→ 保存到 `keys/private_key.txt`
   - **sys_id 汇付公钥**（汇付的公钥，用于验签响应）→ 保存到 `keys/public_key.txt`

#### 密钥作用说明 🔐

根据[汇付签名文档](https://paas.huifu.com/open/doc/api_standard/%22%20/l%20%22/api_v2jqyq/#/api_v2jqyq)，密钥使用方式如下：

**请求签名流程：**
```
您的请求 → 用您的私钥签名 → 发送到汇付 → 汇付用您的公钥验签
```

**响应验签流程：**
```
汇付的响应 → 汇付用自己的私钥签名 → 返回给您 → 您用汇付公钥验签
```

> ⚠️ **重要**：`keys/private_key.txt` 和 `keys/public_key.txt` 不是一对密钥！
> - 私钥是您的，用于签名请求
> - 公钥是汇付的，用于验证响应
> - 这是正常的，不是配置错误

### 4. 测试密钥配置

配置完成后，测试密钥是否正确：
```bash
python test_sign.py
```

看到 **✅ 签名验证成功** 表示密钥配置正确，可以继续下一步。

### 5. 运行主程序

```bash
python main.py
```

按照提示操作即可完成考核！

## 📖 使用流程

### 步骤 1：NATIVE扫码支付

1. 运行程序后，输入支付金额（≥ 1.00 元）
2. 程序自动调用聚合正扫API
3. 支付接口会返回收款二维码链接（`qr_code`）
4. 程序自动在终端显示二维码（ASCII艺术形式）
5. 使用支付宝APP扫描终端中的二维码
6. 确认支付金额并完成支付
7. 可选择等待支付完成（自动轮询订单状态）

### 步骤 2：交易退款

1. 支付成功后，程序会自动获取原交易流水号
2. 确认是否继续执行退款
3. 输入退款金额（≤ 原支付金额）
4. 程序自动调用交易退款API完成退款

### 步骤 3：提交考核

程序执行成功后，会显示：
- 聚合正扫的 `req_seq_id`
- 交易退款的 `req_seq_id`

将这些信息填写到汇付考核页面即可完成考核！

## 📦 项目结构

```
huifu-Assessment/
├── keys/                  # 密钥文件目录
│   ├── private_key.txt    # RSA私钥文件（需自行配置，已加入.gitignore）
│   ├── public_key.txt     # RSA公钥文件（需自行配置，已加入.gitignore）
│   └── README.md          # 密钥配置说明
├── config.py              # 配置文件（商户信息、密钥读取，支持环境变量）
├── env.example            # 环境变量配置示例文件
├── huifu_sdk_api.py       # 汇付API封装（使用官方SDK）⭐
├── main.py                # 主程序（支付+退款完整流程）⭐
├── refund_only.py         # 单独退款工具
├── query_order.py         # 订单查询工具
├── setup_config.py        # 配置向导脚本
├── test_sign.py           # 签名功能测试脚本
├── requirements.txt       # Python依赖包（含SDK）
├── LICENSE                # MIT开源协议
├── .gitignore            # Git忽略规则
└── README.md             # 项目文档（本文件）
```

## 💡 实用工具脚本

项目提供了多个实用脚本，方便不同场景使用：

### 配置向导
查看详细的配置说明和密钥获取方法：
```bash
python setup_config.py
```

### 测试签名
验证RSA密钥配置是否正确：
```bash
python test_sign.py
```
输出 `✅ 签名验证成功` 表示配置正确。

### 完整流程（支付+退款）
执行完整的考核流程：
```bash
python main.py
```
程序会引导您完成：
1. 聚合正扫支付（NATIVE扫码）
2. 交易退款
3. 获取考核所需的 `req_seq_id`

### 单独退款
如果已完成支付，只需执行退款：
```bash
python refund_only.py
```
支持多种输入方式：
- 使用请求流水号（自动提取日期）
- 使用汇付流水号
- 使用商户单号

### 查询订单
查询订单支付状态：
```bash
python query_order.py
```
支持通过请求流水号、汇付流水号或商户单号查询。

## 📝 API 说明

本项目使用[汇付官方Python SDK（dg-sdk）](https://paas.huifu.com/open/doc/devtools/#/sdk_python)，自动处理签名、验签等复杂操作。

### 聚合正扫 API（V3版本）

- **接口类**：`V3TradePaymentJspayRequest`
- **文档**：[聚合正扫API文档](https://paas.huifu.com/open/doc/api/)
- **支持支付方式**：
  - `A_NATIVE`: 支付宝NATIVE扫码支付（本项目使用）
  - `T_JSAPI`: 微信公众号
  - `T_MINIAPP`: 微信小程序
  - `A_JSAPI`: 支付宝JS
  - `U_NATIVE`: 银联二维码正扫
  - `D_NATIVE`: 数字人民币正扫
  - 等更多方式
- **主要参数**：
  - `trade_type`: A_NATIVE（支付宝NATIVE扫码支付）
  - `trans_amt`: 交易金额
  - `req_seq_id`: 请求流水号（必须包含用户ID和日期）
  - `qr_code`: 响应中返回的收款二维码链接（自动在终端显示）

### 交易退款 API

- **接口类**：`V3TradePaymentScanpayRefundRequest`
- **文档**：[交易退款API文档](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tk?id=ewm)
- **主要参数**：
  - `org_req_seq_id`: 原交易请求流水号（推荐）
  - `org_hf_seq_id`: 原交易汇付流水号（可选）
  - `party_order_id`: 原交易商户单号（可选）
  - `org_req_date`: 原交易请求日期（必需）
  - `ord_amt`: 退款金额
  - `req_seq_id`: 退款请求流水号

### 订单查询 API

- **接口类**：`V3TradePaymentScanpayQueryRequest`
- **主要参数**：
  - `req_seq_id`: 请求流水号（可选）
  - `hf_seq_id`: 汇付流水号（推荐）
  - `party_order_id`: 商户单号（可选）
  - `req_date`: 请求日期（必需）

## ⚠️ 注意事项

### 1. 密钥安全
- ✅ 密钥文件已添加到 `.gitignore`，不会被提交到版本控制
- ✅ 使用独立文件存储，方便管理和更换
- ⚠️ 请妥善保管您的私钥，不要泄露或分享
- ⚠️ 不要将 `keys/` 目录下的真实密钥文件上传到公开仓库

### 2. 虚拟环境管理

**激活虚拟环境**（每次使用前）：
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**退出虚拟环境**：
```bash
deactivate
```

### 3. 商户信息配置
- 商户信息（`HUIFU_ID`、`SYS_ID`、`PRODUCT_ID`、`USER_ID`）可通过环境变量配置
- 如果未设置环境变量，程序会使用 `config.py` 中的默认值
- 推荐使用环境变量方式，便于不同环境切换（测试/生产）
- 环境变量设置方式见"快速开始"章节

### 4. 环境选择
- 考核建议使用**测试环境**
- 确保使用测试商户号和测试账号
- SDK会自动处理API地址，无需手动配置

### 5. 金额限制
- 支付金额必须 **≥ 1.00 元**（考核要求）
- 退款金额必须 **> 0** 且 **≤ 原支付金额**
- 程序会自动验证金额范围

### 6. 流水号格式（重要）
- `req_seq_id` 必须包含用户ID: `1435964137120268288`
- 必须包含请求日期（YYYYMMDD格式）
- 示例：`1435964137120268288_20251106_500937`
- ✅ 程序已自动生成符合要求的流水号，无需手动构造

### 7. NATIVE扫码支付流程

1. 调用支付API，获得二维码（`qr_code`）
2. 程序自动在终端显示二维码
3. 用户使用支付宝APP扫描终端中的二维码
4. 用户确认支付
5. 查询订单状态确认支付完成（可选择自动轮询）

### 8. 错误处理
- **签名错误**：检查密钥文件是否完整正确
- **支付失败**：检查金额是否符合要求、二维码是否正确显示
- **退款失败**：检查原交易是否成功、退款金额是否超限、是否提供了原交易日期
- **网络错误**：检查网络连接，SDK会自动处理API地址

## 🔍 故障排查

### 问题 1：密钥文件找不到

**错误信息**：
```
警告: 密钥文件不存在: E:\pythonProject\huifu-Assessment\keys\private_key.txt
```

**解决方案**：
1. 确认 `keys/` 目录存在
2. 确认 `keys/private_key.txt` 和 `keys/public_key.txt` 文件存在
3. 检查文件名是否正确（不要有多余的空格或扩展名）

### 问题 2：签名错误

**错误信息**：
```
验签失败: ...
签名错误
```

**解决方案**：
1. 确认密钥文件内容完整无误
2. 检查密钥格式，必须包含 `-----BEGIN/END-----` 标记（或纯base64，程序会自动转换）
3. 确认使用的是 `sys_id = 6666000108840829` 对应的密钥
4. 运行 `python test_sign.py` 测试密钥配置
5. 检查密钥文件编码为 UTF-8

### 问题 3：SDK未安装

**错误信息**：
```
ModuleNotFoundError: No module named 'dg_sdk'
```

**解决方案**：
1. 确认已激活虚拟环境（命令行前有 `(venv)` 标记）
2. 安装SDK：
```bash
pip install dg-sdk==v2.0.10
```
3. 或重新安装所有依赖：
```bash
pip install -r requirements.txt
```

### 问题 4：退款失败 - 原交易请求日期不能为空

**错误信息**：
```
resp_code: 10000000
resp_desc: 原交易请求日期不能为空
```

**解决方案**：
1. 使用 `--req-seq-id` 参数时，会自动提取日期
2. 使用 `--hf-seq-id` 或 `--party-order-id` 时，必须同时提供 `--req-date`
3. 确保日期格式为 `YYYYMMDD`，如 `20251106`

### 问题 5：查询订单失败 - 21000000错误

**错误信息**：
```
resp_code: 21000000
resp_desc: 原机构请求流水号、交易返回的全局流水号、用户账单上的商户订单号...不能同时为空
```

**解决方案**：
1. 查询订单时需要至少提供一个标识：
   - `--req-seq-id`（请求流水号）
   - `--hf-seq-id`（汇付流水号，推荐）
   - `--party-order-id`（商户单号）
2. 推荐使用汇付流水号查询：
```bash
python query_order.py --hf-seq-id "002900TOP4A251106142509P402ac13649000000"
```

### 问题 6：虚拟环境激活失败

**Windows PowerShell 报错**：
```
无法加载文件 venv\Scripts\Activate.ps1，因为在此系统上禁止运行脚本
```

**解决方案**：
```bash
# 方法1：使用 cmd.exe 而不是 PowerShell
venv\Scripts\activate.bat

# 方法2：修改 PowerShell 执行策略（需要管理员权限）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📚 参考文档

- [汇付开放平台文档](https://paas.huifu.com/open/doc/)
- [聚合正扫API文档](https://paas.huifu.com/open/doc/api/)
- [交易退款API文档](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tk?id=ewm)
- [汇付Python SDK文档](https://paas.huifu.com/open/doc/devtools/#/sdk_python)

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

jiulingyun.cn - 2025

---

**祝您考核顺利通过！** 🎉
