
import requests
from bs4 import BeautifulSoup
import csv

def is_valid_date(date_str):
    date_parts = date_str.split("/")
    if len(date_parts) != 3:
        return False
    try:
        month, day, year = map(int, date_parts)
    except ValueError:
        return False
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    if year < 2024 or year > 2025:
        return False
    return True

def get_valid_date():
    while True:
        date_str = input("Please enter a date (MM/DD/YYYY): ")
        if is_valid_date(date_str):
            return date_str
        else:
            print("Invalid date format. Please enter the date in MM/DD/YYYY format. \nAnd make sure that it is for this year. :)")

def get_match_info(champs_title, match_cards):
    matches_details = []
    for match in match_cards:
        team_a = match.find("div", {"class": "teamA"}).find("p").text.strip()
        team_b = match.find("div", {"class": "teamB"}).find("p").text.strip()
        match_result = match.find("div", {"class": "MResult"}).find_all("span", {"class": "score"})
        score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"
        match_time = match.find("div", {"class": "MResult"}).find("span", {"class": "time"}).text.strip()
        matches_details.append({
            "نوع البطوله": champs_title,
            "الفريق الأول": team_a,
            "الفريق الثاني": team_b,
            "ميعاد المباره": match_time,
            "المنتيجه": score
        })
    return matches_details

def main():
    date = get_valid_date()
    page = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}")
    src = page.content
    soup = BeautifulSoup(src, 'lxml')
    
    matches_details = []
    match_container = soup.find("section", {"class": "mtchCntrContainer"})
    
    if match_container:
        champs = match_container.find_all("div", {"class": "matchCard"})
        for champ in champs:
            champs_title = champ.find("h2").text.strip()
            match_cards = champ.find_all("div", {"class": "liItem"})
            matches_details.extend(get_match_info(champs_title, match_cards))
    else:
        print("No match container found. Please check the date or the website structure.")
        return
    
    if matches_details:
        file_path = input("Kindly enter the full file path: ")
        keys = matches_details[0].keys()
        with open(f"{file_path}matches_details.csv", "w", encoding="utf-8", newline="") as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(matches_details)
            print("Done ya man")
    else:
        print("No match details found for the given date.")

main()
