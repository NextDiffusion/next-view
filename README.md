# NextView

Adds a '**NextView**' tab to the Stable Diffusion Web UI that allows the user to:
- **Turn Video 2 Image Sequences**
- **Turn Image Sequences 2 Video**

![Next_Diffusion_Next_View_Video2ImageSequence_ImageSequence2Video](https://res.cloudinary.com/db7mzrftq/image/upload/v1695207953/Next_Diffusion_Next_View_Video2_Image_Sequence_Image_Sequence2_Video_d463eb9365.webp)

## Requirements
Make sure you have ffmpeg installed. Not sure [how to install ffmpeg](https://www.nextdiffusion.ai/tutorials/how-to-install-ffmpeg-on-windows-for-stable-diffusion-a-comprehensive-guide) on your machine?

### What is FFmpeg?
FFmpeg is a powerful and versatile software tool that allows you to work with audio and video files. It's like a Swiss Army knife for multimedia tasks.

Here's a simple breakdown:
- Audio and Video: FFmpeg can handle both audio (sound) and video (moving images).
- Conversion: You can use FFmpeg to convert one type of audio or video file into another. For example, you can change a video from one format to another, like from MP4 to AVI.
- Editing: FFmpeg lets you edit multimedia files. You can cut, join, or even add effects to videos and audio.
- Streaming: It's also used for streaming media online. Many streaming platforms use FFmpeg behind the scenes.
- Open Source: FFmpeg is open-source software, which means it's free to use and is continually improved by a community of developers.

In a nutshell, if you want to do anything with audio or video files, FFmpeg is a handy tool to have in your toolbox.

## Installation NextView Extension

1. Open your Stable Diffusion Web UI.
2. Click on the "Extensions" tab.
3. Navigate to the "Install from URL" subsection.
4. Paste the following URL: https://github.com/NextDiffusion/next-view
5. Click on the "Install" button.
6. After installation go to the "Installed" tab and click on "Apply and restart UI".

## Usage

On the left side you have the **Video 2 Image Sequence** section where you can upload a video and turn in into an **image sequence**:

![Next_Diffusion_Next_View_Video2ImageSequence](https://res.cloudinary.com/db7mzrftq/image/upload/v1695209566/Next_Diffusion_Next_View_Video2_Image_Sequence_nextdiffusion_943d22af2e.webp)

**Input**
- Upload a video you want to turn to an image sequence
- Click on the "Generate Image Sequence" button to turn it into an image sequence

_You also have the option to click the "Clear" button to remove the uploaded video._

**Output**
- If everything went alright, you now will see your "Image Sequence Location" where the images are stored.
- The output location of the images will be the following: "stable-diffusion-webui\extensions\next-view\image_sequences\{timestamp}"
- The images in the output directory will be in a PNG format
- The images will have the following naming structure: "frame_0001", "frame_0002" etc. 
- You now have the option to copy the output location by clicking on the "Copy" icon in the right bottom corner.


On the right side you have the **Image Sequence 2 Video** section:

![Next_Diffusion_Next_View_ImageSequence2Video](https://res.cloudinary.com/db7mzrftq/image/upload/v1695209722/Next_Diffusion_Next_View_Image_Sequence2_Video_4cb9aca4ae.webp)

**Input**
- Start by pasting a Image Sequence Location folder name
- The images within this folder **should be of PNG format**
- The images **should have the following naming structure** when converting to a video: "frame_0001", "frame_0002" etc. 
- When everything is correct you can click on the "Generate Video" button to turn it into an image sequence

**Output**
- If everything went alright, you now will see your "Generated Video" where you can play/download it.
- The output location of the video will be the following: "stable-diffusion-webui\extensions\next-view\output_videos
- The video will be of MP4 format.

## Credits: **Next Diffusion** ❤️

- [Next Diffusion Website](https://www.nextdiffusion.ai/) 
- [Next Diffusion Youtube](https://www.youtube.com/channel/UCd9UIUkLnjE-Fj-CGFdU74Q?sub_confirmation=1) 
