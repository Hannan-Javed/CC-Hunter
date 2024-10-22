import bs4, os
import requests

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
                    professor = [td.get_text(";", strip=True).partition(';')[0] for td in soup.find_all("td") if "faculty" in td.get_text(strip=True).lower()]
                    faculties = [td.get_text(";", strip=True).partition(';')[2] for td in soup.find_all("td") if "faculty" in td.get_text(strip=True).lower()]
                    if len(faculties) == 0:
                        professor = [td.get_text(";", strip=True).partition(';')[0] for td in soup.find_all("td") if "centre" in td.get_text(strip=True).lower()]
                        faculties = [td.get_text(";", strip=True).partition(';')[2] for td in soup.find_all("td") if "centre" in td.get_text(strip=True).lower()]
                    data[cc] = [faculties[0], professor[0].replace(';','')]
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

def readData():
    with open("ccs.txt", "r") as file:
        data = file.read().splitlines()
    return data

def queryCCCourses(p, f):
    data = readData()
    for line in data:
        cc, courseInfo = line.split(";")
        if p.lower() in courseInfo.lower() and f.lower() in courseInfo.lower():
            print(f"{cc} - {courseInfo.replace('')}")

def main():
    if not 'ccs.txt' in os.listdir():
        print("Data not found, fetching...")
        ccsInformation = HuntCCs()
        saveData(ccsInformation)
    print("Which department's or professor's are you looking for? ")
    professors = input("Professor: ")
    faculties = input("Faculty: ")
    queryCCCourses(professors, faculties)


if __name__ == '__main__':
    main()