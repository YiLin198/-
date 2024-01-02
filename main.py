import pandas as pd
import openpyxl

# 假设 data 是对阵数据的 DataFrame
# 假设 heroes 是英雄数据的 DataFrame

# /Users/dongchen/储东宸/小冰冰传奇.xlsx
# Excel文件的路径
excel_path = '/Users/dongchen/储东宸/小冰冰传奇.xlsx'

# 读取对阵数据
df_battles = pd.read_excel(excel_path, sheet_name='对阵')

# 读取英雄数据
df_heroes = pd.read_excel(excel_path, sheet_name='英雄')

# 查看前几行数据以确认正确导入
data = df_battles

def find_top_counters(team, data, num_counters=10):
    input_team_set = set(team)
    counter_win_rates = {}

    for index, row in data.iterrows():
        team_a = {row[f'英雄A{i}'] for i in range(1, 6)}
        team_b = {row[f'英雄B{i}'] for i in range(1, 6)}

        if input_team_set == team_a:
            opponent_team = team_b
            win = row['结果'] == 'B'
        elif input_team_set == team_b:
            opponent_team = team_a
            win = row['结果'] == 'A'
        else:
            continue

        opponent_team = frozenset(opponent_team)
        wins, total = counter_win_rates.get(opponent_team, (0, 0))
        counter_win_rates[opponent_team] = (wins + win, total + 1)

    # 修正数据结构以匹配 DataFrame 的期望格式
    formatted_counters = []
    for team, (wins, total) in counter_win_rates.items():
        win_rate = wins / total if total > 0 else 0
        formatted_counters.append((','.join(team), wins, total, win_rate))

    top_counters = sorted(formatted_counters, key=lambda x: x[3], reverse=True)[:num_counters]

    top_counters_df = pd.DataFrame(top_counters, columns=['Opponent Team', 'Wins', 'Total Matches', 'Win Rate'])
    return top_counters_df

# 使用示例
input_team = ['骨王', '巨魔', '幻影刺客', '神灵武士', '白虎']
top_counters = find_top_counters(input_team, df_battles)
print(top_counters)

