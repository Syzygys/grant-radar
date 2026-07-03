# Grant Radar

Lightweight CLI for scanning public Web3 grant and bounty opportunities.

## 功能
- 聚合公开 Web3 机会平台到一张表
- 零必需依赖（仅可选 `requests`）；离线时优雅降级不报错
- 支持 `--json` 输出，便于接入其它管线

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```bash
python src/main.py            # 打印机会表格
python src/main.py --json     # JSON 输出
GITHUB_TOKEN=xxx python src/main.py   # 提高 GitHub API 限额
```

## 测试
```bash
python -m pytest tests/ -q     # 或: python tests/test_basic.py
```

## 技术栈
Python 3.10+, requests（可选）

## 数据源
| 平台 | 接口 |
|------|------|
| Superteam Earn | `/api/listings` |
| TON Footsteps | GitHub Issues API（仓库归档时自动跳过） |

## 路线图
- 增加更多公开 grant / bounty 源
- 评分排序与去重
- 导出 CSV / 推送 Telegram
