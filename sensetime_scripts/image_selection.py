import json
import argparse
import shutil
from PIL import Image
import random
import os
from tqdm import tqdm

TARGET_DISTRIBUTION = {'Sunny_DAY': 1250, 'Sunny_NIGHT': 625, 'Rainy_TWLIGHT': 625, 'Rainy_DAY': 1250,
                       'Cloudy_DAY': 625, 'Cloudy_NIGHT': 1250}

CAM = [
    'center_camera_fov30', 'center_camera_fov120', 'left_front_camera', 'left_rear_camera', 'rear_camera',
    'right_front_camera', 'right_rear_camera', 'front_camera_fov195', 'left_camera_fov195',
    'rear_camera_fov195',
    'right_camera_fov195'
]


def image_selection(args):
    json_file_path = os.path.join(args.input_folder, 'result.json')
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    os.makedirs(args.output_folder, exist_ok=True)
    # shuffle data
    random.shuffle(data)
    print(f"There are {len(data)} bundles in total")
    img_index = 0
    for i, _data in enumerate(tqdm(data)):
        if 'camera_infos' not in _data:
            continue
        if len(_data['camera_infos'][0].keys()) != 11:
            print(f"found NOT-11V bundles")
            continue
        scene_tag = _data['scene_tag']
        if scene_tag not in TARGET_DISTRIBUTION or TARGET_DISTRIBUTION[scene_tag] <= 0:
            continue
        for _bundle in _data['camera_infos']:
            for cam in CAM:
                assert cam in _bundle
                img_path = _bundle[cam]['filename']
                img_path = '/'.join(img_path.split('/')[-5:])
                image_path = os.path.join(args.input_folder, img_path)
                #resize image
                #img = Image.open(image_path)
                #img = img.resize((args.resize, args.resize))
                #save image to new path
                new_image_path = os.path.join(args.output_folder, f"{img_index:07d}_{scene_tag}.png")
                shutil.copy(image_path, new_image_path)
                #img.save(new_image_path)
                img_index += 1
                if img_index % 1000 == 0:
                    print(f"Processed {img_index} images")
            TARGET_DISTRIBUTION[scene_tag] -= 1
    print(f"Finished processing {img_index} images")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='select image for SR model')
    parser.add_argument('--input_folder', '-i', type=str, help='input folder')
    parser.add_argument('--output_folder', '-o', type=str, help='output image folder')
    parser.add_argument('--resize', default=512, type=int, help='resize image size')
    args = parser.parse_args()
    image_selection(args)
