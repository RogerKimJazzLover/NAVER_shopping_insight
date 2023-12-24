from tabulate import tabulate
import pandas as pd

def main():
    table = pd.read_csv("./data/test_search_ratio.csv", encoding="euc-kr")
    search_rates = table.drop(table.columns[[0,1,2,3,4,5]], axis=1)
    sum = search_rates.sum()
    x_factor = table["Monthly_num_search"] / (sum[0] / 100)
    daily_search = (search_rates / 100) * x_factor[0]
    daily_search["Keywords"] = table["Keywords"]

    new_table = table.iloc[:, [0,1,2]]
    new_table = pd.merge(left=new_table, right=daily_search, on='Keywords')
    new_table.to_csv("./data/test_daily_search.csv", encoding = "euc-kr", index=False)

if __name__ == "__main__":
  main()