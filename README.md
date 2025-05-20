# COM31006 Computer Vision Assignment - Image-to-Image Steganography
## Set up
Ensure the conda environment [com31006_env.yaml](com31006_env.yaml) is used as this contains all the necessary libraries and dependencies used in this code.

## Run the code
- The code should be run from the [main_dashboard.py](main_dashboard.py) file.
- Images to be watermarked should be stored in the [images](images) folder.

## Expected code functions
### Embedding watermark
- Select image to be watermark and select watermark to embed from the preset options
- Embed watermark in this image and show result (should be imperceptible)
- Option to generate 'drastic' watermarked image as well as normal watermark by ticking checkbox before the run embed button - this generates both versions but displays only the 'drastic' resulting image to show watermark placements
### Recovering watermark
- Select image to test for watermark recovery
- Recovery average watermark and show result (note: the result is inverted to the original watermark)
- States confidence of recovered watermark consistency
### Detecting tampering
- Process selected images and compare keypoints detected
- Check image for cropping, resizing and rotation
- Return mapping of keypoint differences between the two images

## Contributions
Code was developed by: Katie Broadhurst | acb21kb | <kbroadhurst1@sheffield.ac.uk>