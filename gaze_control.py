import time, math, platform
from collections import deque
import numpy as np
import cv2 as cv
import mediapipe as mp
import pyautogui

# -------- Valores por defecto (NO se modifican en runtime) --------
DEBUG_DEFAULT = True
GAIN_DEFAULT = 1.20  # sensibilidad
DEADZONE_DEFAULT = 0.015
WINK_THRESH = 0.20
WINK_MIN_FRAMES = 2
DOUBLE_WINK_WINDOW = 0.60
DWELL_ENABLED_DEFAULT = False
DWELL_TIME = 0.70
SCROLL_BAND = 0.08
SCROLL_STEP = 80
FPS_SMOOTH = 0.9
IS_MAC = platform.system() == "Darwin"


# -------- Filtro One-Euro --------
class OneEuro:
    def __init__(self, freq=60.0, min_cutoff=1.0, beta=0.02, dcutoff=1.0):
        self.freq = freq
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.dcutoff = dcutoff
        self.x_prev = None
        self.dx_prev = None
        self.t_prev = None

    def alpha(self, cutoff):
        te = 1.0 / self.freq
        tau = 1.0 / (2 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / te)

    def filt(self, x, t):
        if self.t_prev is None:
            self.t_prev = t
            self.x_prev = x
            self.dx_prev = 0.0
            return x
        self.freq = 1.0 / max(1e-6, t - self.t_prev)
        dx = (x - self.x_prev) * self.freq
        a_d = self.alpha(self.dcutoff)
        dx_hat = a_d * dx + (1 - a_d) * self.dx_prev
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = self.alpha(cutoff)
        x_hat = a * x + (1 - a) * self.x_prev
        self.t_prev = t
        self.x_prev = x_hat
        self.dx_prev = dx_hat
        return x_hat


# -------- MediaPipe --------
mp_face = mp.solutions.face_mesh
LEFT_EYE = [33, 133, 160, 144, 159, 145]
RIGHT_EYE = [263, 362, 387, 373, 386, 374]


def ear(lm, idx):
    p = [np.array([lm[i].x, lm[i].y]) for i in idx]
    v1 = np.linalg.norm(p[2] - p[5])
    v2 = np.linalg.norm(p[3] - p[4])
    h = np.linalg.norm(p[0] - p[1])
    return (v1 + v2) / (2 * h + 1e-6)


# -------- Calibración afín 2D --------
class Calib:
    def __init__(self, screen_w, screen_h):
        self.sw, self.sh = screen_w, screen_h
        self.A = None
        self.samples_src = []
        self.samples_dst = []

    def grid_points(self):
        xs = [int(self.sw * 0.15), int(self.sw * 0.50), int(self.sw * 0.85)]
        ys = [int(self.sh * 0.15), int(self.sh * 0.50), int(self.sh * 0.85)]
        return [(x, y) for y in ys for x in xs]

    def fit(self):
        if len(self.samples_src) < 3:
            self.A = None
            return False
        X = []
        Yx = []
        Yy = []
        for (cx, cy), (px, py) in zip(self.samples_src, self.samples_dst):
            X.append([cx, cy, 1.0])
            Yx.append(px)
            Yy.append(py)
        X = np.array(X)
        Yx = np.array(Yx)
        Yy = np.array(Yy)
        ax, _r, _rk, _s = np.linalg.lstsq(X, Yx, rcond=None)
        ay, _r, _rk, _s = np.linalg.lstsq(X, Yy, rcond=None)
        self.A = np.vstack([ax, ay])
        return True

    def map(self, cx, cy):
        if self.A is None:
            return int(cx * self.sw), int(cy * self.sh)
        v = np.array([cx, cy, 1.0])
        xy = self.A @ v
        return int(np.clip(xy[0], 0, self.sw - 1)), int(np.clip(xy[1], 0, self.sh - 1))


# -------- Acciones --------
def page_forward():
    pyautogui.hotkey("command" if IS_MAC else "alt", "right")


def page_back():
    pyautogui.hotkey("command" if IS_MAC else "alt", "left")


