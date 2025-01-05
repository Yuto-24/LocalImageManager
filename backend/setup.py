from setuptools import setup, find_packages

setup(
    name="local_image_manager",
    version="0.0.1",
    packages=find_packages(where="src"),  # src 以下のパッケージを検索
    package_dir={"": "src"},  # パッケージのルートディレクトリを指定
    # 必要な依存関係をリストアップ
    install_requires=[
        "tqdm",
        "loguru",
        "pylint",
        "pytest",
        "pytest-cov",
        "opencv-python",
        "pyheif",
        "pillow",
        "piexif",
        "uvicorn",
        "fastapi",
    ],
    # 必要な Python バージョンを指定
    python_requires=">=3.10",
)
