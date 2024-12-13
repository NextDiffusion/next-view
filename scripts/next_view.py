import subprocess
import gradio as gr
from pathlib import Path
from modules import script_callbacks
import modules.scripts as scripts
import datetime
import re

base_dir = scripts.basedir()


def split_video_to_images(video_path, output_dir, final_log_textbox):
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
    with subprocess.Popen(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        result, _ = process.communicate()

    # Convert the frame rate string to a float
    frame_rate = eval(result)
    print(f"Frame rate of input video: {frame_rate} fps")

    # Use ffmpeg to split the video into image sequences with the determined frame rate
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps={frame_rate}",
        output_pattern,
    ]
    with subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        _, _ = process.communicate()

    # Count the number of frames and calculate the total size
    frame_files = list(output_dir.glob("frame_*.png"))
    num_frames = len(frame_files)
    total_size = sum(f.stat().st_size for f in frame_files) / \
        (1024 * 1024)  # Convert to MB
    final_log = f"Video split into {num_frames} images with {frame_rate} fps. The total size is {total_size:.2f} MB."

    print(
        f"Video split into {num_frames} images with {frame_rate} fps. The total size is {total_size:.2f} MB.")

    return final_log


def submit_video(video,out_dir, final_log_textbox):
    # Convert the video path to a pathlib.Path object
    video_directory = Path(video)
    print(f"Uploaded video directory: {video_directory}")

    # Generate a timestamp based on the current date and time
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Create a unique subfolder within "image_sequences" using the timestamp and random identifier
    if out_dir == "":
        output_dir = Path(base_dir, "image_sequences", f"{timestamp}")
    else:
        output_dir = Path(out_dir,"image_sequences", f"{timestamp}")
    # Create parent directories if needed
    output_dir.mkdir(parents=True, exist_ok=True)

    # Split the uploaded video into image sequences
    final_log = split_video_to_images(video, output_dir, final_log_textbox)
    # Return the output directory as a string
    return [str(output_dir), final_log]


def image_sequence_to_video(image_sequence_location, fps, video_out_location, images_pattern, images_regex):
    # Convert the image sequence location to an absolute path
    image_sequence_location = Path(image_sequence_location).absolute()
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    if video_out_location == "":
        output_directory = Path(base_dir, "output_videos")
    else:
        output_directory = Path(video_out_location,"output_videos")

    
    output_directory.mkdir(parents=True, exist_ok=True)

    frame_files = sorted(image_sequence_location.glob(
        images_pattern), key=lambda x: tuple(map(int, re.findall(r''+images_regex+'', x.name))))
    frame_numbers = [int(re.search(r''+images_regex+'', frame.name).group(1))
                     for frame in frame_files]

    # Set total_frames based on the total number of frames in frame_numbers
    total_frames = len(frame_numbers)

    # Explicitly create a file list with correct order
    file_list_path = Path(base_dir, "file_list.txt")
    with file_list_path.open('w') as file_list:
        for frame in frame_files:
            file_list.write(f"file '{frame}'\n")

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

    with subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True) as process:
        # Regular expression to extract frame information from stderr
        frame_regex = re.compile(r"frame=\s*(\d+)")
        for line in process.stderr:
            # Extract and print progress information
            match = frame_regex.search(line)
            if match:
                current_frame = int(match.group(1))
                progress = current_frame / total_frames
                progress_bar_length = 50
                bar = "♥" * int(progress * progress_bar_length)
                spaces = " " * (progress_bar_length - len(bar))
                print(
                    f"Generating your video with {fps} FPS: [{bar}{spaces}] {current_frame}/{total_frames} frames processed", end="\r")

    # Remove the temporary file list
    file_list_path.unlink()

    print(f"\nVideo generated. File Location: {output_video_path}")

    return str(output_video_path)


def open_file_location(output_dir):
    # Open the image sequence file location when the button is clicked
    subprocess.Popen(["explorer", str(output_dir)], shell=True)


def open_video_file_location(output_dir):
    # Open the video file location when the button is clicked
    video_file_location = Path(output_dir, "output_videos")
    subprocess.Popen(["explorer", str(video_file_location)], shell=True)


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
                with gr.Row(elem_id="output_row"):
                    # Define the output component for displaying the image sequence location
                    out_location = gr.Textbox(
                        show_copy_button=False,
                        type="text",
                        label="Image Sequence Location (if blank, default location)",
                        width="auto",
                    )
                    open_location_button = gr.Button(variant='secondary', size='sm', value="📂",
                                                     elem_id="open_location_button", scale=0)
                    open_location_button.click(
                        fn=open_file_location, inputs=out_location)

                # Define the Textbox component for displaying the final log
                final_log_textbox = gr.Textbox(
                    type="text",
                    label="Result Information",
                    default="Final information will be displayed here.",
                    width="auto",
                )

                # Set the click function for the "Generate Image Sequence" button
                btn.click(fn=submit_video, inputs=[inp,out_location], outputs=[
                          out_location, final_log_textbox])

            with gr.Column():
                gr.HTML('''<h2>Image Sequence 2 Video 👇</h2>''')
                with gr.Row():
                    # Define the input component for specifying the image sequence location
                    inp = gr.Textbox(
                        type="text",
                        label="Image Sequence Location",
                    )

                with gr.Row():   
                    video_out_location = gr.Textbox(
                        show_copy_button=False,
                        type="text",
                        label="Video Out Location (if blank, default location)",
                        width="auto",
                    )
                    open_video_location_button = gr.Button(variant='secondary', size='sm', value="📂",
                                                           elem_id="open_video_location_button", scale=0)
                    open_video_location_button.click(
                        fn=open_video_file_location,inputs=video_out_location)

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

                with gr.Accordion(label="Image sequence settings", open=False):
                    images_pattern = gr.Textbox(
                        label="Images pattern",
                        lines=1,
                        value='frame_*.png',
                        info="The pattern used to get the images"
                    )
                    images_regex = gr.Textbox(
                        label="Images regex",
                        lines=1,
                        value='frame_(\d+)(?:-\d+)?\.png',
                        info="Define the regex used to order the images, note that the first group (wrapped by parenthesis) is used to determine the order. (the regex must be compatible with the pattern defined above)"
                    )

                with gr.Row(elem_id="output_row"):
                    # Define the button for generating the video
                    btn = gr.Button("Generate Video",
                                    elem_id="generate_video_button")

                # Set the click function for the "Generate Video" button
                btn.click(fn=image_sequence_to_video,
                          inputs=[inp, fps, video_out_location, images_pattern, images_regex], outputs=out)

    return (next_view, "NextView", "NextView"),


# Register the UI layout function with script_callbacks
script_callbacks.on_ui_tabs(on_ui_tabs)
