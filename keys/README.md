# 密钥文件说明

本目录用于存放 RSA 密钥文件。

## 📁 文件说明

- `private_key.txt` - 您的 sys_id 私钥（商户私钥，用于签名请求）
- `public_key.txt` - 汇付的 sys_id 公钥（汇付公钥，用于验签响应）

## 🔐 密钥工作原理

**重要理解：这两个密钥文件不是一对！**

根据汇付的签名机制：

### 请求签名（您 → 汇付）
```
1. 您构造请求参数
2. 用您的私钥（private_key.txt）对参数签名
3. 将签名随请求发送给汇付
4. 汇付用您的公钥（您需要上传到汇付平台）验证签名
```

### 响应验签（汇付 → 您）
```
1. 汇付处理请求，生成响应
2. 汇付用自己的私钥对响应签名
3. 将签名随响应返回给您
4. 您用汇付的公钥（public_key.txt）验证响应签名
```

所以您需要的密钥是：
- ✅ **您的私钥** - 用于签名您的请求
- ✅ **汇付的公钥** - 用于验证汇付的响应
- ℹ️ **您的公钥** - 需要上传到汇付平台（由汇付使用）

## 🔑 支持的密钥格式

程序**自动支持两种格式**，您可以选择任意一种：

### 格式1：完整 PEM 格式（推荐）

包含 `-----BEGIN/END-----` 标记的标准格式：

**私钥示例：**
```
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDFOYOjLTndQiYA
iFQf4ZZ6UA1T5fg2PH16XboAORgLBz/SjeiIMmIdExP1NFDH6SNqcQk6ginqk+gW
...（更多行）...
-----END PRIVATE KEY-----
```

**公钥示例：**
```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkmP0eyQVeGHVxk/4+Zq9
R6tm8vmQZaMAvtvy5D/Ki3lvhfRn8T3R3vP5xTpp2zAtmZzFnc1k4DswYBsv7lsx
...（更多行）...
-----END PUBLIC KEY-----
```

### 格式2：纯 base64 字符串（自动转换）

从汇付支付平台直接复制的纯 base64 字符串：

