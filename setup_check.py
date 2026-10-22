from pathlib import Path

import cv2
import numpy as np


frame_size = 640
fps = 30
duration_seconds = 10
square_min = 40
square_max = frame_size - square_min
dot_radius = 9
video_path = Path(__file__).with_name("bouncing_dot.mp4")

rng = np.random.default_rng()
position = rng.uniform(
    square_min + dot_radius,
    square_max - dot_radius,
    size=2,
)
angle = rng.uniform(0, 2 * np.pi)
velocity = 5 * np.array([np.cos(angle), np.sin(angle)])

writer = cv2.VideoWriter(
    str(video_path),
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (frame_size, frame_size),
)
if not writer.isOpened():
    raise RuntimeError(f"Could not create video: {video_path}")

try:
    for _ in range(fps * duration_seconds):
        frame = np.full((frame_size, frame_size, 3), 255, dtype=np.uint8)
        cv2.rectangle(
            frame,
            (square_min, square_min),
            (square_max, square_max),
            (0, 0, 0),
            2,
        )
        cv2.circle(
            frame,
            tuple(np.rint(position).astype(int)),
            dot_radius,
            (0, 0, 255),
            -1,
        )
        writer.write(frame)

        position += velocity
        for axis in range(2):
            minimum = square_min + dot_radius
            maximum = square_max - dot_radius
            if position[axis] < minimum:
                position[axis] = 2 * minimum - position[axis]
                velocity[axis] = abs(velocity[axis])
            elif position[axis] > maximum:
                position[axis] = 2 * maximum - position[axis]
                velocity[axis] = -abs(velocity[axis])
finally:
    writer.release()

print(f"Created video: {video_path}")
