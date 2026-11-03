"""Real programs for the video-download power cards (DL-*) that do not already have a code proof.

DL-01..04, 06, 07, 09 are proven by scripts/fetch_video.py; DL-10 is a chain needing faster-whisper.
The functions live with the shared media helpers in photo_video_footage.py.
"""
from .photo_video_footage import dl_05, dl_08, dl_11

PROGRAMS = {"DL-05": dl_05, "DL-08": dl_08, "DL-11": dl_11}
