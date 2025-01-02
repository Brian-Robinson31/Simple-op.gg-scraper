from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def get_tier_list():
    url = "https://www.op.gg/champions"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features="html.parser")

    champion_rows = soup.find_all("tr")
    champions = []

    for rows in champion_rows:
        all_counters = []
        champion_name_tag = rows.find("strong")
        if champion_name_tag:
            champion_name = champion_name_tag.get_text(strip=True)
        else:
            champion_name = None
        role = extract_role(rows)

        counters = rows.find_all("td", class_="css-1gnhxc7 eq1151q6")
        for counter in counters:
            all_counters += extract_counters(counter)

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
            'ban': ban_rate,
            'counters': all_counters
        }
        champions.append(champion_info)
    
    return champions
def extract_role(rows):
    # Function to extract role information
    Role_test = str(rows.find("td", class_="css-1amolq6 eyczova1"))
    start_index = Role_test.find('alt="') + len('alt="')
    end_index = Role_test.find('"', start_index)
    role = Role_test[start_index:end_index]
    return role

def extract_counters(counter):
    # Function to extract counters
    alt_positions = [m.start() for m in re.finditer('alt="', str(counter))]
    all_counters = []
    for start_index in alt_positions:
        end_index = str(counter).find('"', start_index + len('alt="'))
        counter_final = str(counter)[start_index + len('alt="'):end_index]
        all_counters.append(counter_final)
    return all_counters

# API route to serve the champion data as JSON
@app.route('/api/tierlist', methods=['GET'])
def champion_tierlist():
    data = get_tier_list()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
