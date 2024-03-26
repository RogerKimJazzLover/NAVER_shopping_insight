from datetime import datetime, timedelta
from tqdm import trange
import subprocess, os
import pandas as pd
import time

def SeperateTable():
    table = pd.read_csv("./data/m_top10_keywords.csv", encoding="euc-kr")
    table_1 = table.head(3000)
    table_2 = table.tail(3000)

    table_1.to_csv("./data/m_top10_keywords_1.csv", encoding="euc-kr", index=False)
    table_2.to_csv("./data/m_top10_keywords_2.csv", encoding="euc-kr", index=False)

def CombineTable():
    table1 = pd.read_csv("./data/m_search_ratios_1.csv", encoding="euc-kr")
    table2 = pd.read_csv("./data/m_search_ratios_2.csv", encoding="euc-kr")

    table1 = pd.concat([table1, table2], ignore_index=True)
    table1.to_csv("./data/m_search_ratios.csv", encoding="euc-kr", index=False)

def main():
    today = datetime.today()
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=5, microsecond=0)
    start_date = today.date()

    file1 = "get_keywordrank.py"
    file2 = "get_search_num.py"
    file3 = "get_search_rate.py"
    file4 = "get_daily_search.py"
    
    #1. GETTING THE TOP 500 KEYWORDS FOR EACH CATEGORIES FOR D/W/M
    print("\nSYSTEM: Creating d/w/m top10 keywords csv file......")
    print('#' * 100)
    subprocess.run(['python', file1])
    print("\nSYSTEM: Finished creating top10 keywords csv files!")

    #2. GETTING THE SEARCH NUMS
    print("\nSYSTEM: Appending search numbers to the m_top10_keywords.csv file......")
    print('#' * 100)
    subprocess.run(['python', file2])
    print("\nSYSTEM: Finished appending search nums!")

    #3. SEPERATE THE 'm_top10_keywords.csv' INTO TWO BECAUSE THE NAVER API CAN ONLY BE CALLED 1,000 TIMES A DAY
    #   BUT WE HAVE 1,200 ITEMS! SO HAVE TO RUN AT LIKE 11:30 P.M THEN WAIT FOR THE NEXT DAY AND RUN THE REST.
    print("\nSYSTEM: Seperated m_top10_keywords.csv into two!")
    SeperateTable()

    #4. GETTING THE SEARCH RATE FOR THE FIRST HALF OF THE TABLE
    print("\nSYSTEM: Appending search ratio to the first table.......")
    print('#' * 100)
    os.environ['FILE_NAME'] = "./data/m_top10_keywords_1.csv"
    os.environ['SAVE_AS'] = "./data/m_search_ratios_1.csv"
    subprocess.run(['python', file3])
    print("\nSYSTEM: Finished appending first search ratio!\n")

    #5. GETTING THE SEARCH RATE FOR THE SECOND HALF OF THE TABLE
    while(True):
        #RUNS AFTER THE CONFIRMATION FROM THE USER
        #MAKE SURE IT IS RAN ON ANOTHER DAY!
        current_date = datetime.today().date()
        day_passed = (start_date != current_date)
        if day_passed:
            os.environ['FILE_NAME'] = "./data/m_top10_keywords_2.csv"
            os.environ['SAVE_AS'] = "./data/m_search_ratios_2.csv"

            print("\nSYSTEM: Appending search ratio to the second table......")
            print('#' * 100)
            subprocess.run(['python', file3])
            print("\nSYSTEM: Finished appending second search ratio!\n")

            CombineTable()
            os.remove("./data/m_top10_keywords_1.csv")
            print("\nSYSTEM: deleted './data/m_top10_keywords_1.csv'")
            os.remove("./data/m_top10_keywords_2.csv")
            print("\nSYSTEM: deleted './data/m_top10_keywords_2.csv'")

            os.remove("./data/m_search_ratios_1.csv")
            print("\nSYSTEM: deleted './data/m_search_ratios_1.csv'")
            os.remove("./data/m_search_ratios_2.csv")
            print("\nSYSTEM: deleted './data/m_search_ratios_2.csv'")
            break
        else:
            time_til_tmr = (tomorrow - datetime.now()).total_seconds()
            print(f"\nSYSTEM: Time left until tommorrow {time_til_tmr} seconds. Proceed to continue after {time_til_tmr} seconds")
            for _ in trange(int(time_til_tmr), desc="대기 중", unit="sec"):
                time.sleep(1)
            continue

    #6. Calculating the daily search for each keywords for the past month
    print("\nSYSTEM: m_daily_search csv file......")
    print('#' * 100)
    subprocess.run(['python', file4])
    print("\nSYSTEM: Finished creating top10 keywords csv files!")
    print('-'*50, "DONE!", '-'*50)

if __name__ == "__main__":
    main()