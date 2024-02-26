# Vehicle Traffic Counter

This project aims to count vehicles passing through a road. It processes traffic camera footage taken from YouTube using the OpenCV library and a trained YOLOV8 model to count the vehicles passing through the road in the video.

You can access the source video from this [YouTube Link](https://www.youtube.com/watch?v=MNn9qKG2UFI&list=PLcQZGj9lFR7y5WikozDSrdk6UCtAnM9mB).
The project utilizes the `yolov8n` model for vehicle detection. Additionally, it employs the `<botsort.yaml>` tracker type for tracking purposes.

The project has 2 different versions.

## Version 1
Version 1 displays the total number of vehicles passing through the road in the video as well as the number of vehicles detected in real-time.

### Outputs
#### v1_outputs:
![V1_11](output_tracker11.gif)
![V1_12](output_tracker12.gif)
![V1_21](output_tracker21.gif)
![V1_22](output_tracker22.gif)

## Version 2
Version 2 creates 3 different areas for 3 different roads and counts the total number of vehicles passing through these areas.

### Outputs
#### v2_outputs:
![V2_1](output_tracker_with_area11.gif)
![V2_1](output_tracker_with_area12.gif)
