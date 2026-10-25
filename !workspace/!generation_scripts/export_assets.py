### organize sprites and audio into assets folder for pokerogue
import pandas as pd
import os
import shutil
import math
import json
from PIL import Image as img

showdown_dir = "../raw showdown files/monsterhunter/"
audio_in_dir = "../own assets/audio/"
sprite_in_dir = "../own assets/sprites/"
audio_out_dir = "../!!output/assets/audio/cry/"
sprite_out_dir = "../!!output/assets/images/pokemon/"
icon_out_dir = "../!!output/assets/images/"

# helper function to convert string to lowerCamelCase
def camelcase(text):
    temp = text.replace('_', ' ').replace('-', ' ').title().replace(' ', '')  # separate each word by spaces, capitalize first letter of each, then remove spaces
    res = temp[0].lower() + temp[1:] # lowercase the first letter
    return res

# helper function to format .json file for sprites
def sprite_json(spritename, h, w):
    return """{
	"textures": [
		{
			"image": \"""" + spritename + """\",
			"format": "RGBA8888",
			"size": {
				"w": """ + w + """,
				"h": """ + h + """
			},
			"scale": 1,
			"frames": [
				{
					"filename": "0001.png",
					"rotated": false,
					"trimmed": false,
					"sourceSize": {
						"w": """ + w + """,
						"h": """ + h + """
					},
					"spriteSourceSize": {
						"x": 0,
						"y": 0,
						"w": """ + w + """,
						"h": """ + h + """
					},
					"frame": {
						"x": 0,
						"y": 0,
						"w": """ + w + """,
						"h": """ + h + """
					}
				}
			]
		}
	]
}"""

# helper function to format part of .json file for icons
def icons_json(spritename, h, w, x, y):
    json = {
        "filename": spritename,
        "rotated": False,
        "trimmed": False,
        "sourceSize": {
            "w": int(w),
            "h": int(h)
        },
        "spriteSourceSize": {
                "x": 0,
                "y": 0,
                "w": int(w),
                "h": int(h)
        },
        "frame": {
                "x": int(x),
                "y": int(y),
                "w": int(w),
                "h": int(h)
        }
    }
    return json

# helper functions to copy sprites by filepath
def export_sprite(sprite_outpath, sprite_out_name, sprite_in_name, mon_name, is_icon=False, is_back=False, variant_suffix=None):
    front_or_back = "front/"
    sprite_in_name_base = sprite_in_name
    
    if is_back == True: front_or_back = "back/"
    elif variant_suffix is not None:  # if shiny/variant that is missing sprite, fall back to custom non-shiny
        sprite_in_name_base = sprite_in_name[:0-len(variant_suffix)]  # cut last characters of sprite name to trim suffix
    
    if is_icon == False:
        # front and back handled together for non-icon sprites
        # copy the sprite itself first
        if os.path.isfile(sprite_in_dir + front_or_back + sprite_in_name + ".png"):  # if sprite exists in own asset directory, use it
            shutil.copy(sprite_in_dir + front_or_back + sprite_in_name + ".png", sprite_outpath + sprite_out_name + ".png")
        elif variant_suffix is not None and os.path.isfile(sprite_in_dir + front_or_back + sprite_in_name_base + ".png"):
            shutil.copy(sprite_in_dir + front_or_back + sprite_in_name_base + ".png", sprite_outpath + sprite_out_name + ".png")
        elif os.path.isfile(showdown_dir + "sprites/" + front_or_back + mon_name + ".png"):  # if not, copy and rename sprite from showdown if it exists
            shutil.copy(showdown_dir + "sprites/" + front_or_back + mon_name + ".png", sprite_outpath + sprite_out_name + ".png")
        else:  # otherwise, fall back to placeholder sprite
            shutil.copy(sprite_in_dir + "fallback.png", sprite_outpath + sprite_out_name + ".png")
        # create the .json of the sprite next
        sprite_out = img.open(sprite_outpath + sprite_out_name + ".png")
        h, w = sprite_out.size
        with open(sprite_outpath + sprite_out_name + ".json", "w", encoding="utf-8") as json_file:
            json_file.write(sprite_json(sprite_out_name + ".png", str(h), str(w)))
            
    else:
        if os.path.isfile(sprite_in_dir + "icons/" + sprite_in_name + ".png"):  # if sprite exists in own asset directory, use it
            shutil.copy(sprite_in_dir + "icons/" + sprite_in_name + ".png", sprite_outpath + sprite_out_name + ".png")
        elif os.path.isfile(showdown_dir + "sprites/icons/" + mon_name + ".png"):  # if not, copy and rename sprite from showdown if it exists
            shutil.copy(showdown_dir + "sprites/icons/" + mon_name + ".png", sprite_outpath + sprite_out_name + ".png")
        else:  # otherwise, fall back to placeholder sprite
            shutil.copy(sprite_in_dir + "icons/fallback.png", sprite_outpath + sprite_out_name + ".png")

