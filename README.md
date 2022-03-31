# KachnaBot

## Setup
```sh
sudo apt install python3-pip ffmpeg
pip3 install -r requirements.txt
python main.py
mkdir -p ~monitor/.config/systemd/user/multi-user.target.wants/
ln ~monitor/KachnaBot/kachnabot.service ~monitor/.config/systemd/user/kachnabot.service
ln -s ~monitor/.config/systemd/user/kachnabot.service ~monitor/.config/systemd/user/multi-user.target.wants/kachnabot.service
systemctl --user daemon-reload
systemctl --user status kachnabot.service
systemctl --user --now enable kachnabot.service
```

## Run

**Aplikace potřebuje běžet pod běžným uživatelem. Kvůli přístupu ke zvukové kartě.**

Na produkci je aplikace nasazena jako systemd user service `systemctl --user status kachnabot.service`.
Spusť pomocí `systemctl --user start kachna_bot.service`
