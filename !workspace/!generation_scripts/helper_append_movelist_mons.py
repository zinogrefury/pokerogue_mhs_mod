### helper script - appends movelists not in the main movelist Excel
# do need to reformat on your own after

import pandas as pd

# import template and working excels
moves_template = pd.read_excel('./worksheets/movesets_template.xlsx')
moves_file = pd.read_excel('./worksheets/movesets.xlsx')

# exclude mons from template that are already in the working file
moves_template = moves_template[~moves_template['ID'].isin(moves_file['ID'])]


# append truncated template to moveset
moves_file = pd.concat([moves_file, moves_template])
#print(moves_file)

moves_file.sort_values(by=['dex_num', 'level', 'move'], inplace=True)
moves_file.to_excel('./worksheets/movesets.xlsx', index=False)
