import pandas as pd

# import template and working excels
move_df = pd.read_excel('../all_moves_details.xlsx')
tm_df = pd.read_csv('../tm_list.txt', header=None, names=['tm'])
tm_df['tm_id'] = tm_df['tm'].str.lower()  # format tm list to join on movelist
tm_df['tm_id'] = tm_df['tm_id'].str.replace('_','')

tm_details = tm_df.join(move_df.set_index('Simple Move Name'), on='tm_id')

tm_details.to_excel('./output/tm_details.xlsx', index=False)
