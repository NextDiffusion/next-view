import subprocess
import gradio as gr
from pathlib import Path
from modules import script_callbacks
import modules.scripts as scripts
import datetime
import re

base_dir = scripts.basedir()


def split_video_to_images(video_path, output_dir):
    output_pattern = Path(output_dir) / "frame_%04d.png"
    ffprobe_cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path,
    ]
    result = subprocess.run(ffprobe_cmd, stdout=subprocess.PIPE, text=True)
    # Convert the frame rate string to a float
    frame_rate = eval(result.stdout)
    print(f"Frame rate of input video: {frame_rate} fps")

    ffmpeg_cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps={frame_rate}",  # Use the determined frame rate
        output_pattern,
    ]
    subprocess.run(ffmpeg_cmd)
    print(f"Video split into image sequences with {frame_rate} fps.")


def submit_video(video):
    video_directory = Path(video)
    print(f"Uploaded video directory: {video_directory}")

    # Generate a timestamp based on the current date and time
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Create a unique subfolder within "image_sequences" using the timestamp and random identifier
    output_dir = Path(base_dir, "image_sequences", f"{timestamp}")
    # Create parent directories if needed
    output_dir.mkdir(parents=True, exist_ok=True)

    split_video_to_images(video, output_dir)
    return str(output_dir)  # Return the output directory as a string


def image_sequence_to_video(image_sequence_location, fps):
    image_sequence_location = Path(image_sequence_location)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_directory = Path(base_dir, "output_videos")
    # Create the directory if it doesn't exist
    output_directory.mkdir(parents=True, exist_ok=True)
    output_video_path = output_directory / f"output_video_{timestamp}.mp4"

    # Detect the first frame number dynamically
    frame_files = sorted(image_sequence_location.glob("frame_*.png"))
    if frame_files:
        first_frame = frame_files[0].name
        match = re.search(r'(\d+)', first_frame)
        if match:
            start_frame_number = int(match.group())
        else:
            start_frame_number = 1
    else:
        start_frame_number = 1

    # Use ffmpeg to convert image sequences into a video
    ffmpeg_cmd = [
        "ffmpeg",
        "-framerate", f"{fps}",  # You can set the desired frame rate here
        "-start_number", str(start_frame_number),  # Set the start frame number
        "-i", f"{image_sequence_location}/frame_%04d.png",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_video_path,
    ]
    subprocess.run(ffmpeg_cmd)

    return output_video_path


def on_ui_tabs():

    with gr.Blocks(analytics_enabled=False) as next_view:
        with gr.Row():
            with gr.Column():
                gr.HTML('''<h2>Video 2 Image Sequence 👇</h2>''')
                inp = gr.Video(
                    type="file",
                    format="mp4",
                    label="Upload Video",
                    interactive=True,
                    width="auto",
                    height=300,
                )
                with gr.Row():
                    gr.ClearButton(inp)
                    btn = gr.Button("Generate Image Sequence",
                                    elem_id="submit_video_button")

                out_location = gr.Textbox(
                    show_copy_button=True,
                    type="text",
                    label="Image Sequence Location"
                )

                btn.click(fn=submit_video, inputs=inp, outputs=out_location)

            with gr.Column():
                gr.HTML('''<h2>Image Sequence 2 Video 👇</h2>''')
                with gr.Row():
                    inp = gr.Textbox(
                        type="text",
                        label="Image Sequence Location",
                    )

                out = gr.Video(
                    type="auto",
                    label="Generated Video",
                    width="auto",
                    height=300,
                )

                fps = gr.Slider(2, 240, value=24, label="Frames Per Second (FPS)",
                                step=1, info="Choose your FPS", elem_id="fps_slider")
                btn = gr.Button("Generate Video",
                                elem_id="generate_video_button")

                btn.click(fn=image_sequence_to_video,
                          inputs=[inp, fps], outputs=out)

    return (next_view, "NextView", "NextView"),


script_callbacks.on_ui_tabs(on_ui_tabs)
