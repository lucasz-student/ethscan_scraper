from selenium import webdriver
import csv
from datetime import datetime
from itertools import zip_longest

# organizess list and chunks into lists of n value
def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def gather_data(page_nbr):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)

    # gets ethscan page
    driver.get("https://etherscan.io/txs?ps=100&p=" + str(page_nbr))

    # while loop to continuouslyscrape
    while True:
        # gets and comprhends lists of lists of  webelement text
        trs = [[x.text for i, x in enumerate(row) if i in [1, 2, 5, 8, 10]]for row in [list(i) for i in grouper((driver.find_elements_by_tag_name("td")), 12)]]
        
        #appends time to list
        trs.append([datetime.now()])

        # opens the current csv and appends the data to a list
        current_csv = []
        with open("t2.csv", "r", encoding="utf-8") as file:
            reader = iter(csv.reader(file))
            for row in reader:
                if row != []:
                    current_csv.append(row[0])
            file.close()

        # identifies the unscraped data
        new_data = []
        for row in trs: 
            if row[0] not in current_csv:
                new_data.append(row)

        #appends new data
        with open("t2.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(new_data)

        print("added new data")
        # refreshes page for new data
        driver.refresh()

gather_data(1)

