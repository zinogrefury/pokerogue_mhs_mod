### create a file adding monhun mons by formatting mon and movelist data into a file
import pandas as pd

# helper function to convert string to camelCase
def camelcase(text):
    temp = text.replace('_', ' ').replace('-', ' ').title().replace(' ', '')
    res = temp[0].lower() + temp[1:]
    return res

# initialize master strings - will contain the files and important text to replace
species_txt = """import { EVOLVE_MOVE, RELEARN_MOVE } from "#app/constants";
import { EvoCondKey, EvolutionItem, SpeciesEvolution, SpeciesFormEvolution } from "#balance/pokemon-evolutions";
import { GrowthRate } from "#data/exp";
import {
  SpeciesFormChangeAbilityTrigger,
  SpeciesFormChangeItemTrigger,
  SpeciesFormChangeLapseTeraTrigger,
  SpeciesFormChangeTeraTrigger,
} from "#data/form-change-triggers";
import { Gender } from "#data/gender";
import { SpeciesFormChange } from "#data/pokemon-forms";
import { PokemonForm, PokemonSpecies } from "#data/pokemon-species";
import { AbilityId } from "#enums/ability-id";
import { EggTier } from "#enums/egg-type";
import { FormChangeItem } from "#enums/form-change-item";
import { MoveId } from "#enums/move-id";
import { PokemonType } from "#enums/pokemon-type";
import { SpeciesFormKey } from "#enums/species-form-key";
import { SpeciesId } from "#enums/species-id";
import { TimeOfDay } from "#enums/time-of-day";
import type { SpeciesDataMapConfig } from "#types/pokemon-species";

export function initGenerationMonhun(): SpeciesDataMapConfig {
  const generationMonhunSpeciesData: SpeciesDataMapConfig = {} as SpeciesDataMapConfig;
"""
eggmoves_txt = ""
enum_txt = ""
locale_mons_txt = ""
locale_categories_txt = ""


# import mons and movelists
mon_df = pd.read_excel('./worksheets/pokedex.xlsx')
move_df = pd.read_excel('./worksheets/movesets.xlsx')

# filter pokedex to only enabled mons and only if all the relevant fields are filled
mon_df = mon_df[mon_df['enabled'] == 'y']
mon_df = mon_df[~mon_df['dex_num'].isnull()]
mon_df = mon_df[~mon_df['abilp'].isnull()]
mon_df = mon_df[~mon_df['eggmove1'].isnull()]
mon_df = mon_df[~mon_df['eggmove2'].isnull()]
mon_df = mon_df[~mon_df['eggmove3'].isnull()]
mon_df = mon_df[~mon_df['eggmove4'].isnull()]

# filter movelist to only implemented moves
move_df = move_df[move_df['is_implemented'] == 'y']

# separate movelists for just levelups and just tms
level_move_df = move_df[~move_df['level'].isnull()]
tm_move_df = move_df[move_df['is_tm'] == 'y'].sort_values('move')

