from pathlib import Path

import cv2
import numpy as np


FRAME_SIZE = 640
FPS = 30
DURATION_SECONDS = 10
VIDEO_PATH = Path(__file__).with_name("late_to_class.mp4")

FLOOR = (139, 176, 205)
FLOOR_LIGHT = (151, 190, 218)
WALL = (78, 105, 135)
WALL_LIGHT = (99, 128, 158)
WOOD = (73, 119, 174)
WOOD_LIGHT = (102, 150, 204)
INK = (41, 46, 53)
SHIRTS = [
    (75, 121, 170), (88, 142, 187), (93, 105, 151), (112, 137, 163),
    (66, 112, 145), (124, 153, 184), (82, 98, 130), (110, 126, 158),
]
SKINS = [(170, 193, 220), (145, 177, 209), (188, 204, 224), (158, 185, 215)]


def project(point: tuple[float, float, float]) -> tuple[int, int]:
    x, y, z = point
    return (
        int(round(320 + (x - 5) * 34 - (y - 6) * 25)),
        int(round(301 + (x - 5) * 13 - (y - 6) * 17 - z * 35)),
    )


def polygon(
    frame: np.ndarray,
    points: list[tuple[float, float, float]],
    color: tuple[int, int, int],
    outline: tuple[int, int, int] | None = None,
) -> None:
    projected = np.array([project(point) for point in points], dtype=np.int32)
    cv2.fillConvexPoly(frame, projected, color, cv2.LINE_AA)
    if outline is not None:
        cv2.polylines(frame, [projected], True, outline, 1, cv2.LINE_AA)


def line3d(
    frame: np.ndarray,
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    color: tuple[int, int, int],
    thickness: int = 2,
) -> None:
    cv2.line(frame, project(start), project(end), color, thickness, cv2.LINE_AA)


