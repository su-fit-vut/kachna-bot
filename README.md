# KachnaBot

## Závislosti

* python3
* pip3
* sdl
* sdl-mixer
* portmidi

Na manjaru radši: `sudo pacman -S python-pygame`

## Setup
```sh
pip3 install -r requirements.txt
python main.py
```

**Aplikace potřebuje běžet pod běžným uživatelem. Kvůli přístupu ke zvukové kartě.**

Na produkci je aplikace nasazena jako systemd user service `systemctl --user status kachna_bot.service`.
