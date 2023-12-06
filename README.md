# NextView

Adds a '**NextView**' tab to the Stable Diffusion Web UI that allows the user to:
- **Turn Video 2 Image Sequences**
- **Turn Image Sequences 2 Video**

![Next_Diffusion_Next_View_Video2ImageSequence_ImageSequence2Video](https://res.cloudinary.com/db7mzrftq/image/upload/v1695207953/Next_Diffusion_Next_View_Video2_Image_Sequence_Image_Sequence2_Video_d463eb9365.webp)

## Requirements
Make sure you have FFmpeg installed.

### How to install FFmpeg?
Follow the steps below to install FFmpeg on your windows machine:

Here's a simple breakdown:
- Open your command prompt
- Enter the following command and hit enter: winget install -e --id Gyan.FFmpeg
- Voila! FFmpeg is now installed

## Installation NextView Extension

1. Open your Stable Diffusion Web UI.
2. Click on the "Extensions" tab.
3. Navigate to the "Install from URL" subsection.
4. Paste the following URL: https://github.com/NextDiffusion/next-view
5. Click on the "Install" button.
6. After installation go to the "Installed" tab and click on "Apply and restart UI".

## Usage

On the left side you have the "Video 2 Image Sequence" section where you can upload a video and turn in into an **image sequence**:

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


On the right side you have the "Image Sequence 2 Video" section:

![Next_Diffusion_Next_View_ImageSequence2Video](https://res.cloudinary.com/db7mzrftq/image/upload/v1695209722/Next_Diffusion_Next_View_Image_Sequence2_Video_4cb9aca4ae.webp)

**Input**
- Start by pasting an "Image Sequence Location" folder name
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
