# Cut video from start to end frame
import argparse
import os
from pathlib import Path
from datetime import timedelta

import cv2
from tqdm import tqdm


def main(args):
    vid_path = args.vid_path
    save_dir = args.save_dir
    start_time = time2timedelta(args.start_time)
    end_time = time2timedelta(args.end_time)
    view = args.view
    save = args.save

    cap = cv2.VideoCapture(vid_path)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_seconds = int(total_frames / fps)
    total_time = time2timedelta([0, 0, total_seconds])

    start_frame_rate = start_time / total_time
    end_frame_rate = end_time / total_time
    start_frame = int(total_frames * start_frame_rate)
    end_frame = int(total_frames * end_frame_rate)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    save_path = os.path.join(save_dir, ".".join(Path(vid_path).name.split(".")[:-1]) + "_trimmed.mp4")
    vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    print(f"\n--- Processing {Path(vid_path).name}")
    for _ in tqdm(range(end_frame - start_frame)):
        ret, img = cap.read()
        if not ret:
            break
        if view:
            cv2.imshow("img", img)
            cv2.waitKey(1)
        if save:
            vid_writer.write(img)


def time2timedelta(t):
    return timedelta(hours=t[0], minutes=t[1], seconds=t[2])


def parse_args():
    parser = argparse.ArgumentParser()

    vid_path = "/home/daton/Desktop/gs/intrusion/C059100_001.mp4"
    vid_path = "/home/daton/Desktop/gs/intrusion/C061102_003.mp4"
    vid_path = "/home/daton/Desktop/gs/intrusion/C065100_009.mp4"
    parser.add_argument("--vid-path", type=str, default=vid_path)

    save_dir = "/home/daton/Desktop/gs/intrusion_gs_v3/"
    parser.add_argument("--save-dir", type=str, default=save_dir)

    # [hours, minutes, seconds]
    start_time = [0, 2, 54]
    start_time = [0, 3, 0]
    start_time = [0, 3, 0]
    start_time = [0, 0, 0]
    parser.add_argument("--start-time", type=int, default=start_time)

    # [hours, minutes, seconds]
    end_time = [0, 6, 15]
    end_time = [0, 7, 35]
    end_time = [0, 6, 45]
    parser.add_argument("--end-time", type=int, default=end_time)

    parser.add_argument("--view", action="store_true", default=False)
    parser.add_argument("--save", action="store_true", default=True)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    opt = parse_args()
    main(opt)
