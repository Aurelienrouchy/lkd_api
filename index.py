from pathlib import Path
from search import Search

import json
import time


search = Search()

search.authenticate("rouchy.aurelien1@gmail.com", "Odette123")

LOCATION = "Ville de Paris, Île-de-France, France"
# SECTEUR = "Films d’animation"
SECTEUR = "all_secteurs"
SIZE = "501-1 000"

# with open("industries.txt", "r") as industrie:
#     for line in industrie:
        # SECTEUR = line.rstrip("\n")

search.start_capture()

my_file = Path(f"{LOCATION}_{SECTEUR}_{SIZE}.txt")
is_links_employes_list_file_exist = my_file.is_file()
links_employes_list = []

if is_links_employes_list_file_exist:
    with open(f"{LOCATION}_{SECTEUR}_{SIZE}.txt", "r") as text_file:
        for name in text_file:
            links_employes_list.append(name)

else:
    search.open_company_search()
    search.serch_by_location(LOCATION)
    # search.serch_by_secteur(SECTEUR)
    search.serch_by_size(SIZE)

    links_employes_list_from_lkd = search.scroll_and_go_last_page_companies()

    with open(f"{LOCATION}_{SECTEUR}_{SIZE}.txt", "a+") as text_file:
        for x in range(len(links_employes_list_from_lkd)):
            for y in range(len(links_employes_list_from_lkd[x])):
                
                text_file.write(links_employes_list_from_lkd[x][y] + "\n")
                links_employes_list.append(links_employes_list_from_lkd[x][y])


for x in range(len(links_employes_list)):
    search.open_tab(links_employes_list[x].strip(' \t\n\r'))
    search.scroll_and_go_last_page(x)


