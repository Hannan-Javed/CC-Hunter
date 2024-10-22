import bs4
import requests as requests

websites = ["https://commoncore.hku.hk/science-technology-and-big-data/", "https://commoncore.hku.hk/arts-and-humanities/", "https://commoncore.hku.hk/global-issues/", "https://commoncore.hku.hk/china-culture-state-and-society/"]

def HuntCCs():

    data = {}
    for ccArea in websites:
        try:
            response = requests.get(ccArea)
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            ccs_elements = soup.find_all("h5")
            ccs = [cc.get_text(strip=True) for cc in ccs_elements][::2]
            for cc in ccs:
                try:
                    response = requests.get("https://commoncore.hku.hk/" + cc)
                    response.raise_for_status()
                    soup = bs4.BeautifulSoup(response.text, "html.parser")
                    professor = [td.get_text(";", strip=True).partition(';')[0] for td in soup.find_all("td") if "faculty" in td.get_text(strip=True).lower()][0]
                    faculties = [td.get_text(";", strip=True).partition(';')[2] for td in soup.find_all("td") if "faculty" in td.get_text(strip=True).lower()][0].replace(';', '')
                    if len(professor) == 0:
                        professor = soup.find_all(string=lambda text: "dr" in text.lower())
                        if len(professor) == 0:
                            print(f"Cannot find professor for {cc}")
                    if len(faculties) == 0:
                        faculties = soup.find_all(string=lambda text: "centre" in text.lower())
                        if len(faculties) == 0:
                            print(f"Cannot find faculty for {cc}")
                    data[cc] = [faculties, professor]
                except requests.RequestException as e:
                    print(f"Error fetching details for {cc}: {e}")
                except IndexError as e:
                    print(f"Error parsing details for {cc}: {e}")
        except requests.RequestException as e:
            print(f"Error fetching {ccArea}: {e}")
    return data
            
def saveData(data):
    with open("ccs.txt", "w") as file:
        for cc, courseInfo in data.items():
            file.write(f"{cc};{courseInfo}\n")
    print("Data saved to ccs.txt")

def main():
    ccsInformation = HuntCCs()
    saveData(ccsInformation)

if __name__ == '__main__':
    main()