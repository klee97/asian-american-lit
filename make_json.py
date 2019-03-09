#https://stackoverflow.com/questions/19697846/how-to-convert-csv-file-to-multiline-json
# read csv into pandas dataframe
# slice in different ways and create json


# Have a dicionary of codes...

# author/country
# for unique country, slice according to that country and count number
# output unique name, id, and count


# publication over time
# title, ethnicity of author, genre, publication date, generation of author

import pandas as pd
import csv
import json
country_dict = {"Afghanistan": "AF", "Armenia": "AM", "Azerbaijan": "AZ",
 "Bahrain": "BH", "Bangladesh": "BD", "Bhutan": "BT", "Brunei": "BN", 
 "Cambodia": "KH", "China": "CN", "Christmas Island": "CX", 
 "Cocos Islands": "CC", "Diego Garcia": "IO", "Georgia": "GE", 
 "Hong Kong": "HK", "India": "IN", "Indonesia": "ID", "Iran": "IR",
 "Iraq": "IQ", "Israel": "IL", "Japan":"JP", "Jordan": "JO", 
 "Kazakhstan": "KZ", "Kuwait": "KW", "Kyrgyzstan": "KG", "Laos": "LA", 
 "Lebanon": "LB", "Macau": "MO", "Malaysia": "MY", "Maldives": "MV",
 "Mongolia": "MN", "Myanmar": "MM", "Nepal": "NP", "North Korea": "KP",
 "Oman": "OM", "Pakistan": "PK", "Palestine": "PS", "Philippines": "PH",
 "Qatar": "QA", "Saudi Arabia": "SA", "Singapore": "SG", "South Korea": "KR",
 "Sri Lanka": "LK", "Syria": "SY", "Taiwan": "TW", "Tajikistan": "TJ",
 "Thailand": "TH", "Turkey": "TR", "Turkmenistan": "TM", 
 "United Arab Emirates": "AE", "Uzbekistan": "UZ", "Vietnam": "VN",
 "Yemen":"YE"} 
COUNTRY = 3
LASTNAME = 0
FIRSTNAME = 1
GENDER = 6
AGE_CATEGORY = 5
YEAR = 9
def make_years():

    year_dict = dict()
    print("opening json")
    jsonfile = open('timeline.json', 'w')
    print("opened json")

   # sub_dict = {"M": 0, "F": 0, "born": 0, "young adult": 0, "child": 0, "adult": 0, "first-gen": 0, "not first-gen"}
    with open("bibliography.tsv") as tsv:
        print("opened bibliography")
        reader = csv.reader(tsv, delimiter="\t")
        next(reader, None)
        for line in reader:
            print("Adding line")
            year = int(line[YEAR].rstrip())
            m_f = line[GENDER].rstrip()
            age = line[AGE_CATEGORY].rstrip()
            if year not in year_dict:
                year_dict[year] = {"publications": 0, "M": 0, "F": 0, "born": 0, "young adult": 0, "child": 0, "adult": 0, "first-gen": 0}
            year_dict[year][m_f] += 1
            year_dict[year]["publications"] += 1
            if age == "born":
                year_dict[year]["born"] += 1
            else:
                year_dict[year]["first-gen"] += 1
                if age in ["young adult", "child", "adult"]:
                    year_dict[year][age] += 1
    jsonfile.write("[")
    first = 1        
    for year, val in sorted(year_dict.items()):
        val["year"] = str(year)
        if first:
            jsonfile.write(json.dumps(val) + '\n')
            first = 0
        else:
            jsonfile.write(","+ json.dumps(val) + '\n')
    jsonfile.write("]")
    jsonfile.close()


def get_countries():

    countries = dict()
    jsonfile = open('countries.json', 'w')
    authors = set()
    with open("bibliography.tsv") as tsv:
        reader = csv.reader(tsv, delimiter="\t")
        next(reader, None)
        for line in reader:
            name = line[FIRSTNAME].rstrip() + " " + line[LASTNAME].rstrip()
            gender = line[GENDER].rstrip()
            if name in authors:
                continue
            country_list = [x.strip() for x in line[COUNTRY].split(',')]
            for country in country_list:
                if country == "Korea":
                    country = "South Korea"

                if country not in countries:
                    countries[country] = {"value": 0, "id":country_dict[country], "M": 0, "F": 0}
                countries[country]["value"] +=1
                countries[country][gender] += 1

                authors.add(name)

    jsonfile.write("[")
    first = 1
    for country, val in sorted(countries.items()):
        val["country"] = country
        if first:
            jsonfile.write(json.dumps(val) + '\n')
            first = 0
        else:
            jsonfile.write(","+ json.dumps(val) + '\n')


    jsonfile.write("]")
    jsonfile.close()
def make_countries():
    csvfile = open('countries.csv', 'r')
    jsonfile = open('countries.json', 'w')

    fieldnames = ("country","value")
    reader = csv.DictReader(csvfile, fieldnames)


    country_set = set()
    for row in reader:
        print(row)
        row["id"] = country_dict[row["country"]]
        row["value"] = int(row["value"])
        row["fill_value"] =  row["value"]
        country_set.add(row["country"])
        json.dump(row, jsonfile)
        jsonfile.write(',\n')

    for country in country_dict.keys():
        if country not in country_set:
            new_row = '''{"country": "'''+ country + '''", "value": 0, "fill_value": 0, "id": "''' + country_dict[country] + '''"},\n'''
            jsonfile.write(new_row)

    csvfile.close()
    jsonfile.close()
if __name__ == '__main__':
    make_years()
    get_countries()
