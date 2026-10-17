### organize sprites and audio into assets folder for pokerogue
import pandas as pd
import os
import shutil
from PIL import Image as img

showdown_dir = "../raw showdown files/monsterhunter/"
audio_in_dir = "../own assets/audio/"
sprite_in_dir = "../own assets/sprites/"
audio_out_dir = "../!!output/assets/audio/cry/"
sprite_out_dir = "../!!output/assets/images/pokemon/"

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

# set of helper functions to copy sprites by filepath
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

# import mons and movelists
mon_df = pd.read_excel('./worksheets/pokedex.xlsx')
# delete existing colors before appending
if os.path.isfile("../!!output/assets/starter-colors.json.add"): os.remove("../!!output/assets/starter-colors.json.add")

# filter pokedex to only enabled mons and only if all the relevant fields are filled
mon_df = mon_df[mon_df['enabled'] == 'y']
mon_df = mon_df[~mon_df['dex_num'].isnull()]
mon_df = mon_df[~mon_df['abilp'].isnull()]
mon_df = mon_df[~mon_df['eggmove1'].isnull()]
mon_df = mon_df[~mon_df['eggmove2'].isnull()]
mon_df = mon_df[~mon_df['eggmove3'].isnull()]
mon_df = mon_df[~mon_df['eggmove4'].isnull()]

# iterate each mon to handle their sprites and audio
for i, mon in mon_df.iterrows():
    # shorthand variables
    mon_lower = mon['id'].lower().replace("_","")
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

    # create candy colors

    
    with open("../!!output/assets/starter-colors.json.add", "a", encoding="utf-8") as candy_colors:
        candy_colors.write("\"" + dex_num + "\":[\"" + mon['candyColor1'] + "\",\"" + mon['candyColor2'] + "\"],")