def ellipsoid(
    frame: np.ndarray,
    center: tuple[float, float, float],
    axes: tuple[int, int],
    color: tuple[int, int, int],
    highlight: tuple[int, int, int] | None = None,
) -> None:
    px, py = project(center)
    cv2.ellipse(frame, (px + 2, py + 3), axes, -12, 0, 360, (48, 58, 72), -1, cv2.LINE_AA)
    cv2.ellipse(frame, (px, py), axes, -12, 0, 360, color, -1, cv2.LINE_AA)
    if highlight is not None:
        cv2.ellipse(
            frame, (px - axes[0] // 3, py - axes[1] // 3),
            (max(2, axes[0] // 3), max(2, axes[1] // 4)),
            -12, 190, 340, highlight, 2, cv2.LINE_AA,
        )


def draw_room() -> np.ndarray:
    frame = np.full((FRAME_SIZE, FRAME_SIZE, 3), (205, 222, 236), dtype=np.uint8)

    # Open-front, isometric room shell and warm timber floor.
    polygon(frame, [(0, 0, 0), (10, 0, 0), (10, 12, 0), (0, 12, 0)], FLOOR)
    for y in np.arange(0.35, 12, 0.42):
        line3d(frame, (0.1, float(y), 0.015), (9.9, float(y), 0.015), FLOOR_LIGHT, 1)
    for x in np.arange(0.25, 10, 1.0):
        line3d(frame, (float(x), 0.1, 0.015), (float(x), 11.9, 0.015), (130, 168, 198), 1)

    polygon(frame, [(0, 12, 0), (10, 12, 0), (10, 12, 5.1), (0, 12, 5.1)], WALL)
    polygon(frame, [(0, 0, 0), (0, 12, 0), (0, 12, 3.2), (0, 0, 3.2)], (88, 119, 150))
    polygon(frame, [(10, 0, 0), (10, 12, 0), (10, 12, 3.2), (10, 0, 3.2)], (72, 99, 129))

    # Timber panel seams and wall trim add depth without obscuring the open room.
    for x in range(0, 11):
        line3d(frame, (float(x), 11.98, 0.2), (float(x), 11.98, 4.9), (87, 113, 142), 1)
    for z in (0.28, 0.5):
        line3d(frame, (0, 0, z), (0, 12, z), WALL_LIGHT, 3)
        line3d(frame, (10, 0, z), (10, 12, z), (91, 116, 144), 3)

    # Chalkboard and a simple diagram (no words or captions).
    polygon(frame, [(2.1, 11.91, 2.0), (7.9, 11.91, 2.0), (7.9, 11.91, 4.3), (2.1, 11.91, 4.3)], (57, 83, 81), (130, 151, 160))
    line3d(frame, (2.8, 11.88, 2.75), (4.0, 11.88, 2.75), (220, 224, 210), 2)
    line3d(frame, (4.0, 11.88, 2.75), (5.0, 11.88, 3.35), (220, 224, 210), 2)
    ellipsoid(frame, (5.0, 11.86, 3.35), (4, 4), (220, 224, 210))
    ellipsoid(frame, (6.5, 11.86, 3.2), (20, 20), (200, 211, 199))
    line3d(frame, (6.5, 11.86, 3.2), (6.5, 11.86, 3.85), (200, 211, 199), 2)

    # Front door opening, with the door visibly swinging as the student enters.
    for x in (4.15, 5.85):
        line3d(frame, (x, 0, 0), (x, 0, 2.65), (74, 84, 96), 7)
    line3d(frame, (4.15, 0, 2.65), (5.85, 0, 2.65), (74, 84, 96), 7)
    polygon(frame, [(4.15, 0, 0), (5.85, 0, 0), (5.85, 0.08, 0.08), (4.15, 0.08, 0.08)], WOOD_LIGHT)

    # Narrow side windows catch the warm afternoon light.
    for side in (0, 10):
        for y in (4.1, 7.7):
            polygon(
                frame,
                [(side, y, 1.1), (side, y + 1.55, 1.1), (side, y + 1.55, 2.55), (side, y, 2.55)],
                (137, 176, 192),
                (168, 190, 198),
            )
            line3d(frame, (side, y + 0.77, 1.1), (side, y + 0.77, 2.55), (182, 190, 178), 2)
            line3d(frame, (side, y, 1.82), (side, y + 1.55, 1.82), (182, 190, 178), 2)
    return frame


def draw_desk(frame: np.ndarray, x: float, y: float, index: int, watching: bool) -> None:
    width, depth = 0.94, 0.72
    ztop = 0.91
    for dx in (-width / 2 + 0.1, width / 2 - 0.1):
        for dy in (-depth / 2 + 0.1, depth / 2 - 0.1):
            line3d(frame, (x + dx, y + dy, 0.08), (x + dx, y + dy, ztop), (66, 82, 100), 3)
    polygon(
        frame,
        [(x - width / 2, y - depth / 2, ztop), (x + width / 2, y - depth / 2, ztop),
         (x + width / 2, y + depth / 2, ztop), (x - width / 2, y + depth / 2, ztop)],
        WOOD,
        (62, 94, 128),
    )
    polygon(
        frame,
        [(x - width / 2, y - depth / 2, ztop), (x + width / 2, y - depth / 2, ztop),
         (x + width / 2, y - depth / 2, ztop - 0.12), (x - width / 2, y - depth / 2, ztop - 0.12)],
        (55, 92, 137),
    )
    polygon(
        frame,
        [(x - 0.19, y - 0.17, ztop + 0.025), (x + 0.19, y - 0.17, ztop + 0.025),
         (x + 0.19, y + 0.16, ztop + 0.025), (x - 0.19, y + 0.16, ztop + 0.025)],
        (222, 215, 195),
    )
    for offset in (-0.09, 0.0, 0.09):
        line3d(frame, (x - 0.13, y + offset, ztop + 0.035), (x + 0.12, y + offset, ztop + 0.035), (172, 167, 153), 1)

    shirt = SHIRTS[index % len(SHIRTS)]
    skin = SKINS[index % len(SKINS)]
    hair = (48 + index % 4 * 7, 56 + index % 3 * 9, 68 + index % 5 * 7)
    body_y = y - 0.62
    ellipsoid(frame, (x, body_y, 0.75), (12, 18), shirt, (126, 165, 201))
    ellipsoid(frame, (x, y - 0.2, 0.88), (7, 9), skin, (211, 218, 224))
    ellipsoid(frame, (x, y - 0.19, 0.96), (7, 5), hair)
    face = project((x, y - 0.13, 0.89))
    cv2.circle(frame, face, 1, INK, -1, cv2.LINE_AA)
    if watching:
        line3d(frame, (x, y - 0.17, 0.86), (x + (0.13 if x < 5 else -0.13), y - 0.17, 0.86), skin, 2)


def draw_character(
    frame: np.ndarray,
    x: float,
    y: float,
    *,
    teacher: bool = False,
    pose: str = "walk",
    time: float = 0.0,
) -> None:
    shirt = (84, 112, 151) if teacher else (84, 130, 183)
    skin = (173, 193, 215)
    hair = (48, 56, 68)
    z = 0.12
    ellipsoid(frame, (x, y, 0.05), (13 if teacher else 12, 7), (75, 80, 88))
    ellipsoid(frame, (x, y, z + 0.61), (12 if teacher else 11, 19), shirt, (133, 162, 188))
    ellipsoid(frame, (x, y - 0.03, z + 1.27), (9, 11), skin, (210, 218, 225))
    ellipsoid(frame, (x, y - 0.03, z + 1.34), (9, 6), hair)

    # The teacher's changing arm pose carries the meaning without dialogue.
    if teacher and pose == "point":
        line3d(frame, (x - 0.1, y - 0.08, z + 0.75), (x - 0.75, y - 0.1, z + 1.15), skin, 5)
        line3d(frame, (x + 0.1, y - 0.08, z + 0.75), (x + 0.65, y - 0.3, z + 1.8), skin, 5)
        line3d(frame, (x + 0.65, y - 0.3, z + 1.8), (x + 0.7, y - 0.85, z + 2.25), skin, 4)
    elif teacher:
        line3d(frame, (x - 0.1, y - 0.08, z + 0.75), (x - 0.55, y + 0.1, z + 1.5), skin, 5)
        line3d(frame, (x - 0.55, y + 0.1, z + 1.5), (x - 0.9, y + 0.25, z + 1.85), skin, 4)
        line3d(frame, (x + 0.1, y - 0.08, z + 0.75), (x + 0.6, y - 0.1, z + 1.1), skin, 5)
    elif pose == "apology":
        line3d(frame, (x - 0.1, y - 0.08, z + 0.75), (x - 0.45, y - 0.1, z + 1.05), skin, 4)
        line3d(frame, (x + 0.1, y - 0.08, z + 0.75), (x + 0.48, y - 0.15, z + 1.45), skin, 4)
        ellipsoid(frame, (x + 0.48, y - 0.15, z + 1.47), (3, 4), skin)
    else:
        step = 0.25 * np.sin(time * 10)
        line3d(frame, (x - 0.08, y - 0.05, z + 0.5), (x - 0.16 + step, y - 0.05, z + 0.08), (61, 72, 91), 4)
        line3d(frame, (x + 0.08, y - 0.05, z + 0.5), (x + 0.16 - step, y - 0.05, z + 0.08), (61, 72, 91), 4)
        line3d(frame, (x - 0.1, y - 0.08, z + 0.75), (x - 0.42, y - 0.08, z + 0.3 + step), skin, 4)
        line3d(frame, (x + 0.1, y - 0.08, z + 0.75), (x + 0.4, y - 0.08, z + 0.32 - step), skin, 4)


def make_frame(time: float) -> np.ndarray:
    frame = draw_room()

    # Render rows from the rear toward the front so nearer furniture overlaps naturally.
    desks = [
        (x, y, row * 6 + col)
        for row, y in enumerate((8.7, 7.0, 5.3, 3.6))
        for col, x in enumerate((1.2, 2.45, 3.7, 6.3, 7.55, 8.8))
    ]
    watching = 4.0 <= time < 8.7
    for x, y, index in sorted(desks, key=lambda desk: -desk[1]):
        draw_desk(frame, x, y, index, watching)

    if time < 4.9 or time >= 7.8:
        teacher_pose = "explain"
    else:
        teacher_pose = "point"
    draw_character(frame, 5.0, 10.2, teacher=True, pose=teacher_pose, time=time)

    if 1.4 <= time < 9.3:
        if time < 3.8:
            student_y = float(np.interp(time, (1.4, 3.8), (-0.7, 4.5)))
            student_pose = "walk"
        elif time < 4.9:
            student_y, student_pose = 4.5, "apology"
        elif time < 7.8:
            student_y, student_pose = 4.5, "apology"
        else:
            student_y = float(np.interp(time, (7.8, 9.3), (4.5, -0.8)))
            student_pose = "walk"
        draw_character(frame, 5.0, student_y, pose=student_pose, time=time)

    # A swinging door leaf and warm interior light make the entrance readable.
    if 1.15 <= time < 9.3:
        opening = min(1.0, (time - 1.15) / 0.45, (9.3 - time) / 0.45)
        opening = max(0.0, opening)
        door_end = (5.85, 1.15 * opening, 2.45 * opening)
        line3d(frame, (4.15, 0, 0.05), door_end, (93, 129, 169), 5)
        ellipsoid(frame, (5.3, -0.1, 0.05), (8, 5), (102, 131, 159))
    return frame


writer = cv2.VideoWriter(
    str(VIDEO_PATH),
    cv2.VideoWriter_fourcc(*"mp4v"),
    FPS,
    (FRAME_SIZE, FRAME_SIZE),
)
if not writer.isOpened():
    raise RuntimeError(f"Could not create video: {VIDEO_PATH}")

try:
    for frame_number in range(FPS * DURATION_SECONDS):
        writer.write(make_frame(frame_number / FPS))
finally:
    writer.release()

print(f"Created 3D classroom video: {VIDEO_PATH}")
