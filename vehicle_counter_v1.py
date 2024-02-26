import cv2
from ultralytics import YOLO
from collections import defaultdict


# Youtube video
'''
from pytube import YouTube

youtube_video = YouTube("https://www.youtube.com/watch?v=MNn9qKG2UFI&list=PLcQZGj9lFR7y5WikozDSrdk6UCtAnM9mB")
video = youtube_video.streams.get_highest_resolution()
video.download(filename="input_video.mp4")
'''

# Video capturing

input_video = cv2.VideoCapture("input_video.mp4")



# Video size info

width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("width", width)
print("height", height)

# Codec and FPS info
fourcc = int(input_video.get(cv2.CAP_PROP_FOURCC))
fourcc_str = chr(fourcc & 0xFF) + chr((fourcc >> 8) & 0xFF) + chr((fourcc >> 16) & 0xFF) + chr((fourcc >> 24) & 0xFF)
fps = input_video.get(cv2.CAP_PROP_FPS)


print("FourCC int:", fourcc)
print("FourCC :", fourcc_str)
print("FPS: ", fps)

'''
# Video Resize

new_width = HOLD
new_height = HOLD          
resized_video = cv2.VideoWriter("resized_video.mp4", fourcc, fps, (new_width, new_height))
cap.release()
'''



# Load the YOLOv8 model
model = YOLO('yolov8n.pt')
# model = 'yolov8n.pt' / 'yolov8l.pt' / 'yolov8s.pt'

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
output = cv2.VideoWriter("output_tracker2.mp4", fourcc, 30.0, (1280,720))

# Open the video file
video_path = "input_video.mp4"
cap = cv2.VideoCapture(video_path)





track_history = defaultdict(lambda: [])

# Loop through the video frames

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True,tracker="botsort.yaml" )
        # tracker : botsort.yaml / bytetrack.yaml
        # Get the boxes and track IDs
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        # Visualize the results on the frame
        annotated_frame = results[0].plot(conf=False, labels=False, line_width=1, font_size=3, probs=False)

        # Plot the tracks
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            track = track_history[track_id]
            track.append((float(x), float(y)))  # x, y center point
            print(track_id)


        vehicle_count = sum(1 for result in results for box in result.boxes if int(box.cls) in [1,2,3,5,6,7])
        total_vehicle_count = len(track_history) + 1
        cv2.putText(annotated_frame, f"Current Detect Vehicle Count: {vehicle_count}", (800, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36, 255, 12), 2)
        cv2.putText(annotated_frame, f"Total Vehicle Count: {total_vehicle_count}", (800, 60), cv2.FONT_HERSHEY_SIMPLEX,0.6, (36, 255, 12), 2)

        output.write(annotated_frame)
        # Display the annotated frame
        cv2.imshow("Vehicle Counter", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()