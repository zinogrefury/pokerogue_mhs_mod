### helper script - read pokedex from showdown file and export to Excel
# make sure to convert the .ts to .json

import pandas as pd

# initialize dex list - stored as dict of dicts
dex_dict = {}

# import json
dex_json = pd.read_json('../pokedex.json').transpose()
dex_json['id'] = dex_json.index
dex_json.rename(columns={'name': 'friendly_name'}, inplace=True)
dex_json['index'] = range(len(dex_json))
dex_json.set_index('index', inplace=True)

#print(dex_json)

#for i, row in dex_json.iterrows():
#    print(row.id)


# iterate each mon
for i, row in dex_json.iterrows():
    # initialize dict and populate with fields
    dex_dict[i] = {}
    dex_dict[i]['index'] = i
    dex_dict[i]['og_dex_num'] = row.num
    dex_dict[i]['id'] = row.friendly_name.upper().replace(' ', '_').replace('-', '_')
    dex_dict[i]['name'] = row.friendly_name
    dex_dict[i]['type1'] = row.types[0]
    dex_dict[i]['type2'] = None if len(row.types) == 1 else row.types[1]
    dex_dict[i]['hp'] = row.baseStats['hp']
    dex_dict[i]['atk'] = row.baseStats['atk']
    dex_dict[i]['def'] = row.baseStats['def']
    dex_dict[i]['spa'] = row.baseStats['spa']
    dex_dict[i]['spd'] = row.baseStats['spd']
    dex_dict[i]['spe'] = row.baseStats['spe']
    dex_dict[i]['abil1'] = row.abilities['0']
    dex_dict[i]['abil2'] = None if '1' not in row.abilities else row.abilities['1']
    dex_dict[i]['abilh'] = None if 'H' not in row.abilities else row.abilities['H']
    dex_dict[i]['weight'] = round(row.weightkg,1)
    

#for row in dex_dict.values():
#    print(row)


# convert dex dict to dataframe
dex_export = pd.DataFrame.from_dict(dex_dict).transpose()

# export raw dataframe to Excel
dex_export.to_excel('./worksheets/pokedex_raw.xlsx', index=False)

# add empty columns to dataframe to create template for editing
dex_export.insert(loc=15, column='eggmove4', value=None)
dex_export.insert(loc=15, column='eggmove3', value=None)
dex_export.insert(loc=15, column='eggmove2', value=None)
dex_export.insert(loc=15, column='eggmove1', value=None)
dex_export.insert(loc=15, column='abilp', value=None)
dex_export.insert(loc=4, column='category', value=None)
dex_export.insert(loc=2, column='gen', value=None)
dex_export.insert(loc=1, column='dex_num', value=None)
dex_export.insert(loc=0, column='enabled', value=None)
dex_export['height'] = None
dex_export['malePercent'] = 50
dex_export['catchRate'] = None
dex_export['baseFriendship'] = 50
dex_export['baseExp'] = None
dex_export['growthRate'] = 'MEDIUM_SLOW'
dex_export['starterCost'] = None
dex_export['eggTier'] = 'RARE'
dex_export['candyColor1'] = 'DDDDDD'
dex_export['candyColor2'] = '222222'

# export templated dataframe
dex_export.to_excel('./worksheets/pokedex_template.xlsx', index=False)
