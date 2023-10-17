import os
import json

directory = 'address'

json_data_by_state = {}

files = os.listdir(directory)

city_mapping = {}

with open('./city/cities.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        columns = line.strip().split(',')
        if len(columns) >= 2:
            city_code = columns[0]
            city_name = columns[1]
            city_mapping[city_code] = city_name

for file in files:
    if file.endswith('.csv'):
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                columns = line.strip().split(',')
                if columns[4] in ['830', '1126', '1176', '1498', '1650', '2023', '2599', '2621', '3202', '3445', 
                                  '3988', '4044', '4336', '4501', '4508', '4842', '5021', '5481', '5554', '5583',
                                  '6171', '6231', '6849', '7562', '7671', '7723', '7794', '7914', '8135', '8724',
                                  '8758', '9186', '9603', '10175']: 
                    json_obj = {
                        "postal_code": columns[0],
                        "street": columns[1],
                        "observation": columns[2],
                        "neighborhood": columns[3],
                        "city": city_mapping[columns[4]],
                        "state": 'Minas Gerais'
                    }
                    city_neighborhood = f'{json_obj["city"]}_{json_obj["neighborhood"]}'
                    if city_neighborhood in json_data_by_state:
                        json_data_by_state[city_neighborhood].append(json_obj)
                    else:
                        json_data_by_state[city_neighborhood] = [json_obj]

result_directory = 'mapping_result'

os.makedirs(result_directory, exist_ok=True)

for city_neighborhood, data in json_data_by_state.items():
    sorted_data = sorted(data, key=lambda x: x["postal_code"])
    json_filename = os.path.join(result_directory, f"{city_neighborhood}.json")
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(sorted_data, json_file, ensure_ascii=False, indent=4)
