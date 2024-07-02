import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.op.gg/champions"


page = requests.get(url)


soup = BeautifulSoup(page.text, features="html.parser")


champion_rows = soup.find_all("tr")
champions = []


for rows in champion_rows:
    champion_name_tag = rows.find("strong")
    if champion_name_tag:
        champion_name = champion_name_tag.get_text(strip=True)
    else:
        champion_name = None
    Role_test = str(rows.find("td", class_="css-1amolq6 eyczova1"))
    start_index = Role_test.find('alt="') + len('alt="')
    end_index = Role_test.find('"', start_index)
    role = Role_test[start_index:end_index]


    try:
        win_rate = rows.find_all("td", class_="css-1amolq6 eyczova1")[1].text.strip()
    except:
        continue

    try:
        pick_rate = rows.find_all("td", class_="css-1amolq6 eyczova1")[2].text.strip()
    except:
        continue
    try:
            ban_rate = rows.find_all("td", class_="css-1amolq6 eyczova1")[3].text.strip()
    except:
        continue

    champion_info = {
        'name': champion_name,
        'win_rate': win_rate,
        'role': role,
        'pick': pick_rate,
        'ban': ban_rate
    }
    champions.append(champion_info)

df = pd.DataFrame(champions)

for champion in champions:
    print(f"Champion: {champion['name']}, Role: {champion['role']}, Win Rate: {champion['win_rate']}, Pick Rate: {champion['pick']}. Ban Rate: {champion['ban']}")

x=""

while x != 5:
    print("\nHow would you like to see champions")
    x = int(input("1. sort by name\n2. sort by winrate\n3. sort by pick rate\n4. sort by ban rate\n5. exit"))
    if x == 1:
        df_sorted_by_name = df.sort_values(by='name')
        print(df_sorted_by_name)
    elif x == 2:
        df['win_rate'] = df['win_rate'].str.rstrip('%').astype(float)
        df_sorted_by_win_rate = df.sort_values(by='win_rate', ascending=False)
        print(df_sorted_by_win_rate)
    elif x == 3:
        df['pick'] = df['pick'].str.rstrip('%').astype(float)
        df_sorted_by_pick_rate = df.sort_values(by='pick', ascending=False)
        print(df_sorted_by_pick_rate)
    elif x == 4:
        df['ban'] = df['ban'].str.rstrip('%').astype(float)
        df_sorted_by_ban_rate = df.sort_values(by='ban', ascending=False)
        print(df_sorted_by_ban_rate)
