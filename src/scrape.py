from bs4 import BeautifulSoup
import requests, re, json, os

# recipe categories
categories = [
62,
2282,
1,
4,
64,
74,
94,
99,
108,
]

categoryPath = "https://www.dk-kogebogen.dk/opskrifter/retter-3.php?id=%d&limit=%d&order=karakter-antal"
recipePath = "https://www.dk-kogebogen.dk/opskrifter/%d/"
nutritionalPath = "https://www.dk-kogebogen.dk/opskrifter/naeringsberegning.php?id=%d"
#page limit to recipes per categories
limit = 2

#get recipe data from a recipe ID
#this requires 2 requests to get cooking instructions.
'''returns dictionary with {
    title = ""
    instructions = ""
    ingredients = []
    nutrients = {
        kcalTotal
        kcal
        protein
        fat
        carbohydrates
    }
}
'''
def getRecipeInfo(id):
    info = {}
    info["id"] = id
    html_doc = requests.get(recipePath % id).text
    soup = BeautifulSoup(html_doc,'html.parser')
    info["title"] = soup.h1.center.text.strip() #title is found at first occurance h1 in center tags with spaces on both sides.
    info["instructions"] = soup.find("p").text #first p tag is the instructions
    ingredients = []
    ingrtable = soup.find("table",cellpadding="3") #first table with cellpadding=3
    #ingredients are seperated by trs
    for trEntry in ingrtable.find_all("tr"):
        ingr = {}
        tds = trEntry.find_all("td")
        if tds[0].text == "":
            continue
        ingr["amount"] = tds[0].text
        ingr["unit"] = tds[1].text
        ingr["name"] = tds[2].span.text #ingredient is in a span tag
        ingredients.append(ingr)

    info["ingredient"] = ingredients

    # find nutrional information
    html_doc = requests.get(nutritionalPath % id).text
    soup = BeautifulSoup(html_doc,'html.parser')
    nutrients = {}
    regex = "KJ total (.*) \((.*) kcal\)"
    totalEnergy = soup.find(text=re.compile(regex))
    nutrients["Totalkcal"] = re.search(regex,totalEnergy)[2]
    #the lines below are very long. It finds the span containing string num gram and deals with it with regex
    nutrients["kcal"] = re.search("(.*) kcal", soup.find("span", itemprop="calories").text)[1]
    nutrients["protein"] = re.search("Protein (.*) gram", soup.find("span", itemprop="proteinContent").text)[1]
    nutrients["fat"] = re.search("Fedt (.*) gram", soup.find("span", itemprop="fatContent").text)[1]
    nutrients["carbohydrates"] = re.search("Kulhydrat  (.*) gram", soup.find("span", itemprop="carbohydrateContent").text)[1] #2 spaces after Kulhydrat

    info["nutrients"] = nutrients
    return info

def isProcessed(id):
    if id + ".json" in os.listdir("data"):
        return True
    return False

def dumpJSON(recipe,id):
    f = open("data/" + id + ".json","w+")
    f.write(json.dumps(recipe))
    f.close()

# proccess each category
def processCategories(categories):
    #for each of the categories
    recipes = []
    for category in categories:
        for i in range(limit): #search through up to 'limit' pages

            #get the soup from the page
            html_doc = requests.get(categoryPath % (category, i*100)).text
            soup = BeautifulSoup(html_doc,'html.parser')

            #soup contains list of recipes, we find the ones with nutritional info
            for img in soup.find_all(src="/Naeringsberegning/naeringsberegning.gif"):
                href = img.next_element.next_element.find("a").get("href") # get the href which is 2 elements away
                id = re.search("/opskrifter/(.*)/",href)[1] #get 1st capture group containing ID
                if not isProcessed(id):
                    recipe = getRecipeInfo(int(id))
                    print("Retrieved recipe %s" % id)
                    dumpJSON(recipe,id)

if __name__ == '__main__':
    processCategories(categories)
