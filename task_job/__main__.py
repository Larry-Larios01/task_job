import pandas as pd

def one_million_data():
    csv_file = pd.read_csv("resources/task.csv", sep="\t")
    one_million_data = csv_file.head(1000000)
    return one_million_data


def duplicated_data()-> list[int]:
    data = one_million_data()
    duplicated = data[data.duplicated(subset=["<DATE>", "<TIME>"], keep=False)]

    return duplicated

if __name__ == "__main__":
    # Código a ejecutar solo si este archivo se ejecuta directamente
    csv_file = duplicated_data()
    print(csv_file)