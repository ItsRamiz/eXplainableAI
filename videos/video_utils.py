from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx

def convert_to_mp4(video_path):
    clip = VideoFileClip(str(video_path))
    output_path = video_path.with_suffix(".mp4")
    clip.write_videofile(str(output_path), codec="libx264")

def extend_video(video_path, extension_factor):
    original_clip = VideoFileClip(str(video_path))
    extended_clip = original_clip.fx(vfx.time_symmetrize)
    output_path = video_path.with_suffix(".extended.mp4")
    extended_clip.write_videofile(str(output_path), codec="libx264")
