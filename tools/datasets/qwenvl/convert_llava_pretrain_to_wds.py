# Copied from https://github.com/alibaba/Pai-Megatron-Patch/blob/8949a6647cbf6b39837ad3dd911fa4aa0726895b/toolkits/multimodal_data_preprocessing/convert_llava_pretrain_to_wds.py
import json
import os
import sys

import webdataset as wds

from tqdm import tqdm


def convert(llava_pretrain_dir):

    # Paths to the dataset files
    json_file = os.path.join(llava_pretrain_dir, "blip_laion_cc_sbu_558k.json")
    output = os.path.join(llava_pretrain_dir, "wds")

    if not os.path.exists(output):
        os.mkdir(output)

    # Load data
    with open(json_file, "r") as f:
        data = json.load(f)

    with wds.ShardWriter(os.path.join(output, "pretrain-%d.tar"), maxcount=10000) as shard_writer:
        for entry in tqdm(data):
            with open(os.path.join(llava_pretrain_dir, entry["image"]), "rb") as img_file:
                image_data = img_file.read()
            sample = {
                "__key__": entry["id"],
                "jpg": image_data,
                "json": json.dumps(entry["conversations"]).encode("utf-8"),
            }
            shard_writer.write(sample)

    print(f"Dataset successfully converted to wds")


if __name__ == "__main__":
    convert(sys.argv[1])
