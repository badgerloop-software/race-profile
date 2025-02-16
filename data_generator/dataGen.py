import redis, time
import pandas as pd

if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    data_dict = {}
    input_data = pd.read_csv("TestDataAnalysis\\2024-4-7rawdata.csv")
    
    for i in range(0, len(input_data)):
        row = input_data.iloc[i]
        data_dict = row.to_dict()
        r.mset(data_dict)
        print(f"Fed row {i}.")
        time.sleep(30)
        
    print("Feeding complete. Restart with \"python3 dataGen.py\"")