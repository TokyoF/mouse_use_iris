import time
import cv2 as cv
import mediapipe as mp

mp_face = mp.solutions.face_mesh


def draw_point(img, lm, idx, color=(0, 255, 0), r=2):
    h, w = img.shape[:2]
    x, y = int(lm[idx].x * w), int(lm[idx].y * h)
    cv.circle(img, (x, y), r, color, -1)


def main():
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)  # Windows: CAP_DSHOW ayuda con webcams
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara")

    with mp_face.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,  # activa puntos de iris
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    ) as face:
        t0, frames = time.time(), 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame = cv.flip(frame, 1)
            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            res = face.process(rgb)

            if res.multi_face_landmarks:
                lm = res.multi_face_landmarks[0].landmark
                # Iris (centros aproximados): 468 (izq), 473 (der)
                if len(lm) > 473:
                    draw_point(frame, lm, 468, (0, 255, 0), 3)  # iris izq
                    draw_point(frame, lm, 473, (0, 255, 0), 3)  # iris der
                # Unos puntos del contorno de ojos para referencia
                for i in (33, 133, 263, 362):
                    draw_point(frame, lm, i, (255, 0, 0), 2)

            frames += 1
            if frames % 15 == 0:
                fps = 15 / (time.time() - t0)
                t0 = time.time()
                cv.putText(
                    frame,
                    f"FPS: {fps:.1f}",
                    (10, 25),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

            cv.imshow("Prueba Iris (q para salir)", frame)
            if (cv.waitKey(1) & 0xFF) == ord("q"):
                break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
