import subprocess
import gradio as gr
from pathlib import Path
from modules import script_callbacks
import modules.scripts as scripts
import datetime
import re
import tempfile

base_dir = scripts.basedir()


def split_video_to_images(video_path, output_dir):
    # Define the pattern for naming the output frames
    output_pattern = Path(output_dir) / "frame_%04d.png"

    # Use ffprobe to get the frame rate of the input video
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

    # Use ffmpeg to split the video into image sequences with the determined frame rate
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps={frame_rate}",
        output_pattern,
    ]
    subprocess.run(ffmpeg_cmd)
    print(f"Video split into image sequences with {frame_rate} fps.")


def submit_video(video):
    # Convert the video path to a pathlib.Path object
    video_directory = Path(video)
    print(f"Uploaded video directory: {video_directory}")

    # Generate a timestamp based on the current date and time
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Create a unique subfolder within "image_sequences" using the timestamp and random identifier
    output_dir = Path(base_dir, "image_sequences", f"{timestamp}")
    # Create parent directories if needed
    output_dir.mkdir(parents=True, exist_ok=True)

    # Split the uploaded video into image sequences
    split_video_to_images(video, output_dir)
    return str(output_dir)  # Return the output directory as a string


def image_sequence_to_video(image_sequence_location, fps):
    # Convert the image sequence location to an absolute path
    image_sequence_location = Path(image_sequence_location).absolute()
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_directory = Path(base_dir, "output_videos")
    output_directory.mkdir(parents=True, exist_ok=True)

    frame_files = sorted(image_sequence_location.glob(
        "frame_*.png"), key=lambda x: int(re.search(r'(\d+)', x.name).group()))
    frame_numbers = [int(re.search(r'(\d+)', frame.name).group())
                     for frame in frame_files]

    # Explicitly create a file list with correct order
    file_list_path = Path(base_dir, "file_list.txt")
    with file_list_path.open('w') as file_list:
        for num in frame_numbers:
            file_list.write(
                f"file '{image_sequence_location}/frame_{num:04d}.png'\n")

    # Use ffmpeg with the file list to generate the output video
    output_video_path = output_directory / f"output_video_{timestamp}.mp4"
    ffmpeg_cmd = [
        "ffmpeg",
        "-r", f"{fps}",
        "-f", "concat",
        "-safe", "0",
        "-i", str(file_list_path),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        str(output_video_path),
    ]

    subprocess.run(ffmpeg_cmd)

    # Remove the temporary file list
    file_list_path.unlink()

    print(f"Video generated at: {output_video_path}")

    return str(output_video_path)


def on_ui_tabs():
    # Define the UI layout using Gradio Blocks
    with gr.Blocks(analytics_enabled=False) as next_view:
        with gr.Row():
            with gr.Column():
                gr.HTML('''<h2>Video 2 Image Sequence 👇</h2>''')
                # Define the input components for uploading a video
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
                    # Define the button for generating image sequences
                    btn = gr.Button("Generate Image Sequence",
                                    elem_id="submit_video_button")

                # Define the output component for displaying the image sequence location
                out_location = gr.Textbox(
                    show_copy_button=True,
                    type="text",
                    label="Image Sequence Location"
                )

                # Set the click function for the "Generate Image Sequence" button
                btn.click(fn=submit_video, inputs=inp, outputs=out_location)

            with gr.Column():
                gr.HTML('''<h2>Image Sequence 2 Video 👇</h2>''')
                with gr.Row():
                    # Define the input component for specifying the image sequence location
                    inp = gr.Textbox(
                        type="text",
                        label="Image Sequence Location",
                    )

                # Define the output component for displaying the generated video
                out = gr.Video(
                    type="auto",
                    label="Generated Video",
                    width="auto",
                    height=300,
                )

                # Define the slider for selecting frames per second (FPS)
                fps = gr.Slider(2, 240, value=24, label="Frames Per Second (FPS)",
                                step=1, info="Choose your FPS", elem_id="fps_slider")
                # Define the button for generating the video
                btn = gr.Button("Generate Video",
                                elem_id="generate_video_button")

                # Set the click function for the "Generate Video" button
                btn.click(fn=image_sequence_to_video,
                          inputs=[inp, fps], outputs=out)

    return (next_view, "NextView", "NextView"),


# Register the UI layout function with script_callbacks
script_callbacks.on_ui_tabs(on_ui_tabs)
