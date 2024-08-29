# Hizenn: Emotion Detection and Image Description App

![icon](https://github.com/TheSaucese/hizennberg/assets/88286462/750d2669-b5de-4cb5-b738-cd25fb5499ba)


## Abstract
Hizenn is a user-friendly app designed for efficient emotion detection and image description. It provides three main features: video upload, image upload, and camera functionality. By analyzing frames, the app accurately detects emotions and generates descriptive information about the images. The results are presented in a clear format, ensuring that no details are lost during the analysis process.

![image](https://github.com/TheSaucese/hizennberg/assets/88286462/50a0c556-524a-47d9-a9fa-84f0babbd2c8)

## Introduction

Emotion detection and image description are integral components in numerous applications that involve human-computer interaction, such as social robotics, virtual assistants, and content moderation. The ability to accurately perceive and understand human emotions from visual cues is crucial for creating empathetic and responsive systems. Similarly, describing images in a meaningful way enhances accessibility, content understanding, and user engagement.

Recognizing the importance of these tasks, our application aims to provide an efficient solution for emotion detection and image description. By leveraging advanced techniques in computer vision and deep learning, our app empowers users to unlock the rich information embedded within images and videos. Whether it's analyzing facial expressions to gauge sentiment or generating detailed descriptions of visual content, our app offers a range of benefits to users across diverse domains.

In the realm of human-computer interaction, emotion detection plays a pivotal role. It allows virtual assistants to adapt their responses based on user emotions, leading to more personalized and empathetic interactions. In social robotics, emotion detection enables robots to understand and respond appropriately to human emotional states, fostering natural and engaging communication. Additionally, emotion detection holds significant value in applications such as market research, psychological studies, and sentiment analysis, where accurate emotion analysis is crucial for decision-making and understanding human behavior.

Image description, on the other hand, is essential for enhancing accessibility and content comprehension. By providing detailed and accurate descriptions of images and videos, our app enables visually impaired individuals to access visual content, enriching their online experience. It also aids in content moderation by automatically generating textual descriptions of images, helping identify inappropriate or harmful content more efficiently.

The benefits our app offers to users are numerous. It allows businesses to gain valuable insights into customer sentiment and preferences, leading to improved products and services. Educators can leverage our app to create interactive learning materials, enriching the educational experience for students. Individuals with visual impairments can now explore the visual world more independently, while content creators and moderators can streamline their workflows with automated image description capabilities.

In conclusion, our application addresses the crucial tasks of emotion detection and image description, empowering users across various domains. By accurately perceiving and understanding human emotions and generating meaningful image descriptions, our app enables more empathetic human-computer interactions, enhances accessibility, and streamlines content analysis. With our advanced computer vision capabilities, users can unlock new insights and possibilities, making their experiences richer, more engaging, and inclusive.

## Features

- **Video Upload**: Analyze video frames to detect emotions and describe images.
- **Image Upload**: Upload individual images and receive emotion detection and image description results.
- **Camera**: Utilize the camera functionality to analyze real-time video streams for emotion detection and image description.

## Methodology

The Hizenn app employs cutting-edge methodologies and technologies to deliver efficient and accurate results. It utilizes the following:

- **MTCNN** (Multi-task Cascaded Convolutional Networks) and **MediaPipe** face detection algorithms for detecting faces in video frames and images.
  
  ![image](https://github.com/TheSaucese/hizennberg/assets/88286462/1f3294d5-58c9-4dfb-919e-4972a9e79b01)

- **Fer2013** dataset and a highly trained Fer Model for emotion detection, which allows the app to accurately detect emotions from facial expressions.

  ![image](https://github.com/TheSaucese/hizennberg/assets/88286462/807f87a0-b26a-4b0e-a9ac-e0033ca6ee3c)

- **Stable Diffusion Prompt Interrogator**, a powerful image description model, to generate descriptive information about images without losing any details.

  ![image](https://github.com/TheSaucese/hizennberg/assets/88286462/6a64938e-1b29-485f-a3c4-3b1b29b7e50a)

- **Pyside6** framework for building the user interface, ensuring a seamless and intuitive experience for users.

  ![image](https://github.com/TheSaucese/hizennberg/assets/88286462/5011f143-a373-4fd8-96bd-ac01220a08b6)


The app has been extensively tested on a computer with 8GB VRAM, a 6-core AMD CPU (4.2GHz), and utilizes CUDA and TensorFlow to leverage GPU acceleration for faster results. Multithreading techniques have also been implemented to further enhance the app's performance.

The app incorporates the following:

- `Face Detection`: MediaPipe face detection and MTCNN (Multi-task Cascaded Convolutional Networks) algorithms are utilized for precise face detection and alignment.

- `Emotion Detection`: The app employs a well-trained Fer2013 model that utilizes the Fer2013 dataset for accurate emotion detection. It analyzes frames and determines the percentages of different emotions, with the highest percentage corresponding to the predicted emotion.

- `Image Description`: The Stable Diffusion Prompt Interrogator is used for image description. It generates descriptive information about the analyzed images.

- `Interface`: The app's interface is built using Pyside6, ensuring user-friendly interaction and ease of use.

- `Hardware and Optimization`: The app has been extensively tested on an 8GB VRAM computer with a 6-core AMD CPU running at 4.2GHz. GPU utilization is achieved through CUDA and TensorFlow, providing enhanced performance. Multithreading is implemented to expedite the processing and deliver faster results.

## Code Overview

The `hizenn.py` file serves as the main script for running the Hizenn app. It imports necessary libraries and modules, including PySide6 for GUI development, TensorFlow for deep learning, and various custom widgets for different functionalities.

The code initializes the app's interface by creating a `SplashScreen` class, which acts as a splash screen during the app's loading process. The `update` method updates a progress bar until it reaches completion, at which point the main app is launched.

The main functionalities of the app are provided by the following modules:

- `CameraWidget`: Implements the camera functionality for capturing real-time frames for emotion detection and image description.

- `VideoUploadWidget`: Enables the upload and analysis of video files for emotion detection.

- `ImageUploaderWidget`: Allows users to upload and analyze individual images for emotion detection and description.

Additionally, the app incorporates the QDarkTheme library for providing a dark theme interface.

The `CameraWidget` class in `camerawidget.py` serves as the main component for handling camera functionality and displaying real-time frames. It utilizes the OpenCV library for capturing frames from the camera, MediaPipe for face detection, and the FER model for emotion detection.

The class includes a `toggle_camera` method that enables users to turn the camera on and off. When the camera is turned on, the `display_frame` method is invoked periodically to capture frames, perform face detection, analyze emotions, and display the frames with detected emotions in the app's interface. The emotions are visualized using a pie chart generated by the QtCharts module.

The class also includes methods for updating the chart title based on the detected emotion and retrieving the appropriate color and emoji representation for each emotion.

The `CameraWidget` is integrated into the overall app layout and interacts with other components to provide a complete user experience.

The `ImageUploaderWidget` class in `imageUpload.py` provides functionality for uploading and analyzing images. It utilizes various Qt widgets and integrates with other modules and libraries to process and display image data.

The class includes the following features:

- `initUI()`: This method initializes the user interface of the widget. It sets up the layout, labels, progress bar, and buttons.

- `setTheme(darkmode)`: This method sets the theme of the widget based on the provided `darkmode` parameter. It adjusts the background and title colors accordingly.

- `uploadImage()`: This method is triggered when the "Upload Image" button is clicked. It opens a file dialog for selecting an image file and then proceeds to process and display the selected image. It creates a separate thread, `InterrogationThread`, to perform the image analysis asynchronously.

- `updateProgress(progress)`: This method updates the progress bar with the provided `progress` value. It also processes pending events to keep the UI responsive.

- `updateTextLabel(result)`: This method updates the text label with the provided `result` string.

- `convert_cv2_to_qimage(cv2_img)`: This method converts a given OpenCV image (`cv2_img`) to a QImage.

- `exportEmotions()`: This method is triggered when the "Export Data" button is clicked. It opens a file dialog for specifying the export file path and then proceeds to export the detected emotions data to a CSV file.

- `exportEmotionsData(file_path)`: This method exports the detected emotions data to a CSV file at the specified `file_path`. It writes the emotions and their corresponding values to the CSV file.

- `display_frame(image_path)`: This method displays the selected image in the widget. It utilizes the OpenCV library and MediaPipe face detection to detect faces in the image. It also utilizes the FER model to detect emotions and generates a pie chart to visualize the detected emotions. The detected emotions are displayed as text labels and rectangles around the faces in the image.

- `get_emotion_color(emotion)`: This method returns the color and emoji representation for a given `emotion`.

- `update_chart_title(emotion)`: This method updates the chart title with the detected emotion, color, and emoji representation.

- `InterrogationThread`: This class is a QThread subclass responsible for running the image analysis in a separate thread. It uses TensorFlow GPU memory growth for efficient processing. The `run()` method performs the interrogation using the `Interrogator` class from the `clip_interrogator` module and emits signals to indicate progress and result obtained.

The `ImageUploaderWidget` class provides a user-friendly interface for uploading images, analyzing emotions, and visualizing the results. It can be integrated into an application to enhance its functionality.

The `VideoUploadWidget` class in `videoUpload.py` provides functionality for uploading and analyzing videos. It utilizes various Qt widgets and integrates with other modules and libraries to process and display video data.

The class includes the following features:

- `initUI():` This method initializes the user interface of the widget. It sets up the layout, labels, video player, slider, buttons, and other necessary components.
- `setTheme(darkmode):` This method sets the theme of the widget based on the provided darkmode parameter. It adjusts the background and title colors accordingly.
- `uploadVideo():` This method is triggered when the "Upload Video" button is clicked. It opens a file dialog for selecting a video file and then proceeds to process and display the selected video. It creates a separate thread, FrameAnalysisThread, to perform frame analysis asynchronously.
- `analyze_frame(frame, current_frame, total_frames):` This method is responsible for analyzing each frame of the uploaded video. It takes a frame, the current frame number, and the total number of frames as input. It utilizes the analyze_frame function to perform the analysis and updates the frame list with the analyzed frames.
- `interrogateStuff():` This method is triggered when the "Interrogate" button is clicked. It initiates the interrogation process for the paused frame. It creates a separate thread, InterrogationThread, to perform the interrogation asynchronously.
- `updateProgress(progress):` This method updates the progress bar with the provided progress value and processes pending events to keep the UI responsive.
- `updateTextLabel(result):` This method updates the description label with the provided result string.
- `setStuffEnabled(isEnabled):` This method enables or disables various UI elements based on the provided isEnabled parameter.
- `update_slider_position(position):` This method updates the position of the slider based on the current position of the video player.
- `update_slider_range(duration):` This method updates the range of the slider based on the duration of the video.
- `display_frames(frame_list):` This method displays the frames in the frame list within the frame list widget. It utilizes Qt widgets to organize and display the frames.
- `merge_frames():` This method merges the analyzed frames into a video file and plays the resulting video. It saves the video as "output_video.avi" and utilizes OpenCV's VideoWriter to write the frames into the video file.
- `InterrogationThread:` This class is a QThread subclass responsible for running the image analysis in a separate thread. It utilizes TensorFlow GPU memory growth for efficient processing. The run() method performs the interrogation using the Interrogator class from the clip_interrogator module and emits signals to indicate progress and result obtained.
- `FrameAnalysisThread:` This class is a QThread subclass responsible for running the frame analysis in a separate thread. It analyzes each frame of the uploaded video using the analyze_frame() method and updates the frame list.
- `get_emotion_color(emotion):` This method returns the color and emoji representation for a given emotion.

The VideoUploadWidget class provides a user-friendly interface for uploading videos, analyzing frames, interrogating frames for emotions, and visualizing the results. It can be integrated into an application to enhance its functionality.


The `FrameListWidget` class in `frameWidget.py` provides functionality for displaying a scrollable list of frames and navigating between them. It utilizes Qt widgets such as `QLabel`, `QHBoxLayout`, `QScrollArea`, and `QWidget` to organize and display the frames.

The class includes the following features:

- `display_frames(frame_list)`: This method takes a list of frames as input and displays them as thumbnails in the frame list widget. Each frame is converted to a QImage and scaled to a desired thumbnail size using Qt's image processing capabilities. The thumbnails are then added to the frame list layout.

- `keyPressEvent(event)`: This method overrides the default key press event handling of the QMainWindow. It enables navigation between frames using the left and right arrow keys. When the left arrow key is pressed, it shows the previous frame, and when the right arrow key is pressed, it shows the next frame.

- `show_previous_frame()`: This method decrements the `current_frame_index` if it is greater than 0 and updates the frame label to display the previous frame.

- `scroll_to_frame(value)`: This method updates the `current_frame_index` based on the given value and scrolls the frame widget to the corresponding frame's position.

- `show_next_frame()`: This method increments the `current_frame_index` if it is less than the number of frames in the frame list and updates the frame label to display the next frame.

- `update_frame_label()`: This method updates the frame label to display the currently selected frame. It retrieves the image data from the frame list and converts it to a QPixmap to set as the frame label's pixmap.

The `FrameListWidget` class provides an interactive and user-friendly way to navigate through the frames in the application. It is integrated into the main window's layout to complement the camera widget and enhance the overall user experience.

## FER MODEL 

![image](https://github.com/TheSaucese/hizennberg/assets/88286462/881af05c-554e-404b-a418-c2857d7c562c)

The Facial Emotion Recognition (FER) system is a comprehensive solution for analyzing facial expressions in images or videos and classifying them into different emotions. It encompasses several components and functions to achieve accurate emotion recognition.

1. `__init__`:
   - Initializes the `FER` class instance.
   - It takes several parameters, such as the Haar cascade file path, a flag for using MTCNN for face detection, and parameters related to face detection and classification.
   - It loads the face detector (either Haar cascade classifier or MTCNN) and initializes the emotion classification model.

2. `_initialize_model`:
   - This method initializes the emotion classification model.
   - If `tfserving` is set to `True`, it sets the target size for emotion classification as (64, 64) and assumes the model will be loaded from a TensorFlow Serving server.
   - If `tfserving` is `False`, it loads the emotion classification model from a local Keras model file and sets the target size based on the model's input shape.

3. `_classify_emotions`:
   - This method is responsible for classifying emotions for a given set of gray-scale face images.
   - If `tfserving` is `True`, it sends a POST request to a TensorFlow Serving server for emotion classification.
   - If `tfserving` is `False`, it directly uses the loaded local Keras model for emotion classification.

4. `pad` and `depad`:
   - These methods are used to add padding to an image and remove the added padding, respectively.
   - The `pad` method takes an image and pads it with a constant value based on the mean intensity of the bottom row of the image.
   - The `depad` method removes the added padding from the image.

5. `tosquare`:
   - This method takes a bounding box (x, y, w, h) and converts it into a square by elongating the shorter side.
   - It calculates the difference between the width and height, adjusts the coordinates accordingly, and returns the modified bounding box.

6. `find_faces`:
   - This method detects faces in an image using either the Haar cascade classifier or MTCNN, based on the chosen face detection method during initialization.
   - It takes an image as input and returns a list of bounding boxes (x, y, w, h) for the detected faces.

7. `__apply_offsets`:
   - This method offsets the face coordinates by adding padding before classification.
   - It takes the original face coordinates and adds the specified offsets, accounting for the padding around the face.

8. `_get_labels`:
   - This method returns a dictionary mapping emotion labels to their corresponding index.

9. `detect_emotions`:
   - This method detects emotions for faces in an image.
   - It takes an image and an optional list of face rectangles as input.
   - If face rectangles are not provided, it uses the `find_faces` method to detect faces in the image.
   - It preprocesses the faces, resizes them to the target size, and classifies the emotions using the `_classify_emotions` method.
   - It returns a list of dictionaries, where each dictionary contains the bounding box coordinates and a dictionary of labeled emotions with their scores.

10. `top_emotion`:
    - This method is a convenience wrapper for `detect_emotions` that returns only the top emotion and its score for the first face in the image.
    - It calls `detect_emotions` and extracts the top emotion based on the highest score.

11. `parse_arguments`, `top_emotion`, and `main`:
    - These functions are related to the command-line interface (CLI) functionality of the script.
    - `parse_arguments` uses the `argparse`

 library to parse command-line arguments.
    - `top_emotion` is called in the `main` function and prints the top emotion and its score for the specified input image file.
    - The main block of the script checks if it is being executed directly and, if so, calls the `main` function to run the FER system on the input image.

These functions collectively provide the necessary functionality for face detection and emotion classification using either a Haar cascade classifier or MTCNN for face detection and a pre-trained model for emotion classification.

## BLIP AND CLIP INTERROGATOR 

![image](https://github.com/TheSaucese/hizennberg/assets/88286462/03ad4ba6-19bc-4068-ae05-bb5043e62f43)


the BLIP (Bi-directional Latent Inference for Perceptual Tasks) and CLIP (Contrastive Language-Image Pre-training) models allow users to generate captions for images and perform various forms of text-based image interrogation.

1. `load_clip_model()`: This function loads the CLIP model based on the provided configuration. It initializes label tables for various categories such as artists, flavors, mediums, movements, and trendings. These label tables are used during image interrogation.

2. `chain(phrases, similarity_fn)`: This method takes a list of phrases and a similarity function as input. It iteratively selects the next phrase from the list that maximizes the similarity to the previous phrase, creating a chain of phrases. The similarity function is used to compute the similarity between phrases based on their embeddings or features.

3. `generate_caption(image)`: This function generates a caption for a given PIL image using the BLIP model. It takes the image as input, extracts its features using the CLIP model, and passes the features through the BLIP model to generate a caption.

4. `image_to_features(image)`: This function extracts the features of a given image using the CLIP model. It takes the image as input and passes it through the CLIP model to obtain its features.

5. `interrogate_classic(image)`: This method generates an image interrogation prompt using a classic format. It includes the image caption, artist, trending, movement, and flavor text modifiers. The prompt is constructed by combining these elements in a specific format.

6. `interrogate_fast(image)`: This function generates an image interrogation prompt by appending the top-ranked terms after the image caption. It selects the most relevant terms based on their similarity to the image features and appends them to the caption.

7. `interrogate_negative(image)`: This method generates an image interrogation prompt by chaining together the most dissimilar terms to the image. It iteratively selects the next term that is least similar to the previous terms, creating a chain of dissimilar terms. This method is useful for building negative prompts to pair with positive prompts for image generation.

8. `interrogate(image)`: This is a high-level function that performs image interrogation. It generates multiple prompt candidates using different strategies (caption, classic, fast, and flavor chain) and selects the candidate with the highest similarity to the image features.

9. `label_ranking_table(similarity_fn)`: This function generates a ranking table of labels for a specific category (e.g., artists, flavors, mediums). The ranking is based on the similarity between the labels and the image features, computed using the provided similarity function.

These functions work together to load the models, extract image features, generate captions, and perform image interrogation using different prompt generation strategies.

## Data Collection

The emotion detection model in Hizenn utilizes the Fer2013 dataset, which is a publicly available dataset widely used for facial expression analysis. The Stable Diffusion Prompt Interrogator model uses its own pre-trained models, and further details can be found in the documentation provided by Stablediffusion.

## Results

![image](https://github.com/TheSaucese/hizennberg/assets/88286462/157eb834-6773-44e2-a564-64fcd0344e90)


For emotion detection, the app provides a pie chart illustrating the percentages of each detected emotion, with the highest percentage representing the predicted emotion.

Regarding image description, the app leverages the Stable Diffusion Prompt Interrogator. Further details about the results and performance can be obtained from the respective documentation.

## Discussion

After conducting multiple tests and evaluations, it has been observed that the emotion detection capabilities of the Hizenn app demonstrate a significant improvement compared to existing `public` solutions such as OpenFace. 

This improvement can be attributed to the combined use of advanced techniques such as MTCNN and MediaPipe face detection algorithms, along with the utilization of a well-trained Fer2013 model. The Fer2013 dataset used for training ensures that the model has learned to detect a wide range of emotions accurately.

Moreover, the integration of the Stable Diffusion Prompt Interrogator for image description enhances the overall functionality of the app. The results obtained from the image description feature are highly informative, providing comprehensive and detailed descriptions of the analyzed images.

The app's performance has been optimized for efficient execution on various hardware configurations. Extensive testing on an 8GB VRAM computer with a 6-core AMD CPU running at 4.2GHz has demonstrated its ability to handle the computational demands effectively. The utilization of CUDA and TensorFlow for GPU utilization, along with multithreading, further accelerates the processing speed, allowing users to obtain faster results.

## Conclusion
The Hizenn app presents a user-friendly solution for efficient emotion detection and image description. By leveraging advanced algorithms, well-trained models, and optimized hardware utilization, the app offers accurate results and fast performance. With its intuitive interface and robust functionality, Hizenn empowers users to analyze frames from videos, upload individual images, and utilize real-time camera functionality. The app holds promise for various applications, including sentiment analysis, content moderation, and accessibility assistance

## References

- [MTCNN: Face Detection and Alignment](https://kpzhang93.github.io/MTCNN_face_detection_alignment/)
- [MediaPipe: Face Detection](https://mediapipe.dev/)
- [Fer2013 Dataset](https://github.com/muxspace/facial_expressions)
- [Stable Diffusion Prompt Interrogator](https://www.stablediffusion.com/prompt-interrogator)
- [Pyside6 Documentation](https://doc.qt.io/qtforpython/)
- [TensorFlow](https://www.tensorflow.org/)
- [CUDA](https://developer.nvidia.com/cuda-zone)
