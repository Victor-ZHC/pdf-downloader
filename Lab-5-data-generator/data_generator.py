import json
import random

country_list = ["RMB", "USD", "JPY", "EUR"]
base_rate_table = {"RMB": 2.0, "USD": 12.0, "JPY": 0.5, "EUR": 6.0}
rate_change = 0.1

file_num = 3
data_num_per_min = 1000
total_min = 6

def generate_data(time, rate_table):
    random.seed(10)
    country_combination = [random.sample(country_list, 2) for _ in range(data_num_per_min)]
    order_second = [random.randint(0, 59) for _ in range(data_num_per_min)]
    order_value = [random.randint(100, 1000) for _ in range(data_num_per_min)]
    result_dict = {
        "RMB": {"name": "RMB","income": 0.0, "expend": 0.0, "time": time}, 
        "USD": {"name": "USD","income": 0.0, "expend": 0.0, "time": time},
        "JPY": {"name": "JPY","income": 0.0, "expend": 0.0, "time": time},
        "EUR": {"name": "EUR","income": 0.0, "expend": 0.0, "time": time}
    }

    generate_list = []
    for combination, value, second in zip(country_combination, order_value, order_second):
        data = {
            "src_name": combination[0],
            "dst_name": combination[1],
            "value": value,
            "time": time + ":" + (str(second) if second > 9 else '0' + str(second))
        }
        generate_list.append(data)
        result_dict[combination[0]]["expend"] += value
        result_dict[combination[1]]["income"] = round(result_dict[combination[1]]["income"] + round(value * rate_table[combination[0]] / rate_table[combination[1]], 2), 2)

    return generate_list, result_dict

def save_result_data(time, result_list):
    with open(time + ".json", 'wb') as result_file:
        result_file.write(json.dumps(result_list).encode('UTF-8'))
        result_file.close()      

def save_generate_data(file_name, all_generate_list):
    sorted_list = sorted(all_generate_list, key = _time)
    file_data_list = [[] for _ in range(file_num)]
    for index, data in enumerate(sorted_list):
        file_index = index % file_num
        file_data_list[file_index].append(data)

    for index, data_list in enumerate(file_data_list):
        with open(file_name + str(index) + ".json", 'wb') as test_file:
            test_file.write(json.dumps(data_list).encode('UTF-8'))
            test_file.close()

def _time(data):
    return data["time"]

if __name__ == "__main__":
    base_time = "2018-01-01 00:"
    generate_file_name = "test_data_"
    all_generate_list = []
    for i in range(total_min):
        rate_table = {k: v + rate_change * i for k, v in base_rate_table.items()}
        if i < 10:
            time = base_time + "0" + str(i)
        else:
            time = base_time + str(i)

        generate_list, result_dict = generate_data(time, rate_table)
        result_list = [v for v in result_dict.values()]
        save_result_data(time, result_list)
        all_generate_list += generate_list
    
    save_generate_data(generate_file_name, all_generate_list)