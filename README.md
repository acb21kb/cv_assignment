# COM31006 Computer Vision Assignment - Image-to-Image Steganography
## Set up
Ensure the conda environment [com31006_env.yaml](com31006_env.yaml) is used as this contains all the necessary libraries and dependencies used in this code.

## Run the code
- The code should be run from the [main_dashboard.py](main_dashboard.py) file.
- Images to be watermarked should be stored in the [images](images) folder.
- It is not recommended to alter the watermarks, but if required replace one of the selection and ensure it has the same size and file name.

## Expected code functions
User interface is implemented in [main_dashboard.py](main_dashboard.py), please only run the code from this file.
### Embedding watermark
Code is implemented in [watermark_embed.py](watermark_embed.py)
- Select image to be watermark and select watermark to embed from the preset options
- Embed watermark in this image and show result (should be imperceptible)
- Option to generate 'drastic' watermarked image as well as normal watermark by ticking checkbox before the run embed button - this generates both versions but displays only the 'drastic' resulting image to show watermark placements
### Recovering watermark
Code is implemented in [watermark_recover.py](watermark_recover.py)
- Select image to test for watermark recovery
- Recovery average watermark and show result (note: the result is inverted to the original watermark)
- States confidence of recovered watermark consistency
### Detecting tampering
Code is implemented in [tamper_detect.py](tamper_detect.py)
- Process selected images and compare keypoints detected
- Check image for cropping, resizing and rotation
- Return mapping of keypoint differences between the two images

## File structure
A brief explanation of what each folder contains.
| Folder | Contains |
| ------ | -------- |
| [/images](images)  | Original unwatermarked images |
| [/watermarks](watermarks) | The watermarks to be used |
| [/embedded](embedded) | The watermarked images are stored here once generated |
| [/drastic](drastic) | Where the drastic versions of the watermarked images are stored if selected |
| [/recovered](recovered) | The recovered watermarks are stored here if recovered from the image |
| [/tampered](tampered) | The selection of watermarked images that have been tampered with (resized, rotated, cropped) |
| [/detect_matches](detect_matches) | Where the resulting keypoint match image is stored, where matching and non-matching keypoints are shown |

## Contributions
Code was developed by: Katie Broadhurst | acb21kb | <kbroadhurst1@sheffield.ac.uk>