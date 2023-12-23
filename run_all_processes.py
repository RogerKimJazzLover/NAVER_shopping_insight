import reusable_funcs
import subprocess, os
import pandas as pd

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
    file1 = "get_keywordrank.py"
    file2 = "get_search_num.py"
    file3 = "get_search_rate.py"
    
    print("\nSYSTEM: Creating d/w/m top10 keywords csv file......")
    print('#' * 100)
    # subprocess.run(['python', file1])
    print("\nSYSTEM: Finished creating top10 keywords csv files!")

    print("\nSYSTEM: Appending search numbers to the m_top10_keywords.csv file......")
    print('#' * 100)
    # subprocess.run(['python', file2])
    print("\nSYSTEM: Finished appending search nums!")

    print("\nSYSTEM: Seperated m_top10_keywords.csv into two!")
    SeperateTable()

    print("\nSYSTEM: Appending search ratio to the first table.......")
    print('#' * 100)
    os.environ['FILE_NAME'] = "./data/m_top10_keywords_1.csv"
    os.environ['SAVE_AS'] = "./data/m_search_ratios_1.csv"
    subprocess.run(['python', file3])
    print("\nSYSTEM: Finished appending first search ratio!\n")

    #RUNS after the ok sign.
    #ALL THIS BS BECAUSE THE NAVER API CAN ONLY BE CALLED 1,000 TIMES A DAY
    #BUT WE HAVE 1,200 ITEMS! SO HAVE TO RUN AT LIKE 11:30 P.M THEN WAIT FOR THE NEXT DAY AND RUN THE REST.
    while(True):
        a = input("SYSTEM: Ready to run the second file, Sir?\n[y/n]: ")
        if a == 'y':
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
            print('-'*45, "DONE!", '-'*45)
            break
        else:
            print("\nSYSTEM: Very good sir. I'll come back in a minute.\nWaiting.......")
            reusable_funcs.DisplayTimer(60)

if __name__ == "__main__":
    main()