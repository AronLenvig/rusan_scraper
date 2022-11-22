import os
import json
import get_resps
import pandas as pd


def make_url(nr):
    return f"https://rusan.fo/Umbraco/Api/JsonApi/ShopSearchItemsIsotope?argCustomerNo=&argCategoryCode=&argSearchWord={nr}&argDessertir=false&argFiskur=false&argFlogfenadur=false&argFordrykkir=false&argKalvakjot=false&argLambskjot=false&argNeytakjot=false&argOstur=false&argSkeljadjor=false&argSvinakjot=false&argVillinidjor=false&argPriceFrom=0&argPriceTo=500&argVoruOki="

def create_starter_numbers()->list:
    return [f"{i:02d}-" for i in range(0, 100)]

def add_0_9_to_nr(nr) -> list:
    return [f"{nr}{i}" for i in range(0, 10)]

def add_to_json(data):
    with open("resps.json", "r") as f:
        resps = json.load(f)
    resps.update(data)
    with open("resps.json", "w") as f:
        json.dump(resps, f)

def main():
    df = pd.DataFrame()
    starter_numbers = create_starter_numbers()
    starter_urls = [make_url(nr) for nr in starter_numbers]
    pool = get_resps.get(starter_urls, starter_numbers)

    numbers = []
    urls = []
    try:
        while True:
            for resp, nr in pool:
                if len(resp) <= 0:
                    print(f"Found no results for {nr}")
                    continue
                if len(resp) >= 50:
                    print(f"creating more iteration for {nr}")
                    numbers.extend(add_0_9_to_nr(nr))
                    continue
                df = df.append(resp, ignore_index=True)
            if len(numbers) == 0:
                break
            urls.extend([make_url(nr) for nr in numbers])
            pool = get_resps.get(urls, numbers)
            numbers.clear()
            urls.clear()
    except Exception as e:
        print(e)
    finally:
        df.to_excel("rusan_data.xlsx", index=False)
        print("Done")

        
if __name__ == "__main__":
    main()