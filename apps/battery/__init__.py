# Your app's directory
APP_DIR = "/system/apps/battery"

import os
import sys

# Standalone bootstrap for finding app assets
os.chdir(APP_DIR)

# Standalone bootstrap for module imports
sys.path.insert(0, APP_DIR)

from badgeware import set_brightness

set_brightness(0.2)
screen.font = rom_font.winds

# Battery geometry, laid out for Blinky's 39x26 matrix
BODY_X = 5
BODY_Y = 1
BODY_W = 27
BODY_H = 12
NUB_W = 2
NUB_H = 6
TEXT_Y = BODY_Y + BODY_H + 2

SAMPLE_MS = 500         # how often the battery is re-read
FLASH_MS = 500          # half-period of the flash
LOW_FLASH_MS = 200      # faster flash once the battery is low
LOW_LEVEL = 20
CHARGE_SWEEP_MS = 2000  # time for the charging fill animation to sweep to full

bright = color.white
dim = color.rgb(70, 70, 70)

level = clamp(badge.battery_level(), 0, 100)
charging = badge.is_charging()
last_sample = badge.ticks


def sample():
    global level, charging, last_sample

    if badge.ticks - last_sample >= SAMPLE_MS:
        level = clamp(badge.battery_level(), 0, 100)
        charging = badge.is_charging()
        last_sample = badge.ticks


def fill_level():
    # while charging the fill sweeps from the current level up to full
    if charging:
        sweep = (badge.ticks % CHARGE_SWEEP_MS) / CHARGE_SWEEP_MS
        return level + (100 - level) * sweep
    return level


def draw_battery(fill, pen):
    # outline and terminal nub
    screen.pen = pen
    screen.rectangle(BODY_X, BODY_Y, BODY_W, BODY_H)
    screen.rectangle(BODY_X + BODY_W, BODY_Y + (BODY_H - NUB_H) // 2, NUB_W, NUB_H)
    screen.pen = color.black
    screen.rectangle(BODY_X + 1, BODY_Y + 1, BODY_W - 2, BODY_H - 2)

    # fill proportional to the battery percentage
    inner_w = BODY_W - 4
    width = int(inner_w * fill / 100 + 0.5)
    if width > 0:
        screen.pen = pen
        screen.rectangle(BODY_X + 2, BODY_Y + 2, width, BODY_H - 4)


def draw_percentage():
    screen.pen = bright
    text = f"{level}%"
    w, _ = screen.measure_text(text)
    screen.text(text, (screen.width - w) // 2, TEXT_Y)


def update():
    sample()

    screen.pen = color.black
    screen.clear()

    period = LOW_FLASH_MS if level <= LOW_LEVEL and not charging else FLASH_MS
    pen = bright if (badge.ticks // period) % 2 == 0 else dim

    draw_battery(fill_level(), pen)
    draw_percentage()


run(update)
