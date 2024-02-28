from setuptools import setup, find_packages

setup(
    name='OCRServer',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'Flask==3.0.2',
        'numpy==1.26.4',
        'opencv-python==4.9.0.80',
        'opencv-python-headless==4.9.0.80',
        'pillow==10.2.0',
        'pytesseract==0.3.10',
        'slugify==0.0.1',
    ],
    entry_points={
        'console_scripts': [
            'OCRService = run:create_ocr_server',
        ],
    },
)
