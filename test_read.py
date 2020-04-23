import json
json_open = open("labelbox_data.json", "r")
json_load = json.load(json_open)

num_json_data = len(json_load)
print("num data:", num_json_data)

prj_name = json_load[0]["Project Name"]
print("project name:", prj_name)
print()

for curr_json in json_load:
    # curr_json = json_load[j_id]
    labeled_data = curr_json["Labeled Data"]
    temp_fname1 = labeled_data.rsplit(".png?")[0]
    temp_fname2 = temp_fname1.rsplit("-")[-1]
    src_fname = temp_fname2 + ".png"
    print("source file name:", src_fname)

    objects = curr_json["Label"]["objects"]
    num_objs = len(objects)
    # print(num_objs)
    for curr_obj in objects:
        print(curr_obj["line"])

    print()

# print(json_load)
