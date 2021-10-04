import argparse
import os
import pathlib
import random as rand
import struct as st
import sys
from os import stat
from shutil import copyfile
from time import time

import bossrando as boss_shuffler
import bossscaler as boss_scale
import characterwriter as char_slots
import charrando
import enemywriter as enemystuff
import fastmagic
import ipswriter as bigpatches
import logicwriter as keyitems
import logicwriter_chronosanity as chronosanity_logic
import patcher as patches
import randomizergui as gui
import roboribbon
import shopwriter as shops
import specialwriter as hardcoded_items
import tabchange as tabwriter
import techwriter as tech_order
import treasurewriter as treasures


def read_names():
    p = open("names.txt", "r")
    names = p.readline()
    names = names.split(",")
    p.close()
    return names


# Script variables
flags = ""
sourcefile = ""
outputfolder = ""
difficulty = ""
glitch_fixes = ""
#fast_move = ""
#sense_dpad = ""
lost_worlds = ""
boss_scaler = ""
zeal_end = ""
quick_pendant = ""
locked_chars = ""
tech_list = ""
seed = ""
tech_list = ""
unlocked_magic = ""
quiet_mode = ""
chronosanity = ""
tab_treasures = ""
boss_rando = ""
shop_prices = ""
duplicate_chars = ""
#
# Handle the command line interface for the randomizer.
#


def command_line():
    global flags
    global sourcefile
    global outputfolder
    global difficulty
    global glitch_fixes
#     global fast_move
#     global sense_dpad
    global lost_worlds
    global boss_scaler
    global zeal_end
    global quick_pendant
    global locked_chars
    global tech_list
    global seed
    global tech_list_balanced
    global unlocked_magic
    global quiet_mode
    global chronosanity
    global tab_treasures
    global boss_rando
    global shop_prices
    global duplicate_chars
    global same_char_techs
    global char_choices

    flags = ""

    parser = argparse.ArgumentParser(description="Crono Trigger Jets of Time Randomizer")

    parser.add_argument('sourcefile', type=str)
    parser.add_argument('outputfolder', type=str)

    parser.add_argument('--seed', type=str, default=None)
    parser.add_argument('--difficulty', type=str, default="Normal", choices=['easy', 'normal', 'hard'])

    parser.add_argument('--glitch_fixes', action='store_true')
    # parser.add_argument('--fast_move', action='store_true')
    # parser.add_argument('--sense_dpad', action='store_true')
    parser.add_argument('--lost_worlds', action='store_true')
    parser.add_argument('--boss_scaler', action='store_true')
    parser.add_argument('--boss_rando', action='store_true')
    parser.add_argument('--zeal_end', action='store_true')
    parser.add_argument('--quick_pendant', action='store_true')
    parser.add_argument('--locked_chars', action='store_true')
    parser.add_argument('--tech_list', action='store_true')
    parser.add_argument('--tech_list_balanced', action='store_true')
    parser.add_argument('--unlocked_magic', action='store_true')
    parser.add_argument('--quiet_mode', action='store_true')
    parser.add_argument('--chronosanity', action='store_true')
    parser.add_argument('--duplicate_chars', action='store_true')
    parser.add_argument('--same_char_techs', action='store_true')
    parser.add_argument('--tab_treasures', action='store_true')
    parser.add_argument('--shop_prices', default="normal", choices=['normal', 'free', 'mostly_random', 'fully_random'])

    args = parser.parse_args()

    sourcefile = args.sourcefile
    sourcefile = sourcefile.strip("\"")
    if sourcefile.find(".sfc") == -1:
        if sourcefile.find(".smc") == - 1:
            input("Invalid File Name. Try placing the ROM in the same folder as the randomizer. Also, try writing the extension(.sfc/smc).")
            exit()

    outputfolder = args.outputfolder

    seed = args.seed
    if seed is None or seed == "":
        names = read_names()
        seed = "".join(rand.choice(names) for i in range(2))
    rand.seed(seed)

    difficulty = args.difficulty
    flags = flags + difficulty[0]

    glitch_fixes = "Y" if args.glitch_fixes else "N"
    if glitch_fixes == "Y":
        flags = flags + "g"

    #fast_move = "Y" if args.fast_move else "N"
    # if fast_move == "Y":
    #   flags = flags + "s"

    #sense_dpad = "Y" if args.sense_dpad else "N"
    # if sense_dpad == "Y":
    #   flags = flags + "d"

    lost_worlds = "Y" if args.lost_worlds else "N"
    if lost_worlds == "Y":
        flags = flags + "l"

    boss_scaler = "Y" if args.boss_scaler else "N"
    if boss_scaler == "Y":
        flags = flags + "b"

    boss_rando = "Y" if args.boss_rando else "N"
    if boss_rando == "Y":
        flags = flags + "ro"

    zeal_end = "Y" if args.zeal_end else "N"
    if zeal_end == "Y":
        flags = flags + "z"
    if lost_worlds == "Y":
        pass
    else:
        quick_pendant = "Y" if args.quick_pendant else "N"
        if quick_pendant == "Y":
            flags = flags + "p"

    locked_chars = "Y" if args.locked_chars else "N"
    if locked_chars == "Y":
        flags = flags + "c"

    tech_list = "Y" if args.tech_list else "N"
    if tech_list == "Y":
        flags = flags + "te"
        tech_list = "Fully Random"
        tech_list_balanced = "Y" if args.tech_list_balanced else "N"
        if tech_list_balanced == "Y":
            flags = flags + "x"
            tech_list = "Balanced Random"

    unlocked_magic = "Y" if args.unlocked_magic else "N"
    if unlocked_magic == "Y":
        flags = flags + "m"

    quiet_mode = "Y" if args.quiet_mode else "N"
    if quiet_mode == "Y":
        flags = flags + "q"

    chronosanity = "Y" if args.chronosanity else "N"
    if chronosanity == "Y":
        flags = flags + "cr"

    duplicate_chars = "Y" if args.duplicate_chars else "N"
    if duplicate_chars == "Y":
        flags = flags + "dc"
        same_char_techs = "Y" if args.same_char_techs else "N"
    else:
        same_char_techs = "N"

    tab_treasures = "Y" if args.tab_treasures else "N"
    if tab_treasures == "Y":
        flags = flags + "tb"

    shop_prices = {
        'normal': 'Normal',
        'free': 'Free',
        'mostly_random': 'Mostly Random',
        'fully_random': 'Fully Random'
    }[args.shop_prices]

    if shop_prices == "F":
        shop_prices = "Free"
        flags = flags + "spf"
    elif shop_prices == "M":
        shop_prices = "Mostly Random"
        flags = flags + "spm"
    elif shop_prices == "R":
        shop_prices = "Fully Random"
        flags = flags + "spr"
    else:
        shop_prices = "Normal"


