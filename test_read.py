import json
import numpy as np
# json_open = open("labelbox_data.json", "r")
json_open = open("clips_001.json", "r")
json_load = json.load(json_open)

num_json_data = len(json_load)
print("num data:", num_json_data)

prj_name = json_load[0]["Project Name"]
print("project name:", prj_name)
print()

# fy_all = list(range(num_pts - 1))
fy_all = list(range(num_json_data))

for index, curr_json in enumerate(json_load):
    if ("objects" in curr_json["Label"]) == False:
        continue

    print("ID:", index)
    
    # curr_json = json_load[j_id]
    labeled_data = curr_json["Labeled Data"]
    temp_fname1 = labeled_data.rsplit(".png?")[0]
    temp_fname2 = temp_fname1.rsplit("-")[-1]
    src_fname = temp_fname2 + ".png"
    print("source file name:", src_fname)

    ## parse annotational lines in current image. ##
    objects = curr_json["Label"]["objects"]
    num_objs = len(objects)
    print("num objects:", num_objs)

    fy_objs = list(range(num_objs))
    fy_all[index] = (fy_objs)

    for obj_id, curr_obj in enumerate(objects):
        curr_lines = curr_obj["line"]
        print("line no.", obj_id)

        num_pts = len(curr_lines)
        fy = list(range(num_pts - 1))
        before_point = None
        for point_id, curr_point in enumerate(curr_lines):
            x = curr_point["x"]
            y = curr_point["y"]
            msg = "pt[{0:d}]:(x, y) = ({1:f}, {2:f})".format(point_id, x, y)
            print(msg)

            if (before_point != None):
                ## create x = f(y)
                bf_x = before_point["x"]
                bf_y = before_point["y"]

                pt_x = np.array([bf_x, x])
                pt_y = np.array([bf_y, y])

                k = np.polyfit(pt_y, pt_x, 1)
                curr_fy = np.poly1d(k)
                # print(curr_fy(0.0))
                
                ## [x = f(y)], [y_i-1, y_i]
                fy[point_id - 1] = (curr_fy, (bf_y, y))

            before_point = curr_point

        fy_all[index][obj_id] = fy
        # print(fy_all[index][obj_id][0])

    print()

# print(json_load)
