import cv2 as cv
import mediapipe as mp
import pyautogui

mp_face = mp.solutions.face_mesh


class EMA:
    def __init__(self, alpha=0.7):
        self.a, self.x, self.y = alpha, None, None

    def upd(self, x, y):
        if self.x is None:
            self.x, self.y = x, y
        else:
            self.x = self.a * self.x + (1 - self.a) * x
            self.y = self.a * self.y + (1 - self.a) * y
        return self.x, self.y


def main():
    pyautogui.FAILSAFE = True
    screen_w, screen_h = pyautogui.size()
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    ema = EMA(alpha=0.75)

    with mp_face.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    ) as face:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame = cv.flip(frame, 1)
            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            res = face.process(rgb)
            if (
                res.multi_face_landmarks
                and len(res.multi_face_landmarks[0].landmark) > 473
            ):
                lm = res.multi_face_landmarks[0].landmark
                cx = (lm[468].x + lm[473].x) / 2
                cy = (lm[468].y + lm[473].y) / 2
                sx, sy = ema.upd(cx, cy)
                x = max(0, min(screen_w - 1, int(sx * screen_w)))
                y = max(0, min(screen_h - 1, int(sy * screen_h)))
                pyautogui.moveTo(x, y, _pause=False)

            cv.imshow("Mouse por Iris (q para salir)", frame)
            if (cv.waitKey(1) & 0xFF) == ord("q"):
                break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
