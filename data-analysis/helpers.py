import json
import pickle

def load_dict_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_dict_to_json(data,file_path):
    with open(file_path, 'w') as file:
        json.dump(data,file,indent=4)

def load_container_from_pickle(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

def save_container_to_pickle(data, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

def load_and_append_to_pickle(data, file_path):
    loaded_data = load_container_from_pickle(file_path)
    loaded_data.append(data)
    save_container_to_pickle(loaded_data, file_path)

def load_and_append_to_pickle_and_remove_duplicates(data, file_path):
    loaded_data = load_container_from_pickle(file_path)
    loaded_data.extend(data)
    loaded_data = list(set(loaded_data))
    save_container_to_pickle(loaded_data, file_path)

def format_date(date_text): # converts date to format yyyy-mm-dd
    try:
        date = datetime.strptime(date_text, "%d %b, %Y")
        date_formatted = date.strftime('%Y-%m-%d')
        return date_formatted
    except ValueError:
        return "Erro ao converter a data de lançamento."

def read_and_append_to_json(new_data,file_path):

    file = open(file_path, 'r')
    data = json.load(file)
    file.close()

    data.update(new_data)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_number_keys(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
        
        # Extract number keys
        number_keys = [key for key in data.keys() if key.isdigit()]
        
        return number_keys

def split(lst, n):
    k, m = divmod(len(lst), n)
    for i in range(n):
        yield lst[i*k+min(i, m):(i+1)*k+min(i+1, m)]

def list_subtraction(list1,list2):
    return [item for item in list1 if item not in list2]

def findkeys(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, kv):
                yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findkeys(j, kv):
                yield x

def findIntKeys(node):
    if isinstance(node, list):
        for i in node:
            for x in findIntKeys(i):
                yield x
    elif isinstance(node, dict):
        for j in node.keys():
            if j.isdigit():
                yield j
            for x in findIntKeys(node[j]):
                yield x
