import requests
from bs4 import BeautifulSoup

mot = input("De quel mot voulez-vous la définition ? \n")

def infinitif_definition(word):
    vgm_url = f'https://dictionnaire.lerobert.com/conjugaison/{word}'
    retour = requests.get(vgm_url)
    if retour.status_code != 200:
        return False
    html_text = retour.text
    soup = BeautifulSoup(html_text, 'html.parser')
    infinitif = soup.find("span", class_="conj_lemme").get_text()
    return infinitif


def definition(word):
    vgm_url = f'https://dictionnaire.lerobert.com/definition/{word}'
    retour = requests.get(vgm_url)
    if retour.status_code == 200:
        html_text = retour.text
        soup = BeautifulSoup(html_text, 'html.parser')
        definitions = soup.find(id="definitions")
        divs = definitions.find_all("div", class_="b")
        for i in divs:
            print(f"\n{divs.index(i)+1} : {i.find('span', class_='d_cat').get_text().capitalize()}\n---------------------")
            resultat = i.find_all("div", class_="d_dvn")
            if len(resultat) == 0:
                resultat = i.find_all("div", class_="d_ptma")
            for j in resultat:
                s = j.get_text()
                if '\n' in s:
                    s = s[s.index('\n')+1:-1]
                if '➙\xa0' in s:
                    s = s[:s.index('➙\xa0')-1]
                if '\xa0' in s:
                    s = s.replace("\xa0", " ")
                while '\n\n' in s:
                    s = s.replace('\n\n', '\n')
                index = resultat.index(j)
                s = s[0].upper() + s[1:]
                print(f"Définition {index + 1} : {s} \n++++ \n")


    else:
        verbe = infinitif_definition(word)
        if not verbe:
            raise ValueError("Mot inconnu dans le dictionnaire Le Robert. S'il s'agit d'une forme conjuguée, il faut entrer le verbe à l'infinitif !")
        else:
            print(f"Affichage de la définition de l'infinitif {verbe}, correspondant à ce mot !\n")
            definition(verbe)
definition(mot)