#
# Generate the randomized ROM.
#


def generate_rom():
    global flags
    global sourcefile
    global outputfolder
    global difficulty
    global glitch_fixes
    global fast_move
    global sense_dpad
    global lost_worlds
    global boss_rando
    global boss_scaler
    global zeal_end
    global quick_pendant
    global locked_chars
    global tech_list
    global seed
    global unlocked_magic
    global quiet_mode
    global chronosanity
    global tab_treasures
    global shop_prices
    global duplicate_chars
    global same_char_techs
    global char_choices

    # isolate the ROM file name
    inputPath = pathlib.Path(sourcefile)
    outfile = inputPath.name

    # Create the output file name
    outfile = outfile.split(".")
    outfile = str(outfile[0])
    if flags == "":
        outfile = "%s.%s.sfc" % (outfile, seed)
    else:
        outfile = "%s.%s.%s.sfc" % (outfile, flags, seed)

    # Append the output file name to the selected directory
    # If there is no selected directory, use the input path
    if outputfolder == None or outputfolder == "":
        outfile = str(inputPath.parent.joinpath(outfile))
    else:
        outfile = str(pathlib.Path(outputfolder).joinpath(outfile))

    size = stat(sourcefile).st_size
    if size % 0x400 == 0:
        copyfile(sourcefile, outfile)
    elif size % 0x200 == 0:
        print("SNES header detected. Removing header from output file.")
        f = open(sourcefile, 'r+b')
        data = f.read()
        f.close()
        data = data[0x200:]
        open(outfile, 'w+').close()
        f = open(outfile, 'r+b')
        f.write(data)
        f.close()
    print("Applying patch. This might take a while.")
    bigpatches.write_patch_alt("patch.ips", outfile)
    patches.patch_file("patches/patch_codebase.txt", outfile)
    if glitch_fixes == "Y":
        patches.patch_file("patches/save_anywhere_patch.txt", outfile)
        patches.patch_file("patches/unequip_patch.txt", outfile)
        patches.patch_file("patches/fadeout_patch.txt", outfile)
        patches.patch_file("patches/hp_overflow_patch.txt", outfile)
    patches.patch_file("patches/fast_overworld_walk_patch.txt", outfile)
    patches.patch_file("patches/faster_epoch_patch.txt", outfile)
    patches.patch_file("patches/faster_menu_dpad.txt", outfile)
    if zeal_end == "Y":
        patches.patch_file("patches/zeal_end_boss.txt", outfile)
    if lost_worlds == "Y":
        bigpatches.write_patch_alt("patches/lost.ips", outfile)
    if lost_worlds == "Y":
        pass
    elif quick_pendant == "Y":
        patches.patch_file("patches/fast_charge_pendant.txt", outfile)
    if unlocked_magic == "Y":
        fastmagic.set_fast_magic_file(outfile)
        # bigpatches.write_patch_alt("patches/fastmagic.ips",outfile)
    if difficulty == "hard":
        bigpatches.write_patch_alt("patches/hard.ips", outfile)
    tabwriter.rewrite_tabs(outfile)  # Psuedoarc's code to rewrite Power and Magic tabs and make them more impactful
    roboribbon.robo_ribbon_speed_file(outfile)
    print("Randomizing treasures...")
    treasures.randomize_treasures(outfile, difficulty, tab_treasures)
    hardcoded_items.randomize_hardcoded_items(outfile, tab_treasures)
    print("Randomizing enemy loot...")
    enemystuff.randomize_enemy_stuff(outfile, difficulty)
    print("Randomizing shops...")
    shops.randomize_shops(outfile)
    shops.modify_shop_prices(outfile, shop_prices)
    print("Randomizing character locations...")
    char_locs = char_slots.randomize_char_positions(outfile, locked_chars, lost_worlds)
    print("Now placing key items...")
    if chronosanity == "Y":
        chronosanity_logic.writeKeyItems(
            outfile, char_locs, (locked_chars == "Y"), (quick_pendant == "Y"), lost_worlds == "Y")
    elif lost_worlds == "Y":
        keyitemlist = keyitems.randomize_lost_worlds_keys(char_locs, outfile)
    else:
        keyitemlist = keyitems.randomize_keys(char_locs, outfile, locked_chars)
    if boss_scaler == "Y" and chronosanity != "Y":
        print("Rescaling bosses based on key items..")
        boss_scale.scale_bosses(char_locs, keyitemlist, locked_chars, outfile)
    #print("Boss rando: " + boss_rando)
    if boss_rando == "Y":
        boss_shuffler.randomize_bosses(outfile, difficulty)
        boss_shuffler.randomize_dualbosses(outfile, difficulty)
    # going to handle techs differently for dup chars
    if duplicate_chars == "Y":
        charrando.reassign_characters_file(outfile, char_choices,
                                           same_char_techs == "Y",
                                           tech_list,
                                           lost_worlds == "Y")
    else:
        if tech_list == "Fully Random":
            tech_order.take_pointer(outfile)
        elif tech_list == "Balanced Random":
            tech_order.take_pointer_balanced(outfile)

    if quiet_mode == "Y":
        bigpatches.write_patch_alt("patches/nomusic.ips", outfile)
    # Tyrano Castle chest hack
    f = open(outfile, "r+b")
    f.seek(0x35F6D5)
    f.write(st.pack("B", 1))
    f.close()
    # Mystic Mtn event fix in Lost Worlds
    if lost_worlds == "Y":
        f = open(outfile, "r+b")
        bigpatches.write_patch_alt("patches/mysticmtnfix.ips", outfile)
    # Bangor Dome event fix if character locks are on
  #      if locked_chars == "Y":
  #        bigpatches.write_patch_alt("patches/bangorfix.ips",outfile)
        f.close()
    print("Randomization completed successfully.")


if __name__ == "__main__":
    command_line()
    generate_rom()
