import os
import subprocess

from hevc_cache_simulator import CacheSimulatorHEVC

# Metadata
TRACE_INPUT = "mem_trace.txt"
CACHE_OUTPUT = "cache_output.txt"

HEADER = "Video Sequence;Encoder Configuration;Hit Count;Miss Count"

# HEVC Paths
HM = "../hm-videomem/"

ENCODER_CMD = HM + "bin/TAppEncoderStatic"

CONFIG = {  # "Low Delay": HM + "cfg/encoder_lowdelay_main.cfg",
    "Random Access": HM + "cfg/encoder_randomaccess_main.cfg"}

VIDEO_CFG_PATH = HM + "cfg/per-sequence/"

VIDEO_SEQUENCES_PATH = "../video_sequences"

# Parameters
FRAMES = '9'


def list_all_videos(path):
    paths = list()

    for root, _, files in os.walk(path):
        for f in files:
            video_path = os.path.join(root, f)
            paths.append(video_path)

    return paths


def get_video_info(video_path):
    # video_path: '../video_sequences/BQTerrace_1920x1080_60.yuv'
    parse = video_path.split("/")
    video_info = parse.pop()

    # ['BQTerrace', '1920x1080', '60.yuv']
    title, resolution, *_ = video_info.split("_")
    width, height = resolution.split('x')

    video_cfg = VIDEO_CFG_PATH + title + ".cfg"

    return title, int(width), int(height), video_cfg


def generate_trace(cfg_path, video_cfg, video_path):
    cmd_array = [ENCODER_CMD, '-c', cfg_path, '-c', video_cfg,
                 '-i', video_path, '-f', FRAMES]

    subprocess.run(cmd_array)


def clean():
    # Remove temporary files
    try:
        os.remove(TRACE_INPUT)
        os.remove('str.bin')
        os.remove('rec.yuv')
    except FileNotFoundError:
        pass


def process_video(video_path):
    title, width, height, video_cfg = get_video_info(video_path)

    for cfg, cfg_path in CONFIG.items():
        generate_trace(cfg_path, video_cfg, video_path)

        output = cache_simulator.simulate(title, width, height, cfg)
        cache_simulator.clear()

        with open(CACHE_OUTPUT, 'w+') as output_file:
            output_file.write(output)

        clean()


if __name__ == "__main__":
    cache_simulator = CacheSimulatorHEVC()

    # Creates output file
    with open(CACHE_OUTPUT, 'w+') as output_file:
        output_file.write(HEADER)

    videos = list_all_videos(VIDEO_SEQUENCES_PATH)

    [process_video(video) for video in videos]