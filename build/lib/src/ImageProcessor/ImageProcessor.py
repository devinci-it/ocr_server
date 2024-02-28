import cv2
import pytesseract


class ImageProcessor:

    """
    ImageProcessor: Class for processing images and extracting text using Optical Character Recognition (OCR).

    Methods:
        - process_and_extract_text(image_path: str) -> str:
            Process the image and extract text.

    Private Methods:
        - _preprocess_image(image_path: str) -> np.ndarray:
            Preprocess the image for better OCR recognition.

        - _extract_text(preprocessed_image: np.ndarray) -> str:
            Extract text from a preprocessed image using pytesseract.
    """

    def process_and_extract_text(self, image_path):
        """
        Process the image and extract text.

        Parameters:
        - image_path (str): Path to the image file.

        Returns:
        - str: Extracted text from the image.
        """
        preprocessed_image = self._preprocess_image(image_path)

        try:
            return self._extract_text(preprocessed_image)

        except Exception as e:
            # Handle general exceptions
            return f"Error processing image: {e}"


    def _preprocess_image(self, image_path):
        """
        Preprocess the image for better OCR recognition.

        Parameters:
        - image_path (str): Path to the image file.

        Returns:
        - np.ndarray: Preprocessed image as a NumPy array.
        """
        try:
            # Read the image using OpenCV
            image = cv2.imread(image_path)

            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply GaussianBlur to reduce noise and improve OCR
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Apply thresholding to improve text visibility
            _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            return thresh
        except Exception as e:
            print(f"Error preprocessing image for OCR: {str(e)}")
            return None

    def _extract_text(self, preprocessed_image):
        """
        Extract text from a preprocessed image using pytesseract.

        Parameters:
        - preprocessed_image (np.ndarray): Preprocessed image.

        Returns:
        - str: Extracted text from the image.
        """
        try:
            # Use pytesseract to extract text
            extracted_text = pytesseract.image_to_string(preprocessed_image, lang='eng')
            return extracted_text
        except Exception as e:
            print(f"Error extracting text from image: {str(e)}")
            return "Error extracting text"


