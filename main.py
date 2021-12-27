import requests, threading, os, datetime

e = datetime.datetime.now()
current_date = e.strftime("%Y-%m-%d-%H-%M-%S")


if not os.path.exists("Backups\\"):
    os.makedirs("Backups\\")
if not os.path.exists(f"Backups\\{current_date}\\"):
    os.makedirs(f"Backups\\{current_date}\\")
token = input("Token: ")


headers = {"Authorization": token}

r = requests.get(
    "https://discord.com/api/v9/users/@me/relationships",
    headers=headers,
)
print(f"{len(r.json())} Friends found!")

for frend in r.json():
    user = frend["user"]["username"] + frend["user"]["discriminator"]
    user_id = frend["user"]["id"]
    print(f"Username: {user} | User ID: {user_id}")
    with open(
        f"Backups\\{current_date}\\backedup-friends.txt",
        "a",
        encoding="utf-8",
        errors="ignore",
    ) as f:
        f.write(f"Username: {user} | User ID: {user_id}\n")


def get_invs(guild_id):
    indexx = 0
    while True:
        r = requests.get(
            f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=headers
        )
        try:
            chl_id = r.json()[indexx]["id"]
        except KeyError:
            break
        r = requests.post(
            f"https://discord.com/api/v9/channels/{chl_id}/invites",
            json={"max_age": 0, "max_uses": 0},
            headers=headers,
        )
        try:
            if "Missing Permissions" in r.text:
                indexx += 1

                continue
            elif "Unknown Channel" in r.text:
                indexx += 1

                continue
            elif r.status_code == 429:
                indexx += 1

                continue
            inv_code = r.json()["code"]
            server_name = r.json()["guild"]["name"]
            server_id = r.json()["guild"]["id"]
            print(f"discord.gg/{inv_code} | Name: {server_name} | ID: {server_id}")
            with open(f"Backups\\{current_date}\\backedup-invites.txt", "a") as f:
                f.write(
                    f"discord.gg/{inv_code} | Name: {server_name} | ID: {server_id}\n"
                )
            break
        except:
            indexx += 1
            continue


r = requests.get(
    "https://discord.com/api/v9/users/@me/guilds",
    headers=headers,
)
print(f"{len(r.json())} Guilds found!")
for guild in r.json():
    guild_id = guild["id"]
    while True:
        if threading.active_count() < 200:
            threading.Thread(target=get_invs, args=(guild_id.strip(),)).start()
            break
