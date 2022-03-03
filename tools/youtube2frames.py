# Load youtube video and save as frames or video
import argparse
import os
import sys
from pathlib import Path
from datetime import timedelta

import cv2

FILE = Path(__file__).absolute()
utils_dir = FILE.parents[1]
if utils_dir not in sys.path:
    sys.path.append(utils_dir.as_posix())
from custom_utils.general import increment_path, get_youtube_stream


def main(args):
    source = args.source
    start_time = args.start_time
    end_time = args.end_time
    save_dir = args.save_dir
    target_size = args.target_size
    view = args.view
    save = args.save
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
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    total_seconds = int(total_frames / fps)
    tmp_frame1 = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    if save_mode == 2:
        save_path = os.path.join(save_dir, f"{run_name}.mp4")
        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, target_size)

    if start_time is None:
        start_frame = 0
    else:
        assert all(isinstance(x, int) for x in start_time), "All elements in start_time should be int"
        start_time_delta = timedelta(hours=start_time[0], minutes=start_time[1], seconds=start_time[2])
        total_time_delta = timedelta(seconds=total_seconds)
        start_time_rate = min(1, max(0, start_time_delta / total_time_delta))
        start_frame = int(total_frames * start_time_rate)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    if end_time is None:
        end_frame = total_frames
    else:
        assert all(isinstance(x, int) for x in end_time), "All elements in end_time should be int"
        if any(x < 0 for x in end_time):
            end_frame = total_frames
        else:
            end_time_delta = timedelta(hours=end_time[0], minutes=end_time[1], seconds=end_time[2])
            total_time_delta = timedelta(seconds=total_seconds)
            end_time_rate = min(1, max(0, end_time_delta / total_time_delta))
            end_frame = int(total_frames * end_time_rate)
            assert end_frame >= start_frame, "end_time should be bigger than start time"

    print(f"\twidth: {width}, height: {height}, fps: {fps:.2f}, " +
          f"duration: {total_seconds // 60}:{total_seconds % 60}, total_frames: {total_frames}\n" +
          f"\tstart_time: {start_time_delta}, end_time: {end_time_delta}")

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
        if save:
            if save_mode == 1:
                save_path = os.path.join(save_dir, f"{run_name}_{tmp_frame1}.png")
                cv2.imwrite(save_path, img)
            else:  # save_mode == 2:
                vid_writer.write(img)
        if view:
            cv2.imshow("img", img)
            cv2.waitKey(1)
        if tmp_frame1 == end_frame:
            break
    if save:
        if save_mode == 1:
            print(f"\ttotal {tmp_frame1} images are saved!")
        else:
            print(f"total video is saved!")


def parse_args():
    parser = argparse.ArgumentParser()

    source = "https://www.youtube.com/watch?v=P8dgrReTkrU"
    parser.add_argument("--source", type=str, default=source)

    start_time = [0, 0, 59]
    parser.add_argument("--start-time", type=int, default=start_time)

    end_time = [0, 1, 11]
    parser.add_argument("--end-time", type=int, default=end_time)

    save_dir = f"{FILE.parents[1]}/youtube_frames"
    parser.add_argument("--save-dir", type=str, default=save_dir)

    target_size = [1280, 720]
    parser.add_argument("--target-size", type=int, default=target_size)

    parser.add_argument("--view", action="store_true", default=True)
    parser.add_argument("--save", action="store_true", default=False)
    parser.add_argument("--save-mode", type=int, default=2)  # 1: images, 2: video

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    opt = parse_args()
    main(opt)
