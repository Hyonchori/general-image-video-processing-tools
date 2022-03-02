# Load youtube video and save as frames
import argparse
import os
import sys
from pathlib import Path

import cv2

FILE = Path(__file__).absolute()
utils_dir = FILE.parents[1]
if utils_dir not in sys.path:
    sys.path.append(utils_dir.as_posix())
from custom_utils.general import increment_path, get_youtube_stream


def main(args):
    source = args.source
    save_dir = args.save_dir
    target_size = args.target_size
    view = args.view
    save_mode = args.save_mode
    assert save_mode in [1, 2], f"Save mode should be in [1(images), 2(video)]"

    print(f"\n--- Processing {source}")
    run_name = Path(source).name
    save_dir = increment_path(Path(save_dir) / run_name, exist_ok=False)
    save_dir.mkdir(parents=True, exist_ok=True)

    source = get_youtube_stream(source)
    cap = cv2.VideoCapture(source)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_seconds = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps)
    tmp_frame1 = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    if save_mode == 2:
        save_path = os.path.join(save_dir, f"{run_name}.mp4")
        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, target_size)

    print(f"\twidth: {width}, height: {height}, fps: {fps:.2f}, duration: {total_seconds // 60}:{total_seconds % 60}")
    while True:
        ret, img = cap.read()
        if not ret:
            break
        tmp_frame2 = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        if tmp_frame1 == tmp_frame2:
            continue
        else:
            tmp_frame1 = tmp_frame2
        img = cv2.resize(img, dsize=target_size)
        if save_mode == 1:
            save_path = os.path.join(save_dir, f"{run_name}_{tmp_frame1}.png")
            cv2.imwrite(save_path, img)
        else:  # save_mode == 2:
            vid_writer.write(img)
        if view:
            cv2.imshow("img", img)
            cv2.waitKey(1)
    if save_mode == 1:
        print(f"\ttotal {tmp_frame1} images are saved!")
    else:
        print(f"total video is saved!")


def parse_args():
    parser = argparse.ArgumentParser()

    source = "https://www.youtube.com/watch?v=cDD2ToN10KI"
    parser.add_argument("--source", type=str, default=source)

    save_dir = f"{FILE.parents[1]}/youtube_frames"
    parser.add_argument("--save-dir", type=str, default=save_dir)

    target_size = [1280, 720]
    parser.add_argument("--target-size", type=int, default=target_size)

    parser.add_argument("--view", action="store_true", default=True)
    parser.add_argument("--save-mode", type=int, default=2)  # 1: images, 2: video

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    opt = parse_args()
    main(opt)
