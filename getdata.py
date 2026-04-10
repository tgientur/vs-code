import akshare as ak
import pandas as pd
import json
import os

SYMBOL = "600549"
START = "20251201"
END = "20260327"

# 获取数据
df = ak.stock_zh_a_hist(symbol=SYMBOL, period="daily",
                        start_date=START, end_date=END, adjust="")

# 重命名列
df.rename(columns={
    '日期': 'date',
    '开盘': 'open',
    '收盘': 'close',
    '最高': 'high',
    '最低': 'low',
    '成交量': 'volume'
}, inplace=True)

# 日期转为字符串（ECharts 需要）
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

# 计算均线
df['MA5'] = df['close'].rolling(5).mean()
df['MA10'] = df['close'].rolling(10).mean()
df['MA20'] = df['close'].rolling(20).mean()

# 保留需要的列：日期、开高低收、成交量、均线
df_out = df[['date', 'open', 'close', 'high', 'low', 'volume', 'MA5', 'MA10', 'MA20']].copy()

# 处理 NaN 为 None（以便 JSON 序列化）
df_out = df_out.where(pd.notnull(df_out), None)

# 转为 JSON 格式（记录数组）
records = df_out.to_dict(orient='records')

# 保存到文件（路径根据你的笔记库调整）
output_path = r"C:\Users\admin\Documents\Obsidian Vault\stock_data"   # 修改为你的实际路径
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"数据已保存至：{output_path}")