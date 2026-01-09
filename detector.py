import cv2
import numpy as np
import base64
from skimage.metrics import structural_similarity as ssim

FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


class DeepfakeAnalyzer:

    def extract_face(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return None

        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        x, y, w, h = faces[0]

        pad = int(0.12 * w)
        x1 = max(x + pad, 0)
        y1 = max(y + pad, 0)
        x2 = min(x + w - pad, img.shape[1])
        y2 = min(y + h - pad, img.shape[0])

        face = img[y1:y2, x1:x2]
        return cv2.resize(face, (256, 256))

    def face_to_base64(self, face):
        _, buffer = cv2.imencode(".jpg", face)
        return base64.b64encode(buffer).decode("utf-8")

    def sharpness(self, gray):
        return cv2.Laplacian(gray, cv2.CV_64F).var()

    def edge_density(self, gray):
        edges = cv2.Canny(gray, 100, 200)
        return np.sum(edges > 0) / edges.size

    def color_histogram_distance(self, face1, face2):
        hsv1 = cv2.cvtColor(face1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(face2, cv2.COLOR_BGR2HSV)

        h1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
        h2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])

        cv2.normalize(h1, h1)
        cv2.normalize(h2, h2)

        return cv2.compareHist(h1, h2, cv2.HISTCMP_BHATTACHARYYA)

    def compare_images(self, img1, img2):
        face1 = self.extract_face(img1)
        face2 = self.extract_face(img2)

        if face1 is None or face2 is None:
            return {"error": "Face not detected in one or both images"}

        gray1 = cv2.cvtColor(face1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(face2, cv2.COLOR_BGR2GRAY)

        ssim_score, _ = ssim(gray1, gray2, full=True)
        similarity_percent = round(ssim_score * 100, 2)

        sharp1 = self.sharpness(gray1)
        sharp2 = self.sharpness(gray2)

        edge1 = self.edge_density(gray1)
        edge2 = self.edge_density(gray2)

        color_diff = self.color_histogram_distance(face1, face2)

        # 🔬 Forensic Risk Fusion
        risk = 0

        if ssim_score < 0.80:
            risk += 35
        elif ssim_score < 0.88:
            risk += 20

        if abs(sharp1 - sharp2) > 120:
            risk += 25

        if abs(edge1 - edge2) > 0.04:
            risk += 20

        if color_diff > 0.30:
            risk += 20

        risk = min(risk, 100)

        return {
            "structural_similarity_%": similarity_percent,
            "sharpness_original": round(sharp1, 2),
            "sharpness_suspected": round(sharp2, 2),
            "edge_density_original": round(edge1, 4),
            "edge_density_suspected": round(edge2, 4),
            "color_difference_score": round(color_diff, 3),
            "deepfake_risk_%": risk,
            "interpretation": (
                "Likely Manipulated / Face Swap"
                if risk >= 50
                else "Likely Same Real Face"
            ),
            "debug_faces": {
                "original_face_base64": self.face_to_base64(face1),
                "suspected_face_base64": self.face_to_base64(face2)
            }
        }
