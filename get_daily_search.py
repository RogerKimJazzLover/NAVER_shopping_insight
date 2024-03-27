from tabulate import tabulate
import pandas as pd

def round_to_int(daily_search: pd.DataFrame):
    for index, row in daily_search.iterrows():
        try:
            daily_search.loc[index] = row.round().astype(int)
        except:
            for i in range(30):
                try:
                    row.iloc[i] = round(row.iloc[i], 0)
                except:
                    row.iloc[i] = row.iloc[i]
            continue

def main():
    table = pd.read_csv("./data/m_search_ratios.csv", encoding="euc-kr")
    search_rates = table.drop(table.columns[[0,1,2,3,4,5]], axis=1)
    sum = search_rates.sum(axis=1)
    x_factor = table["Monthly_num_search"] / (sum[0] / 100)
    daily_search = search_rates.mul(x_factor, axis="index") / 100
    round_to_int(daily_search)

    new_table = table.iloc[:, [0,1,2,3,5]]
    new_table = pd.merge(left=new_table, right=daily_search, left_index=True, right_index=True)
    new_table = new_table.drop_duplicates(subset='Keywords')
    new_table.to_csv("./data/m_daily_search.csv", encoding = "euc-kr", index=False)

if __name__ == "__main__":
  main()