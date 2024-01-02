import pandas as pd

# 从您提供的文本构造DataFrame
excel_path = '/Users/dongchen/储东宸/小冰冰传奇.xlsx'

# 读取对阵数据
df_battles = pd.read_excel(excel_path, sheet_name='对阵')

# 读取英雄数据
df_heroes = pd.read_excel(excel_path, sheet_name='英雄')

def find_teams_including_heroes(input_heroes, df):
    # 清理输入英雄列表，移除空字符串
    input_heroes = [hero for hero in input_heroes if hero]

    # 定义匹配函数，检查给定的英雄是否都在队伍中
    def team_includes_heroes(row, heroes, team_prefix):
        team_heroes = {row[f'{team_prefix}{i+1}'] for i in range(5)}
        return all(hero in team_heroes for hero in heroes)

    # 初始化胜率统计
    win_rates = {}

    for index, row in df.iterrows():
        for team_prefix in ('英雄A', '英雄B'):
            if team_includes_heroes(row, input_heroes, team_prefix):
                team = tuple(row[f'{team_prefix}{i+1}'] for i in range(0, 5))
                result_key = 'A' if team_prefix == '英雄A' else 'B'
                win = int(row['结果'] == result_key)

                if team not in win_rates:
                    win_rates[team] = {'wins': 0, 'total': 0}
                win_rates[team]['wins'] += win
                win_rates[team]['total'] += 1

    if not win_rates:
        return pd.DataFrame()  # 如果没有匹配的记录，则返回空DataFrame

    # 计算胜率
    for team, stats in win_rates.items():
        stats['Win Rate'] = stats['wins'] / stats['total'] if stats['total'] > 0 else 0

    # 创建包含胜率信息的列表
    win_rate_list = [
        {'Team': ' - '.join(team), 'Wins': stats['wins'], 'Total Matches': stats['total'], 'Win Rate': stats['Win Rate']}
        for team, stats in win_rates.items()
    ]

    # 创建DataFrame并排序
    win_rate_df = pd.DataFrame(win_rate_list)
    win_rate_df.sort_values(by=['Win Rate', 'Total Matches'], ascending=[False, False], inplace=True)
    # 筛选场次大于2的队伍
    # win_rate_df = win_rate_df[win_rate_df['Total Matches'] > 1]
    win_rate_df.reset_index(drop=True, inplace=True)

    return win_rate_df


# 示例输入，输入的英雄在同一队伍中
input_heroes = ['斧王', '圣堂刺客', '', '', '']
input_heroes2 = ['人马', '', '发条', '', '暗牧']
input_heroes3 = ['骨王', '末日使者', '幻影刺客', '冰女', '']

# 获取胜率最高的队伍
high_win_rate_teams_df = find_teams_including_heroes(input_heroes, df_battles)
high_win_rate_teams_df2 = find_teams_including_heroes(input_heroes2, df_battles)
high_win_rate_teams_df3 = find_teams_including_heroes(input_heroes3, df_battles)
print(high_win_rate_teams_df)
print(high_win_rate_teams_df2)
print(high_win_rate_teams_df3)

