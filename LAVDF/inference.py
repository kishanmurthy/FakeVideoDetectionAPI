# import json
# import os.path
# from pathlib import Path
# from typing import Any, List

# import numpy as np
# import pandas as pd
# from pytorch_lightning import LightningModule, Trainer, Callback

# # from dataset.lavdf import LAVDF, Metadata
# # from utils import read_video, padding_video, padding_audio, resize_video

# from dataset import LAVDFDataModule
# from dataset.lavdf import Metadata

# class SaveToJsonCallback(Callback):
#     def __init__(self, max_duration: int, metadata: List[Metadata], model_name: str):
#     # def __init__(self, max_duration: int, model_name: str):
#         super().__init__()
#         self.max_duration = max_duration
#         self.metadata = metadata
#         self.model_name = model_name
#         self.results = {}

#     def on_predict_batch_end(
#         self,
#         trainer: Trainer,
#         pl_module: LightningModule,
#         outputs: Any,
#         batch: Any,
#         batch_idx: int,
#         dataloader_idx: int,
#     ) -> None:
#         fusion_bm_map = outputs[0].cpu().numpy()[0]
#         v_bm_map = outputs[1].cpu().numpy()[0]
#         a_bm_map = outputs[2].cpu().numpy()[0]
        
#         frames = batch[3][0]
#         video_name = batch[4][0]
#         video_name = self.metadata[batch_idx].file

#         # for each boundary proposal in boundary map
#         new_props = []
#         for i in range(frames):
#             for j in range(1, self.max_duration):
#                 # begin frame and end frame
#                 begin = i
#                 end = i + j
#                 if end <= frames:
#                     new_props.append([begin, end, 
#                                       fusion_bm_map[j, i]])
#                     # , 
#                     #                   v_bm_map[j, i],
#                     #                   a_bm_map[j, i]]
#                     # new_props.append({"begin": int(begin),
#                     #                   "end": int(end),
#                     #                   "A/V Score": float(fusion_bm_map[j, i]),
#                     #                   "V Score": float(v_bm_map[j, i]),
#                     #                   "A Score": float(a_bm_map[j, i])})
                    
#         new_props = np.stack(new_props)
#         col_name = ["begin", "end", "score"]
#         new_df = pd.DataFrame(new_props, columns=col_name)
#         new_df["begin"] = new_df["begin"].astype(int)
#         new_df["end"] = new_df["end"].astype(int)
#         new_df.to_csv(
#             os.path.join("../outputs", "results", self.model_name, video_name.split('/')[-1].replace(".mp4", ".csv")),
#             index=False)

#         # print(new_props)
#         #         with open("../outputs/out.json", "w") as out:
#         #             json.dump(new_props, out, indent = 2)

#         #         # Calculate the cumulative values
#         #         cum_av_score = np.max([prop["A/V Score"] for prop in new_props])
#         #         cum_v_score = np.max([prop["V Score"] for prop in new_props])
#         #         cum_a_score = np.max([prop["A Score"] for prop in new_props])

#         #         # Store the cumulative values in the results dictionary
#         #         self.results[video_name] = {
#         #             "Cumulative A/V Score": float(cum_av_score),
#         #             "Cumulative V Score": float(cum_v_score),
#         #             "Cumulative A Score": float(cum_a_score),
#         #         }

#         # self.results[video_name] = new_props


# def inference_batfd(model_name: str, model: LightningModule, dm: LAVDFDataModule, max_duration: int, gpus: int = 1):
#     Path(os.path.join("output", "results", model_name)).mkdir(parents=True, exist_ok=True)
#     model.eval()

#     test_dataset = dm.test_dataset
#     save_to_json_call = SaveToJsonCallback(max_duration, test_dataset.metadata, model_name)
#     trainer = Trainer(logger=False,
#         enable_checkpointing=False, devices=1 if gpus > 1 else None,
#         accelerator="gpu" if gpus > 0 else "cpu",
#         callbacks=[save_to_json_call]
#     )

#     trainer.predict(model, dm.test_dataloader())
#     return save_to_json_call.results

import os.path
from pathlib import Path
from typing import Any, List

import numpy as np
import pandas as pd
from pytorch_lightning import LightningModule, Trainer, Callback

from .dataset import LAVDFDataModule
from .dataset.lavdf import Metadata


class SaveToCsvCallback(Callback):
    def __init__(self, max_duration: int, metadata: List[Metadata], model_name: str):
        super().__init__()
        self.max_duration = max_duration
        self.metadata = metadata
        self.model_name = model_name

    def on_predict_batch_end(
        self,
        trainer: Trainer,
        pl_module: LightningModule,
        outputs: Any,
        batch: Any,
        batch_idx: int,
        dataloader_idx: int,
    ) -> None:
        fusion_bm_map = outputs[0].cpu().numpy()[0]
        frames = batch[3][0]
        video_name = self.metadata[batch_idx].file

        # for each boundary proposal in boundary map
        new_props = []
        for i in range(frames):
            for j in range(1, self.max_duration):
                # begin frame and end frame
                begin = i
                end = i + j
                if end <= frames:
                    new_props.append([begin, end, fusion_bm_map[j, i]])

        new_props = np.stack(new_props)
        col_name = ["begin", "end", "score"]
        new_df = pd.DataFrame(new_props, columns=col_name)
        new_df["begin"] = new_df["begin"].astype(int)
        new_df["end"] = new_df["end"].astype(int)
        print(122)
        new_df.to_csv(
            os.path.join("../outputs", self.model_name, video_name.split('/')[-1].replace(".mp4", ".csv")),
            index=False)


def inference_batfd(model_name: str, model: LightningModule, dm: LAVDFDataModule, max_duration: int, gpus: int = 1):
    Path(os.path.join("../outputs", model_name)).mkdir(parents=True, exist_ok=True)
    model.eval()

    test_dataset = dm.test_dataset

    trainer = Trainer(logger=False,
        enable_checkpointing=False, devices=1 if gpus > 1 else None,
        accelerator="gpu" if gpus > 0 else "cpu",
        callbacks=[SaveToCsvCallback(max_duration, test_dataset.metadata, model_name)]
    )

    trainer.predict(model, dm.test_dataloader())