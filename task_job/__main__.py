import pandas as pd

def one_million_data():
    csv_file = pd.read_csv("resources/task.csv", sep="\t", nrows=1000000)
    #one_million_data = csv_file.head(1000000)
    return csv_file


def duplicated_data()-> list[int]:
    data = one_million_data()
    duplicated = data[data.duplicated(subset=["<DATE>", "<TIME>"], keep=False)]
    duplicated_with_Nan = duplicated[(duplicated['<BID>'].isna()) | (duplicated['<ASK>'].isna())]
    list_of_duplicated_of_Nan = duplicated_with_Nan.index.to_list()

    return list_of_duplicated_of_Nan

def delete_duplicated_data():
    data = one_million_data()
    list_data_to_delete = duplicated_data()
    leaked_data = data.drop(index=list_data_to_delete)
    return leaked_data

def create_new_column():
    leaked_data = delete_duplicated_data()
    leaked_data["<ASK>"] = leaked_data["<ASK>"].fillna(0)
    leaked_data["<BID>"] = leaked_data["<BID>"].fillna(0)
    leaked_data["<SPREAD>"] = leaked_data["<ASK>"] - leaked_data["<BID>"]
    
    return leaked_data

    



if __name__ == "__main__":
   data = create_new_column()
   print(data)
