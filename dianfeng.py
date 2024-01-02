import pandas as pd

# 从您提供的文本构造DataFrame
excel_path = '/Users/dongchen/储东宸/小冰冰传奇.xlsx'

# 读取对阵数据
df_battles = pd.read_excel(excel_path, sheet_name='对阵')

# 读取英雄数据
df_heroes = pd.read_excel(excel_path, sheet_name='英雄')


def dianfeng_find_high_win_rate_teams(input_heroes, df):
    hero_pattern = [None if hero == '' else hero for hero in input_heroes]

    def match_pattern_a(row, pattern):
        return all(hero is None or row[f'英雄A{i + 1}'] == hero for i, hero in enumerate(pattern))

    def match_pattern_b(row, pattern):
        return all(hero is None or row[f'英雄B{i + 1}'] == hero for i, hero in enumerate(pattern))

    matched_records_a = df[df.apply(lambda row: match_pattern_a(row, hero_pattern), axis=1)]
    matched_records_b = df[df.apply(lambda row: match_pattern_b(row, hero_pattern), axis=1)]

    # print(matched_records_a)
    # print(matched_records_b)
    win_rates = {}
    for index, row in matched_records_a.iterrows():
        opponent_team = tuple(row['英雄B1':'英雄B5'].values)
        if opponent_team not in win_rates:
            win_rates[opponent_team] = {'wins': 0, 'total': 0}
        if row['结果'] == 'B':
            win_rates[opponent_team]['wins'] += 1
        win_rates[opponent_team]['total'] += 1

    for index, row in matched_records_b.iterrows():
        opponent_team = tuple(row['英雄A1':'英雄A5'].values)
        if opponent_team not in win_rates:
            win_rates[opponent_team] = {'wins': 0, 'total': 0}
        if row['结果'] == 'A':
            win_rates[opponent_team]['wins'] += 1
        win_rates[opponent_team]['total'] += 1

    # Check if win_rates is not empty
    if not win_rates:
        return pd.DataFrame()  # Return an empty DataFrame if no matches found

    # Calculate win rate for each team
    for team, stats in win_rates.items():
        stats['Win Rate'] = stats['wins'] / stats['total'] if stats['total'] > 0 else 0

    # Create a list of teams with their win rates
    win_rate_list = [
        {'Team': ' - '.join(team), 'Wins': stats['wins'], 'Total Matches': stats['total'], 'Win Rate': stats['Win Rate']}
        for team, stats in win_rates.items()
    ]

    # Create DataFrame from the list
    win_rate_df = pd.DataFrame(win_rate_list)

    # Sort the DataFrame by win rate in descending order
    win_rate_df.sort_values(by=['Win Rate', 'Total Matches'], ascending=False, inplace=True)
    win_rate_df.reset_index(drop=True, inplace=True)

    return win_rate_df


# 示例输入，其中包括两个隐藏的英雄
input_heroes = ['骨王', '末日使者', '', '', '小黑']
input_heroes2 = ['人马', '', '', '', '美杜莎']
input_heroes3 = ['潮汐', '全能骑士', '', '', '冰女']

# 获取胜率最高的队伍
high_win_rate_teams_df = dianfeng_find_high_win_rate_teams(input_heroes, df_battles)
high_win_rate_teams_df2 = dianfeng_find_high_win_rate_teams(input_heroes2, df_battles)
high_win_rate_teams_df3 = dianfeng_find_high_win_rate_teams(input_heroes3, df_battles)
print(high_win_rate_teams_df)
print(high_win_rate_teams_df2)
print(high_win_rate_teams_df3)
