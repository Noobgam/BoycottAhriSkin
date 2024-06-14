# What is this?

This repo contains code to automatically ban ahri in every gamemode where you have bans.

# Why?

In case you're living under a rock, Riot are making questionable decisions.

As an example of explanation video: [Rival](https://youtu.be/EDkw-Qq8-ks?si=UiGBXGrPCE4wPng6)

# How to use it?

1. Download the latest release from github. [link](https://github.com/Noobgam/BoycottAhriSkin/releases/download/readme-release/main.exe)
2. Open league
3. Run the binary
4Enter any queue/match you want, Ahri will get automatically banned when it's your turn

# Will I get banned for it?

Not sure. LCU is approved by Riot (a.k.a. Milk The Whales LLC), but automating actions during the champ select has never been approved.

Similar scripts have been used extensively to run bots by people, you're unlikely to get banned, but use at your own risk.

# What about Vanguard?

Vanguard is seemingly completely useless, all the bots that are using LCU and even those that are not are still not getting banned.

# How is the release built?

1. create venv
2. `pip install -r requirements.txt`
3. `pyinstaller --onefile main.py`
4. `./dist/main.exe`