# helper function to initialize images for icon spritesheets by copying and extending original sheet
def init_icon_sheet(sheet_outpath, sheet_inpath, num_mons):
    # open original sheet from pokerogue and get its dimensions
    icon_sheet = img.open(sheet_inpath)
    img_size = icon_sheet.size
    
    # get height of original sheet for the given generation
    sheet_height = img_size[1]
    num_rows = sheet_height // 40
    num_cols = -(num_mons // -num_rows)
    new_width = img_size[0] + num_cols * 40

    # create new sheet at the output folder with new dimensions
    new_sheet = img.new(mode="RGBA", size=(new_width, sheet_height), color=(0,0,0,0))
    new_sheet.paste(icon_sheet, (0, 0, img_size[0], img_size[1]))

    # export sheet to outpath
    new_sheet.save(sheet_outpath)
    
    # return original image size for tracking later
    return img_size

# helper function to add icon to respective spritesheet
def add_to_icon_sheet(sheet_outpath, icon_name, mon_name, icon_index, og_sheet_size):
    # get icon sprite
    icon_img = None
    if os.path.isfile(sprite_in_dir + "icons/" + icon_name + ".png"):  # if sprite exists in own asset directory, use it
        icon_img = img.open(sprite_in_dir + "icons/" + icon_name + ".png")
    elif os.path.isfile(showdown_dir + "sprites/icons/" + mon_name + ".png"):  # if not, copy and rename sprite from showdown if it exists
        icon_img = img.open(showdown_dir + "sprites/icons/" + mon_name + ".png")
    else:  # otherwise, fall back to placeholder sprite
        icon_img = img.open(sprite_in_dir + "icons/fallback.png")

    # get icon parameters for pasting into spritesheet
    icon_w = icon_img.size[0]
    icon_h = icon_img.size[1]

    # calculate position in spritesheet
    start_x = og_sheet_size[0]
    sheet_height = og_sheet_size[1]
    num_rows = sheet_height // 40
    row_idx = icon_index % num_rows
    col_idx = icon_index // num_rows

    icon_x = start_x + col_idx * 40
    icon_y = row_idx * 40
    
    # copy paste icon into sheet
    icon_sheet = img.open(sheet_outpath + '.png')
    icon_sheet.paste(icon_img, (icon_x, icon_y))
    icon_sheet.save(sheet_outpath + '.png')

    # add text block to .json definition
    # open json file and navigate to where icons are being added
    icon_json_file = open(sheet_outpath + '.json', 'r')
    icon_json = json.load(icon_json_file)
    icon_json_file.close()
    icon_sheet_list = icon_json['textures'][0]['frames']

    # append formatted json and save the file
    #print(icons_json(icon_name, str(icon_h), str(icon_w), str(icon_x), str(icon_y)))
    icon_sheet_list.append(icons_json(icon_name, str(icon_h), str(icon_w), str(icon_x), str(icon_y)))

    icon_json_file = open(sheet_outpath + '.json', 'w')
    json.dump(icon_json, icon_json_file, indent = 4, ensure_ascii=False)
    icon_json_file.close()
    
    #icon_json.write(icons_json(icon_name, str(icon_h), str(icon_w), str(icon_x), str(icon_y)))
    #icon_json.close()

# import mons and movelists
mon_df = pd.read_excel('./worksheets/pokedex.xlsx')
# delete existing colors before appending
if os.path.isfile("../!!output/assets/starter-colors.json.add"): os.remove("../!!output/assets/starter-colors.json.add")


# filter pokedex to only enabled mons and only if all the relevant fields are filled
mon_df = mon_df[mon_df['enabled'] == 'y']
mon_df = mon_df[~mon_df['dex_num'].isnull()]
mon_df = mon_df[~mon_df['Passive Ability'].isnull()]
mon_df = mon_df[~mon_df['Egg Move 1'].isnull()]
mon_df = mon_df[~mon_df['Egg Move 2'].isnull()]
mon_df = mon_df[~mon_df['Egg Move 3'].isnull()]
mon_df = mon_df[~mon_df['Egg Move 4 (rare)'].isnull()]

# initialize parameters for icon sheets
shutil.copy('../pokerogue assets/starter-colors.json', '../!!output/assets/starter-colors.json')
mons_in_each_gen = {}
icon_sheet_shapes = {}
gen_icon_index = {}
# get number of mons for each gen
for i, mon in mon_df.iterrows():
    gen = int(mon['gen'])
    if gen in mons_in_each_gen: mons_in_each_gen[gen] += 1
    else:
        mons_in_each_gen[gen] = 1
        gen_icon_index[str(gen)] = 0

# initialize icon sheets and their .json
for gen in mons_in_each_gen.keys():
    icon_sheet_shapes[str(gen)] = init_icon_sheet(icon_out_dir + 'pokemon_icons_' + str(gen) + '.png', '../pokerogue assets/pokemon_icons_' + str(gen) + '.png', mons_in_each_gen[gen] * 2)
    icon_sheet_shapes[str(gen) + 'v'] = init_icon_sheet(icon_out_dir + 'pokemon_icons_' + str(gen) + 'v.png', '../pokerogue assets/pokemon_icons_' + str(gen) + 'v.png', mons_in_each_gen[gen] * 2)
    shutil.copy('../pokerogue assets/pokemon_icons_' + str(gen) + '.json', icon_out_dir + 'pokemon_icons_' + str(gen) + ".json")
    shutil.copy('../pokerogue assets/pokemon_icons_' + str(gen) + 'v.json', icon_out_dir + 'pokemon_icons_' + str(gen) + "v.json")
    #icon_json = open(icon_out_dir + 'pokemon_icons_' + str(gen) + ".json.add", "w", encoding="utf-8")
    #icon_v_json = open(icon_out_dir + 'pokemon_icons_' + str(gen) + "v.json.add", "w", encoding="utf-8")

# iterate each mon to handle their sprites and audio
for i, mon in mon_df.iterrows():
    #print(mon)
    # shorthand variables
    mon_lower = mon['ID'].lower().replace("_","")
    dex_num = str(int(mon['dex_num'] + 1500))
    gen = str(int(mon['gen']))
    
    audio_filename = dex_num + ".m4a"
    
    ### audio
    if os.path.isfile(audio_in_dir + audio_filename):  # if audio exists in own asset directory, use it
        shutil.copy(audio_in_dir + audio_filename, audio_out_dir + audio_filename)
    else:  # otherwise, fall back to empty placeholder sound
        shutil.copy(audio_in_dir + "fallback.m4a", audio_out_dir + audio_filename)

    ### sprites
    # each of normal, shiny, and 2 variants have to be handled separately due to different paths
    # copy the icons first - will still need to add them into the sheets manually

    # normal
    export_sprite(sprite_out_dir + "icons/" + gen + "/", dex_num, dex_num, mon_lower, is_icon=True)  # icon
    export_sprite(sprite_out_dir, dex_num, dex_num, mon_lower)  # front
    export_sprite(sprite_out_dir + "back/", dex_num, dex_num, mon_lower, is_back=True)  # back
    # shiny
    export_sprite(sprite_out_dir + "icons/" + gen + "/", dex_num + "s", dex_num + "s", mon_lower, is_icon=True, variant_suffix="s")  # icon
    export_sprite(sprite_out_dir + "shiny/", dex_num, dex_num + "s", mon_lower, variant_suffix="s")  # front
    export_sprite(sprite_out_dir + "back/shiny/", dex_num, dex_num + "s", mon_lower, is_back=True, variant_suffix="s")  # back
    # variant 2
    export_sprite(sprite_out_dir + "icons/variant/" + gen + "/", dex_num + "_2", dex_num + "_2", mon_lower, is_icon=True, variant_suffix="_2")  # icon
    export_sprite(sprite_out_dir + "variant/", dex_num + "_2", dex_num + "_2", mon_lower, variant_suffix="_2")  # front
    export_sprite(sprite_out_dir + "variant/back/", dex_num + "_2", dex_num + "_2", mon_lower, is_back=True, variant_suffix="_2")  # back
    # variant 3
    export_sprite(sprite_out_dir + "icons/variant/" + gen + "/", dex_num + "_3", dex_num + "_3", mon_lower, is_icon=True, variant_suffix="_3")  # icon
    export_sprite(sprite_out_dir + "variant/", dex_num + "_3", dex_num + "_3", mon_lower, variant_suffix="_3")  # front
    export_sprite(sprite_out_dir + "variant/back/", dex_num + "_3", dex_num + "_3", mon_lower, is_back=True, variant_suffix="_3")  # back

    ### icons
    # similar to sprites but have to be collected into a single new image to add to the spritesheet
    icon_outpath = icon_out_dir + 'pokemon_icons_' + gen
    
    add_to_icon_sheet(icon_outpath, dex_num, mon_lower, gen_icon_index[gen], icon_sheet_shapes[gen]) # normal
    add_to_icon_sheet(icon_outpath + 'v', dex_num + '_2', mon_lower, gen_icon_index[gen], icon_sheet_shapes[gen + 'v']) # variant 2 - do one in each sheet for indexing
    gen_icon_index[gen] += 1 # increment gen index
    add_to_icon_sheet(icon_outpath, dex_num + 's', mon_lower, gen_icon_index[gen], icon_sheet_shapes[gen]) # shiny
    add_to_icon_sheet(icon_outpath + 'v', dex_num + '_3', mon_lower, gen_icon_index[gen], icon_sheet_shapes[gen + 'v']) # variant 3
    gen_icon_index[gen] += 1

    # add candy colors
    candy_colors_file = open('../!!output/assets/starter-colors.json', 'r')
    candy_colors = json.load(candy_colors_file)
    candy_colors_file.close()
    
    candy_colors[dex_num] = [str(mon['candyColor1']), str(mon['candyColor2'])]
    
    candy_colors_file = open('../!!output/assets/starter-colors.json', 'w')
    json.dump(candy_colors, candy_colors_file)
    candy_colors_file.close()
    #with open("../!!output/assets/starter-colors.json.add", "a", encoding="utf-8") as candy_colors:
    #    candy_colors.write("\"" + dex_num + "\":[\"" + str(mon['candyColor1']) + "\",\"" + str(mon['candyColor2']) + "\"],")

