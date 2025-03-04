import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time

# Λίστα με URLs των αγώνων
match_urls = [
    "https://www.flashscore.gr/",
    "https://www.livescore.com/en/",
    "https://www.sofascore.com/"
]

def fetch_match_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:  # Ελέγχουμε αν η σελίδα φορτώθηκε σωστά
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Εξαγωγή στατιστικών
            home_xG = soup.find("div", {"class": "home-xg"})
            away_xG = soup.find("div", {"class": "away-xg"})
            home_shots = soup.find("span", {"class": "home-shots"})
            away_shots = soup.find("span", {"class": "away-shots"})
            
            # Αν τα δεδομένα δεν υπάρχουν, αποφεύγουμε τα σφάλματα
            if home_xG and away_xG and home_shots and away_shots:
                home_xG = home_xG.text.strip()
                away_xG = away_xG.text.strip()
                home_shots = home_shots.text.strip()
                away_shots = away_shots.text.strip()
                
                # Δημιουργία DataFrame
                match_data = {
                    "Home xG": [home_xG],
                    "Away xG": [away_xG],
                    "Home Shots": [home_shots],
                    "Away Shots": [away_shots],
                    "URL": [url]
                }
                df = pd.DataFrame(match_data)

                # Αποθήκευση δεδομένων σε CSV
                df.to_csv("match_stats.csv", mode='a', header=False, index=False)
                print(f"Δεδομένα αποθηκεύτηκαν για τον αγώνα: {url}")
            else:
                print(f"Δεδομένα λείπουν για τον αγώνα: {url}")
        else:
            print(f"Σφάλμα φόρτωσης της σελίδας {url} (status code: {response.status_code})")
    except Exception as e:
        print(f"Σφάλμα κατά την εξαγωγή δεδομένων από την {url}: {e}")

def scrape_matches():
    for url in match_urls:
        fetch_match_data(url)

# Ορισμός του χρονοδιαγράμματος (π.χ., κάθε μέρα στις 18:00)
schedule.every().day.at("18:00").do(scrape_matches)

# Εκτέλεση του προγραμματισμένου scraping
while True:
    schedule.run_pending()
    time.sleep(60)  # Κοιμάται για 60 δευτερόλεπτα πριν ξαναελέγξει αν πρέπει να εκτελέσει κάποιο task
