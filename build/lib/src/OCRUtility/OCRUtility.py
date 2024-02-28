import hashlib
import os
import zipfile
from datetime import datetime

from PIL import Image
from slugify import slugify


class OCRUtility:

    """
    OCRUtility: Utility class for Optical Character Recognition (OCR) operations.

    Methods:
        - resize_photo(photo_path: str, output_path: str, size: tuple = (1920, 1080)) -> None:
            Resize a photo to the specified dimensions.

        - sanitize_name(name: str) -> str:
            Sanitize a name by removing special characters and spaces.

        - save_uploaded_file(file: FileStorage, upload_directory: str, token: str) -> str:
            Save an uploaded file to the specified directory with organized storage.

    Example Usage:
        ocr_utility = OCRUtility()
        ocr_utility.resize_photo('input_photo.jpg', 'resized_photo.jpg')
        sanitized_name = ocr_utility.sanitize_name('Hello World!')
        saved_path = ocr_utility.save_uploaded_file(uploaded_file, 'uploads', 'example_token')
    """


    @staticmethod
    def resize_photo(photo_path, output_path, size=(1920, 1080)):
        """
        Resize a photo to the specified dimensions.

        Parameters:
        - photo_path (str): Path to the input photo.
        - output_path (str): Path to save the resized photo.
        - size (tuple): Desired dimensions (width, height).

        Returns:
        - None
        """
        try:
            image = Image.open(photo_path)
            rgb_image = image.convert('RGB')
            resized_image = rgb_image.resize(size)
            resized_image.save(output_path)
        except Exception as e:
            print(f"Error resizing photo: {e}")

    @staticmethod
    def sanitize_name(name):
        """
        Sanitize a name by removing special characters and spaces.

        Parameters:
        - name (str): Input name to be sanitized.

        Returns:
        - str: Sanitized name.
        """
        return slugify(name)

    @staticmethod
    def save_uploaded_file(file, upload_directory, token):
        """
        Save an uploaded file to the specified directory with organized storage.

        Parameters:
        - file (FileStorage): Uploaded file object.
        - upload_directory (str): Directory to save the file.
        - token (str): Token used for the request.

        Returns:
        - str: Path to the saved file.
        """
        try:
            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)

            # Get the original file name
            original_filename = file.filename

            # Generate a hash of the original image
            hash_object = hashlib.md5(file.read())
            hash_value = hash_object.hexdigest()

            # Create a unique filename based on date, hash, and token
            current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            unique_filename = f"{current_date}_{hash_value}_{token}.zip"

            # Create a directory based on the current month
            month_directory = os.path.join(upload_directory, datetime.now().strftime("%Y-%m"))
            if not os.path.exists(month_directory):
                os.makedirs(month_directory)

            # Create a ZIP file and save the processed image
            # processed_image_path = 'path_to_processed_image.jpg'  # Replace with the actual path
            zip_file_path = os.path.join(month_directory, unique_filename)
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                zipf.writestr('original_filename.txt', original_filename)
                zipf.writestr('hash_value.txt', hash_value)
                # zipf.write(processed_image_path, 'processed_image.jpg')

            return zip_file_path
        except Exception as e:
            print(f"Error saving uploaded file: {e}")
            return None
