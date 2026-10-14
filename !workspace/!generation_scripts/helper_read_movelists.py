### helper script - read pokemon movelists from showdown file and export to Excel
# make sure to convert the .ts to .json

import pandas as pd

# initialize movelist - stored as dict of dicts
moves_dict = {}

# import json
moves_json = pd.read_json('../learnsets.json').transpose()

#print(moves_json)

#for i, row in moves_json.iterrows():
#    print(row)

i = 0
for mon_name, row in moves_json.iterrows():
    for move in row.learnset.keys():
        moves_dict[i] = {}
        moves_dict[i]['mon'] = mon_name.upper().replace(' ', '_').replace('-', '_')
        moves_dict[i]['move'] = move
        moves_dict[i]['level'] = None
        for term in row.learnset[move]:
            if 'L' in term:
                lvl = term.split('L')[1]
                if not lvl.isdigit(): lvl = 1
                moves_dict[i]['level'] = int(lvl)
        i += 1

#for row in moves_dict.values():
#    print(row)

# convert movelist dict to dataframe
moves_export = pd.DataFrame.from_dict(moves_dict).transpose()

# export raw dataframe to Excel
moves_export.to_excel('./output/movesets_raw.xlsx', index=False)

### prep for editable list
# import monster list to restrict to just active mons
mon_df = pd.read_excel('./output/pokedex.xlsx')
mon_df_filtered = mon_df[mon_df['enabled'] == 'y']  # filter to only enabled mons

mon_df_filtered['ID_TRUNC'] = mon_df_filtered['ID'].replace('_', '', regex=True)

print(mon_df_filtered['ID'])

moves_export = moves_export[moves_export['mon'].isin(mon_df_filtered['ID_TRUNC'])]  # use isin() to limit list of moves
moves_export = moves_export.join(mon_df_filtered[['dex_num', 'ID', 'ID_TRUNC']].set_index('ID_TRUNC'), on='mon')
moves_export = moves_export[['dex_num', 'ID', 'move', 'level']]

#print(moves_export)

# import list of tms to mark learnable
tm_df = pd.read_csv('../tm_list.txt', header=None, names=['tm'])
tm_df['tm'] = tm_df['tm'].str.lower()  # format tm list to join on movelist
tm_df['tm'] = tm_df['tm'].str.replace('_','')

# use join() to quickly mark learnable tms
tm_df['is_tm'] = 'y'
moves_export = moves_export.join(tm_df.set_index('tm'), on='move')

#print(moves_export)

# import list of all moves in pokerogue to mark those from showdown that need to be implemented
# same process as with tms
all_moves_df = pd.read_csv('../all_moves_list.txt', header=None, names=['move_id'])
all_moves_df['join_move'] = all_moves_df['move_id'].str.lower()
all_moves_df['join_move'] = all_moves_df['join_move'].str.replace('_','')
all_moves_df['is_implemented'] = 'y'
moves_export = moves_export.join(all_moves_df.set_index('join_move'), on='move')
moves_export['move'] = moves_export[['move_id', 'move']].bfill(axis=1).iloc[:, 0]
moves_export = moves_export.drop('move_id', axis=1)

# sort list and export to template file
moves_export.sort_values(by=['dex_num', 'level', 'move'], inplace=True)
moves_export.to_excel('./output/movesets_template.xlsx', index=False)
