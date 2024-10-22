import bs4
import requests as requests

websites = ["https://commoncore.hku.hk/science-technology-and-big-data/", "https://commoncore.hku.hk/arts-and-humanities/", "https://commoncore.hku.hk/global-issues/", "https://commoncore.hku.hk/china-culture-state-and-society/"]

def HuntCCs():

    for ccArea in websites:
        response = requests.get(ccArea)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        ccs_elements = soup.find_all("h5")
        ccs = [cc.get_text(strip=True) for cc in ccs_elements][::2]
        for cc in ccs:
            response = requests.get("https://commoncore.hku.hk/"+cc)
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            faculties = soup.find_all(string=lambda text: "faculty" in text.lower())[0]
            faculties = faculties.replace("(", "").replace(")", "").replace("\n", "")
            print(faculties)


def main():
    ccs = HuntCCs()
    print(ccs)
if __name__ == '__main__':
    main()