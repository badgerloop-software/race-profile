"""
Tool I write to convert the scuffed .txt file into a csv for easy access.
"""

def convert(file_path):
    try:
        rowList = []
        with open(file_path, 'r') as file:
            for row in file:
                if not row.strip():
                    continue
                rowList.append(row.split())
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
    except Exception as e:
        print(f"Error occurred: {e}")

    with open('solar_car_telemetry/src/solcast/repaired.csv', "w") as file:
        for i in range(len(rowList)):
            file.write(f"{rowList[i][0]},{rowList[i][1]},{rowList[i][2]},{rowList[i][3]},{rowList[i][4]},{rowList[i][5]},{rowList[i][5]},{rowList[i][6]}\n")


if __name__ == '__main__':
    convert("solar_car_telemetry/src/solcast/ASC2022_FullRoute.txt")