# iterate each mon to fill out the data struct
for i, mon in mon_df.iterrows():
    # prepare format for certain fields such as abilities
    mon_abil_1 = str(mon['abil1']).upper().replace(' ', '_').replace('-', '_')
    mon_abil_2 = "NONE" if pd.isnull(mon['abil2']) else str(mon['abil2']).upper().replace(' ', '_').replace('-', '_')
    mon_abil_h = "NONE" if pd.isnull(mon['abilh']) else str(mon['abilh']).upper().replace(' ', '_').replace('-', '_')
    mon_abil_p = str(mon['abilp']).upper().replace(' ', '_').replace('-', '_')

    # fill out non-iterated values for the mon
    # species
    species_txt += "  generationMonhunSpeciesData[SpeciesId." + mon['id'] + "] = {\n    species: new PokemonSpecies({\n"
    species_txt += "      id: SpeciesId." + mon['id'] + ",\n"
    species_txt += "      generation: " + str(mon['gen']) + ",\n"
    species_txt += "      category: \"" + mon['category'] + "\",\n"
    species_txt += "      type1: PokemonType." + mon['type1'].upper() + ",\n"
    species_txt += "      type2: PokemonType." + ("null" if pd.isnull(mon['type2']) else mon['type2'].upper()) + ",\n"
    species_txt += "      height: " + str(mon['height']) + ",\n"
    species_txt += "      weight: " + str(mon['weight']) + ",\n"
    species_txt += "      ability1: AbilityId." + mon_abil_1 + ",\n"
    species_txt += "      ability2: AbilityId." + ("NONE" if pd.isnull(mon_abil_2) else mon_abil_2) + ",\n"
    species_txt += "      abilityHidden: AbilityId." + ("NONE" if pd.isnull(mon_abil_h) else mon_abil_h) + ",\n"
    species_txt += "      baseTotal: " + str(mon['hp'] + mon['atk'] + mon['def'] + mon['spa'] + mon['spd'] + mon['spe']) + ",\n"
    species_txt += "      baseHp: " + str(mon['hp']) + ",\n"
    species_txt += "      baseAtk: " + str(mon['atk']) + ",\n"
    species_txt += "      baseDef: " + str(mon['def']) + ",\n"
    species_txt += "      baseSpatk: " + str(mon['spa']) + ",\n"
    species_txt += "      baseSpdef: " + str(mon['spd']) + ",\n"
    species_txt += "      baseSpd: " + str(mon['spe']) + ",\n"
    species_txt += "      catchRate: " + str(mon['catchRate']) + ",\n"
    species_txt += "      baseFriendship: " + str(mon['baseFriendship']) + ",\n"
    species_txt += "      baseExp: " + str(mon['baseExp']) + ",\n"
    species_txt += "      growthRate: GrowthRate." + mon['growthRate'] + ",\n"
    species_txt += "      malePercent: " + str(mon['malePercent']) + ",\n"
    species_txt += "      genderDiffs: false,\n"
    species_txt += "    }),\n"
    species_txt += "    starter: SpeciesId." + mon['id'] + ",\n"
    species_txt += "    starterCost: " + str(mon['starterCost']) + ",\n"
    species_txt += "    evolutions: [],\n"
    species_txt += "    eggTier: EggTier." + mon['eggTier'] + ",\n"
    species_txt += "    passives: AbilityId." + mon_abil_p + ",\n"

    # egg moves
    eggmoves_txt += "  [SpeciesId." + mon['id'] + "]: [ MoveId." + mon['eggmove1'] + ", MoveId." + mon['eggmove2'] + ", MoveId." + mon['eggmove3'] + ", MoveId." + mon['eggmove4'] + " ],\n"

    # species enums
    enum_txt += "  " + mon['id'] + " = " + str(int(mon['dex_num'] + 1500)) + ",\n"

    # species locale
    locale_mons_txt += "  \"" + camelcase(mon['id']) + "\": \"" + mon['name'] + "\",\n"
    
    # caterogy locale
    locale_categories_txt += "  \"" + camelcase(mon['id']) + "Category\": \"" + mon['category'] + "\",\n"

    # iterate movelists to fill out levelup and tm moves
    species_txt += "    levelMoves: [\n"
    for j, move in level_move_df[level_move_df['mon'] == mon['id']].iterrows():
        species_txt += "      [" + str(move['level']) + ", MoveId." + move['move'] + "],\n"
    species_txt += "    ],\n"
    
    species_txt += "    tms: [\n"
    for j, move in tm_move_df[tm_move_df['mon'] == mon['id']].iterrows():
        species_txt += "      MoveId." + move['move'] + ",\n"
    species_txt += "    ],\n"
    species_txt += "  };\n"

# write last sections of file
species_txt += "  return generationMonhunSpeciesData;\n"
species_txt += "}\n"

#print(species_txt)

# finally, write the contents to the output file
with open("../!!output/src/data/balance/species/generation-mh.ts", "w", encoding="utf-8") as f:
    f.write(species_txt)

with open("../!!output/src/data/balance/moves/egg-moves.ts.add", "w", encoding="utf-8") as f:
    f.write(eggmoves_txt)

with open("../!!output/src/enums/species-id.ts.add", "w", encoding="utf-8") as f:
    f.write(enum_txt)

with open("../!!output/locales/en/pokemon.json.add", "w", encoding="utf-8") as f:
    f.write(locale_mons_txt)

with open("../!!output/locales/en/pokemon-category.json.add", "w", encoding="utf-8") as f:
    f.write(locale_categories_txt)