# -------- Principal --------
def main():
    # Warnings de TFLite/XNNPACK que ves en consola son normales.
    pyautogui.FAILSAFE = True
    sw, sh = pyautogui.size()
    calib = Calib(sw, sh)
    filx, fily = OneEuro(min_cutoff=1.2, beta=0.04), OneEuro(min_cutoff=1.2, beta=0.04)

    # Variables **locales** que sí podemos modificar
    debug = DEBUG_DEFAULT
    gain = GAIN_DEFAULT
    deadzone = DEADZONE_DEFAULT
    dwell_enabled = DWELL_ENABLED_DEFAULT

    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara.")

    left_frames = right_frames = 0
    last_left_winks = deque()
    dwell_t0 = None
    last_cx = last_cy = None
    fps = 0.0
    last_fps_t = time.time()
    frames = 0

    with mp_face.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    ) as face:
        mode_calib = False
        targets = []
        target_i = 0
        hold_t0 = None

        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame = cv.flip(frame, 1)
            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            res = face.process(rgb)
            now = time.time()

            if (
                res.multi_face_landmarks
                and len(res.multi_face_landmarks[0].landmark) > 473
            ):
                lm = res.multi_face_landmarks[0].landmark
                cx = (lm[468].x + lm[473].x) / 2.0
                cy = (lm[468].y + lm[473].y) / 2.0

                # Dead-zone
                if last_cx is not None and last_cy is not None:
                    if abs(cx - last_cx) < deadzone and abs(cy - last_cy) < deadzone:
                        cx, cy = last_cx, last_cy
                last_cx, last_cy = cx, cy

                # Filtro
                fx = filx.filt(cx, now)
                fy = fily.filt(cy, now)

                # Mapeo
                gx = np.clip(fx * gain, 0.0, 1.0)
                gy = np.clip(fy * gain, 0.0, 1.0)
                x, y = calib.map(gx, gy)
                pyautogui.moveTo(x, y, _pause=False)

                # Gestos (guiños)
                ear_l = ear(lm, LEFT_EYE)
                ear_r = ear(lm, RIGHT_EYE)

                if ear_l < WINK_THRESH and ear_r >= WINK_THRESH:
                    left_frames += 1
                else:
                    if left_frames >= WINK_MIN_FRAMES:
                        pyautogui.click(x, y)
                        t = time.time()
                        last_left_winks.append(t)
                        while (
                            last_left_winks
                            and t - last_left_winks[0] > DOUBLE_WINK_WINDOW
                        ):
                            last_left_winks.popleft()
                        if len(last_left_winks) >= 2:
                            page_forward()
                            last_left_winks.clear()
                    left_frames = 0

                if ear_r < WINK_THRESH and ear_l >= WINK_THRESH:
                    right_frames += 1
                else:
                    if right_frames >= WINK_MIN_FRAMES:
                        page_back()
                    right_frames = 0

                # Dwell click
                if dwell_enabled:
                    nx, ny = gx, gy
                    if dwell_t0 is None:
                        dwell_t0 = now
                        ref = (nx, ny)
                    else:
                        if abs(nx - ref[0]) < deadzone and abs(ny - ref[1]) < deadzone:
                            if now - dwell_t0 > DWELL_TIME:
                                pyautogui.click(x, y)
                                dwell_t0 = now
                        else:
                            dwell_t0 = now
                            ref = (nx, ny)

                # Scroll por bandas
                if gy < SCROLL_BAND:
                    pyautogui.scroll(SCROLL_STEP)
                elif gy > 1.0 - SCROLL_BAND:
                    pyautogui.scroll(-SCROLL_STEP)

            # Calibración
            if mode_calib:
                if not targets:
                    targets = calib.grid_points()
                    target_i = 0
                    hold_t0 = None
                tx, ty = targets[target_i]
                cv.circle(frame, (tx, ty), 14, (0, 255, 255), 2)
                cv.circle(frame, (tx, ty), 4, (0, 255, 255), -1)
                if (
                    res.multi_face_landmarks
                    and len(res.multi_face_landmarks[0].landmark) > 473
                ):
                    lm = res.multi_face_landmarks[0].landmark
                    cx = (lm[468].x + lm[473].x) / 2.0
                    cy = (lm[468].y + lm[473].y) / 2.0
                    if hold_t0 is None:
                        hold_t0 = now
                    if now - hold_t0 >= 0.4:
                        calib.samples_src.append((cx, cy))
                        calib.samples_dst.append((tx, ty))
                        target_i += 1
                        hold_t0 = None
                        if target_i >= len(targets):
                            mode_calib = False
                            print(
                                "Calibración:", "OK" if calib.fit() else "Insuficiente"
                            )
                else:
                    hold_t0 = None

            # HUD
            frames += 1
            if frames % 10 == 0:
                dt = time.time() - last_fps_t
                fps = FPS_SMOOTH * fps + (1 - FPS_SMOOTH) * (10.0 / dt)
                last_fps_t = time.time()
            if debug:
                text = f"FPS:{fps:.1f} GAIN:{gain:.2f} DZ:{deadzone:.3f} Dwell:{'On' if dwell_enabled else 'Off'}"
                cv.putText(
                    frame, text, (10, 24), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
                )
                cv.putText(
                    frame,
                    "[c] calibrar  [r] reset  [d] debug  [+/-] ganancia  [g] dwell  [q] salir",
                    (10, sh - 12),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                )

            cv.imshow("Gaze Control", frame)
            k = cv.waitKey(1) & 0xFF
            if k == ord("q"):
                break
            elif k == ord("d"):
                debug = not debug
            elif k == ord("c"):
                mode_calib = True
                calib.samples_src.clear()
                calib.samples_dst.clear()
                targets = []
                target_i = 0
            elif k == ord("r"):
                calib.A = None
            elif k in (ord("+"), ord("=")):
                gain = min(2.5, gain + 0.05)
            elif k == ord("-"):
                gain = max(0.5, gain - 0.05)
            elif k == ord("g"):
                dwell_enabled = not dwell_enabled

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
