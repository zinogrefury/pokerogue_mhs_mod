### helper script - retrieves custom moves and abilities
# make sure to convert the .ts to .json

import pandas as pd

# initialize lists for both moves and abils - stored as dict of dicts
moves_dict = {}
abils_dict = {}

# import jsons
moves_json = pd.read_json('../custom_moves.json').transpose()
moves_json['id'] = moves_json.index
moves_json.rename(columns={'name': 'friendly_name'}, inplace=True)
moves_json['index'] = range(len(moves_json))
moves_json.set_index('index', inplace=True)

abils_json = pd.read_json('../custom_abils.json').transpose()
abils_json['id'] = abils_json.index
abils_json.rename(columns={'name': 'friendly_name'}, inplace=True)
abils_json.rename(columns={'shortDesc': 'desc2'}, inplace=True)
abils_json['index'] = range(len(abils_json))
abils_json.set_index('index', inplace=True)

# import mons and their movesets for joining
mon_df = pd.read_excel('./worksheets/pokedex_raw.xlsx')
move_df = pd.read_excel('./worksheets/movesets_raw.xlsx')

#print(moves_json)

# iterate moves to get relevant stats and descriptions
for ind, move in moves_json.iterrows():
    moves_dict[ind] = {}
    moves_dict[ind]['Move Name'] = move.friendly_name
    moves_dict[ind]['Type'] = move.type
    moves_dict[ind]['Category'] = move.category
    moves_dict[ind]['PP'] = move.pp
    moves_dict[ind]['Power'] = "-" if move.basePower == 0 else str(move.basePower)
    moves_dict[ind]['Accuracy'] = "-" if move.accuracy == True else move.accuracy
    moves_dict[ind]['ID'] = move.friendly_name.replace(" ", "_").replace("-", "_").replace("'", "").upper()
    moves_dict[ind]['Simplified ID'] = move.id

# same for abilities
for ind, abil in abils_json.iterrows():
    abils_dict[ind] = {}
    #print(abil)
    
    if str(abil['desc']) != 'nan': abil_desc = abil.desc
    elif str(abil['desc2']) != 'nan': abil_desc = abil.desc2
    else: abil_desc = ''
    
    abils_dict[ind]['Ability Name'] = abil.friendly_name
    abils_dict[ind]['ID'] = abil.friendly_name.replace(" ", "_").replace("-", "_").replace("'", "").upper()
    abils_dict[ind]['Description'] = abil_desc
    
# join mon/movelist data to get the list of mons that have each move/ability
moves_export = pd.DataFrame.from_dict(moves_dict).transpose()
abils_export = pd.DataFrame.from_dict(abils_dict).transpose()

# group mons that learn each move together and concatenate into list
move_df = move_df[move_df['move'].isin(moves_export['Simplified ID'])]  # use isin() to limit list of moves
move_df = move_df[['move', 'mon']]  # subset of columns
move_df.sort_values(by=['move','mon'], inplace=True)  # sort before grouping
move_df = move_df.groupby(['move'])['mon'].apply(', '.join).reset_index()
#print(move_df)
moves_export = moves_export.join(move_df.set_index('move'), on='Simplified ID')

# same for abilities - format so each abil is its own row first
abil_df = mon_df[['abil1', 'abil2', 'abilh', 'name']]  # subset of columns
abil_df = abil_df.melt(id_vars=['name'], var_name='abil_type', value_name='abil')  # use melt() to break down column values into rows
abil_df = abil_df[['abil', 'name']]  # subset of columns
abil_df = abil_df[abil_df['abil'].isin(abils_export['Ability Name'])]  # use isin() to limit list of moves
abil_df.sort_values(by=['abil','name'], inplace=True)  # sort before grouping
abil_df = abil_df.groupby(['abil'])['name'].apply(', '.join).reset_index()  # group by to concatenate mon names
#print(abil_df)
abils_export = abils_export.join(abil_df.set_index('abil'), on='Ability Name')
abils_export = abils_export[['Ability Name', 'ID', 'name', 'Description']]  # reorder columns

# sort and export both
moves_export.sort_values(by=["Type", "Category", "Power", "Accuracy", "Move Name"], inplace=True)
moves_export.to_excel('./worksheets/custom_moves.xlsx', index=False)

abils_export.sort_values(by=["Ability Name"], inplace=True)
abils_export.to_excel('./worksheets/custom_abils.xlsx', index=False)
