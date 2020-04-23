import json
import numpy as np
# json_open = open("labelbox_data.json", "r")
json_open = open("clips_001.json", "r")
json_load = json.load(json_open)

num_json_data = len(json_load)
print("num data:", num_json_data)

prj_name = json_load[0]["Project Name"]
print("project name:", prj_name)

fy_all = []

## for offset
dw = 0.5
dh = 0.5

for index, curr_json in enumerate(json_load):
    if ("objects" in curr_json["Label"]) == False:
        continue

    # print("ID:", index)
    src_fname = curr_json["External ID"]
    ds_name = curr_json["Dataset Name"]
    # print("source file name:", src_fname)

    ## parse annotational lines in current image. ##
    objects = curr_json["Label"]["objects"]
    num_objs = len(objects)

    fy_objs = list(range(num_objs))

    for obj_id, curr_obj in enumerate(objects):
        curr_lines = curr_obj["line"]

        num_pts = len(curr_lines)

        fy = list(range(num_pts - 1))
        before_point = None
        for point_id, curr_point in enumerate(curr_lines):
            curr_x = float(curr_point["x"]) + dw
            curr_y = float(curr_point["y"]) + dh
            # msg = "pt[{0:d}]:(x, y) = ({1:f}, {2:f})".format(point_id, x, y)
            # print(msg)

            if (before_point != None):
                ## create x = f(y)
                bf_x = float(before_point["x"]) + dw
                bf_y = float(before_point["y"]) + dh

                pt_x = np.array([bf_x, curr_x])
                pt_y = np.array([bf_y, curr_y])

                k = np.polyfit(pt_y, pt_x, 1)
                curr_fy = np.poly1d(k)
                # print(curr_fy(0.0))
                
                ## [x = f(y)], [y_i-1, y_i]
                fy[point_id - 1] = (curr_fy, (bf_y, curr_y))

            before_point = curr_point

        fy_objs[obj_id] = fy

    clips_root_dir = prj_name.split("_", 1)[-1]
    clips_data_dir = ds_name.rsplit("_", 1)[-1]
    # src_path = prj_name + "/" + ds_name + "/" + src_fname
    src_path = clips_root_dir + "/" + clips_data_dir + "/" + src_fname
    fy_all.append((src_path, fy_objs))

num_imgs = len(fy_all)
print(num_imgs)

## prepare to write json for lanenet.
out_json_str = ""

## y-data for input 
s_y = 200
e_y = 720
h_samples = np.arange(s_y, e_y, 10)

for fname, fy_objs in fy_all:
    curr_dict = {}
    lines_list = []
    for fy_polylines in fy_objs:
        w_samples = np.full(h_samples.shape[0], -2)
        # print(fy_polylines)
        for curr_fy, range_y in fy_polylines:
    #         msg = "[{0:d}][{1:d}][{2:d}]".format(im_id, -1, f_id)
    #         # print(msg)
            # print(curr_fy)
            # print(range_y)
            curr_range = (range_y[0] < h_samples) & (h_samples <= range_y[1])
            curr_h_samples = h_samples[curr_range]
            w_samples[curr_range] = curr_fy(curr_h_samples)
            # print(curr_h_samples)

        ## TODO: 1280 で頭打ち
        # print(h_samples)
        # print(np.round(w_samples))
        # print()
        lines_list.append(np.round(w_samples).tolist())
    
    curr_dict["lines"] = lines_list
    curr_dict["h_samples"] = h_samples.tolist()
    curr_dict["raw_file"] = fname

    out_json_str = out_json_str + "\n" + str(json.dumps(curr_dict))

## prepare to write json for lanenet.
with open("./label_data_test.json", "w") as out_file:
    out_file.write(out_json_str[1:])
#    json.dump(out_dict, out_file, indent=2)
