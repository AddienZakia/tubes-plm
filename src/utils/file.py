import pandas as pd
import json

class Files:
    def __init__(self, path):
        self.path = path

    def read_data_csv(self, path):
        df = pd.read_csv(
            path,
            delimiter=';',      
            encoding='utf-8',   
        )

        json_data = df.to_json(orient='records', indent=2)
        json_data = json.loads(json_data)
        result = {}

        for items in json_data:
            val = [int(values) for keys, values in items.items() if keys != 'Country']

            result[items['Country']] = val
        
        self.data = result
    
    def get_recent_data(self):
        try: 
            with open(self.path, "r") as file:
                data = json.load(file)
                return data
        except:
            print("Spesific JSON file not found")

    def save_recent_data(self, date, file_name, path):
        data = []

        with open(self.path, "r") as file:
            data = json.load(file)

        data.append({
            "date": date, 
            "file": file_name, 
            "path": path
        })

        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)
