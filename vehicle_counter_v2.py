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
output = cv2.VideoWriter("output_tracker_with_area.mp4", fourcc, 30.0, (1280,720))


# Open the video file
video_path = "input_video.mp4"
cap = cv2.VideoCapture(video_path)

# Define the areas
areas = {
    "Area A": (40, 220, 450, 500),
    "Area B": (510, 220, 240, 500),
    "Area C": (780, 220, 480, 500),
}

# Initialize the counters and the track history
counters = defaultdict(int)
track_history = defaultdict(set)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, tracker="botsort.yaml")
        # tracker : botsort.yaml / bytetrack.yaml
        # Get the boxes and track IDs
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()

        # Check if each box is in any of the areas and update the track history
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            for area_name, (ax, ay, aw, ah) in areas.items():
                if ax < x < ax + aw and ay < y < ay + ah:
                    if area_name not in track_history[track_id]:
                        counters[area_name] += 1
                        track_history[track_id].add(area_name)

        # Visualize the results on the frame
        annotated_frame = results[0].plot(conf=False, labels=False, line_width=1, font_size=3, probs=False)

        # Draw the areas on the frame and write the area names
        for area_name, (ax, ay, aw, ah) in areas.items():
            cv2.rectangle(annotated_frame, (ax, ay), (ax + aw, ay + ah), (255, 0, 0), 2)
            # Define the text and get its size
            text = area_name.replace("Area ", "")
            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

            # Define the rectangle position and size
            rect_x, rect_y = ax, ay - 10 - text_height
            rect_width, rect_height = text_width, text_height

            # Draw the rectangle (in this case, the color is blue)
            cv2.rectangle(annotated_frame, (rect_x-2, rect_y-2), (rect_x + rect_width+2, rect_y + rect_height+2), (255, 0, 0),-1)

            # Write the text on top of the rectangle
            cv2.putText(annotated_frame, text, (ax, ay - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        # Write the counts on the frame
        for i, (area_name, count) in enumerate(counters.items()):
            cv2.putText(annotated_frame, f"{area_name} Count: {count}", (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

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