import argparse

import toml

import json
from moviepy.video.io.VideoFileClip import VideoFileClip

from .dataset.lavdf import LAVDFDataModule, Metadata
from .inference import inference_batfd
from .model import BATFD
from .post_process import post_process
from .utils import read_json

# parser = argparse.ArgumentParser(description="BATFD evaluation")
# parser.add_argument("--config", type=str)
# parser.add_argument("--data_root", type=str)
# parser.add_argument("--checkpoint", type=str)
# parser.add_argument("--gpus", type=int, default=1)

def evaluate():
    # args = parser.parse_args()
    args = {"config": "./config/default.toml",
            "data_root": "./videos/",
            "gpus": 1,
            "checkpoint": "./weights/baftd_default.ckpt"}
    config = toml.load(args.config)
    model_name = config["name"]
    alpha = config["soft_nms"]["alpha"]
    t1 = config["soft_nms"]["t1"]
    t2 = config["soft_nms"]["t2"]
    
    # Change the duration in a json file that has been loaded
    with open("../videos/metadata.min.json", "r") as file:
        data = json.load(file)
        
    # print(data)
        
    video_path = "../videos/file.mp4"
    videoclip = VideoFileClip(video_path)
    durn = videoclip.duration
    
    data[0]["duration"] = durn
    
    with open('../videos/metadata.min.json', 'w') as f:
        json.dump(data, f)

    # prepare dataset
    dm = LAVDFDataModule(root=args.data_root,
        frame_padding=config["num_frames"],
        max_duration=config["max_duration"],
        batch_size=2, num_workers=3,
        get_meta_attr=BATFD.get_meta_attr)
    dm.setup()

    # prepare model
    model = BATFD.load_from_checkpoint(args.checkpoint)

    inference_batfd(model_name, model, dm, config["max_duration"], args.gpus)

    metadata = dm.test_dataset.metadata
    post_process(model_name, metadata, 25, alpha, t1, t2)
    proposals = read_json(f"../outputs/{model_name}.json")
    return proposals