**私钥示例：**
```
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDFOYOjLTndQiYAiFQf4ZZ6UA1T5fg2PH16XboAORgLBz/SjeiIMmIdExP1NFDH6SNqcQk6ginqk+gW0CBojEE5Loj3ROqtBRnBehVavO89xnvezsj1NZDqw416GYPCU0n6198A73c3Kn0OWoiivF5BJDra88z/zcApNzAeiVw6loZEEvzNRpfuKzs6uH6NeFQnY2wtePQwTAW5d89gUyewJSzwPPVU8r/hiPVKSB0AEkGT85UOBzaEKyAEqPfLAS/uY49Qdq+/j6lszNpjWcb6vkIeoHD3wmZdoHR7uLc+VxSk7kvJyLUv6SBtH3/jTy4ghFLQWJHagLB2QCPy9ompAgMBAAECggEAcG4JDMyLYAaFg2g0DLic/70C3AENLl3tagRkNBxYCHFpgK5FEN8n70sg5XedVVkiR1uI10G8g20tsVOUJgVOaTqN+effoCJ4PENMSR3LhHvRwYJALQkMQ8iWrjQ9WFoComzNQ8s/OsON5tDVc2/Oi3QL2SWCh5DTKqu7Uq0bVonYUX2IT8x7zWbE+tgphjI76JRDp4gkjh5ebebNBhqsOjYelNNWF3g7rVAr4zB2TMRM6N/66z/qLRk+mQQEhShojS2c2pyAtNC+7C6VZiX+XxH4ArSbf6AQyaMmPj4d3rMAYG916WNfb9GkqFyZhRNbMwRsAIfErS46PDKpKhInwQKBgQDnu4vV2U7Sqc/ab3hXh8H6d1HvxvTb7634XNyT/qtJ4nMT9CCxZE88iesqJyXNxzEElpLJRlwNPgDaJfs8qEjJ9zF6N/7ip9VPxITd5/6jBuILiugJSa7epvdZAtyVo1xOf2BN7cX/4Ul/SE11YjgyjLr1b3U4SY/Bc8w01Pmb+wKBgQDZ4Nq8u+k4GQh6G9pFSwgDxMnPUGX4vnWew7zsyy6z45tXuzFZrvpuzWTUUtnGalzXYGaUqm5ivmmP9+CCZBWaxZkSTF8ONRm1OXTRCJlF57AzXZVVc4+inhM8WnX6KIN/FDu4nlTf7wN6J42BcqOkz8KS9N7twpYartJnTPG7qwKBgQDhqVUHLtL/erYadSqvslhH3CJCaXDRLJoxndx/kiSjko2WBMpBdPlkbro/FlhOB4fIfAj9UDMcAiE6TnpWG1qmsr3P0u+3MNEdGLZ6kgz6HR3LN722LbbIw7djStIcNjURjCDwQnfqMi0scfBcOwWW1EzL7XotEhWXwXg+ipd4OQKBgQCotysK7UQ6sX/T9s99yw1IxdE0nWBpTysLpy0b/HaMzFqVhBpCBXJd7OUAWavTrrd3/GlTA+r4wdRCrMMIlXH5aLwQ5FzTRqFCqVxhJhRygmf6TqR+CD+YwGnK2Y30Cf1RoZxhaRH2WkJKDGjSbbB0xoE4hTA/0uejf+7kGTwzgwKBgBgcuEy5fxR5O+HkV/Lay/rrHznbJxOEJ/EiV2WDKDi1Acp1QZAKb1aguqx15j7t9exGUr6Y5eCfAFOQfzlePJuLthe5APEsuzv9nslnVusamWKkxoWl6h36OYQjTf1FCgOD7QCjhaiKKQQLsZGigmMKy2D5utIWQdNoLnlhayan
```

**公钥示例：**
```
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkmP0eyQVeGHVxk/4+Zq9R6tm8vmQZaMAvtvy5D/Ki3lvhfRn8T3R3vP5xTpp2zAtmZzFnc1k4DswYBsv7lsxwseoJ3sIM6of6NYnf+39CK+NhKSsdDNDET2KCxD5Gip3WJVtgP3P4w3P/U2jCi8Xzm9sxy3XZ3TSZuokvX77UnfBZTFMuGjCmZFcuM6VjDOxoaEtnYhAVLOQItb3Jr1vvIg4vrhCWBus9YVgl3Ua5qtTccmpspnFbY3ix0UFrmHczTaPWrxKMrnEIDurgmMPXPiyR67Z/AcvcJ8vgvaVHnINmDb0hlRUkI623P9dO/fPswaNIEj0ZeoZHcdLya07swIDAQAB
```

> ⚠️ **重要**：如果使用纯 base64 格式，程序会在运行时提示"检测到纯base64格式密钥，自动转换为PEM格式..."

## 📝 如何获取密钥

1. 登录汇付商户平台
2. 进入 **开发配置** → **密钥管理**
3. 找到 `sys_id = 6666000108840829`
4. 下载或复制对应的密钥：
   - **sys_id 私钥** → 保存到 `private_key.txt`
   - **sys_id 汇付公钥** → 保存到 `public_key.txt`

## 💡 使用建议

- **推荐方式**：直接从平台复制纯 base64 字符串粘贴即可，无需手动添加 PEM 标记
- 程序会自动检测格式并进行转换
- 可以包含换行符或空格，程序会自动清理

## ⚠️ 安全提示

- 密钥文件已添加到 `.gitignore`，不会被提交到版本控制
- 请妥善保管您的私钥，不要泄露或分享
- 不要将真实密钥上传到公开仓库

## ✅ 测试配置

配置完成后，运行测试命令验证：

```bash
python test_sign.py
```

看到 "✅ 签名验证成功" 表示配置正确。

