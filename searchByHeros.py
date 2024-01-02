import pandas as pd

# 从您提供的文本构造DataFrame
excel_path = '/Users/dongchen/储东宸/小冰冰传奇.xlsx'

# 读取对阵数据
df_battles = pd.read_excel(excel_path, sheet_name='对阵')

# 读取英雄数据
df_heroes = pd.read_excel(excel_path, sheet_name='英雄')


def find_high_win_rate_teams(input_heroes, df):
    # 清理输入英雄列表，移除空字符串
    input_heroes = [hero for hero in input_heroes if hero]

    # 定义匹配函数，检查队伍是否包含所有输入的英雄
    def match_team(row, heroes, team='A'):
        team_heroes = set(row[f'英雄{team}{i + 1}'] for i in range(5) if pd.notna(row[f'英雄{team}{i + 1}']))
        return all(hero in team_heroes for hero in heroes)

    # 初始化胜率字典
    win_rates = {}

    for index, row in df.iterrows():
        if match_team(row, input_heroes, team='A'):
            opponent_team = tuple(row[f'英雄B{i + 1}'] for i in range(5))
            if row['结果'] == 'B':
                win = 1
            else:
                win = 0
        elif match_team(row, input_heroes, team='B'):
            opponent_team = tuple(row[f'英雄A{i + 1}'] for i in range(5))
            if row['结果'] == 'A':
                win = 1
            else:
                win = 0
        else:
            continue

        # 更新胜率统计
        if opponent_team not in win_rates:
            win_rates[opponent_team] = {'wins': 0, 'total': 0}
        win_rates[opponent_team]['wins'] += win
        win_rates[opponent_team]['total'] += 1

    if not win_rates:
        return pd.DataFrame()  # 如果没有匹配的记录，则返回空DataFrame

    # 计算胜率
    win_rate_list = [
        {'Team': ' - '.join(filter(None, team)), 'Wins': stats['wins'], 'Total Matches': stats['total'],
         'Win Rate': stats['wins'] / stats['total']}
        for team, stats in win_rates.items()
    ]

    # 创建DataFrame并排序
    win_rate_df = pd.DataFrame(win_rate_list)
    win_rate_df.sort_values(by=['Win Rate', 'Total Matches'], ascending=[False, False], inplace=True)
    # 筛选场次大于2的队伍
    # win_rate_df = win_rate_df[win_rate_df['Total Matches'] > 2]
    win_rate_df.reset_index(drop=True, inplace=True)

    return win_rate_df


# 示例输入，输入的英雄在同一队伍中
input_heroes = ['骨王', '末日使者', '幻影刺客', '', '']
input_heroes2 = ['剑圣', '', '', '舞姬', '白虎']
input_heroes3 = ['人马', '幻影刺客', '冰女', '', '']

# 获取胜率最高的队伍
high_win_rate_teams_df = find_high_win_rate_teams(input_heroes, df_battles)
high_win_rate_teams_df2 = find_high_win_rate_teams(input_heroes2, df_battles)
high_win_rate_teams_df3 = find_high_win_rate_teams(input_heroes3, df_battles)
print(high_win_rate_teams_df)
print(high_win_rate_teams_df2)
print(high_win_rate_teams_df3)
