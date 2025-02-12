from setuptools import setup, find_packages

setup(
    name="dyu_sis_lib",  # library 的名稱
    version="1.0.0-beta.1",  # 初始版本號
    description="Including DaYeh University SIS (Student Information System) and iCloud system crawler library. ",  # library 的簡短描述
    long_description=open("README.md").read(),  # 詳細描述，通常從 README.md 載入
    long_description_content_type="text/markdown",  # 說明文件的格式
    author="NUTT1101",  # 作者名稱
    author_email="nutt@ohin1.com",  # 作者 Email
    url="https://github.com/DyuOhin1",  # 專案網址
    packages=find_packages(),  # 自動尋找所有包含程式碼的目錄
    include_package_data=True,  # 包括非 Python 文件（例如靜態文件）
    install_requires=[
        "beautifulsoup4==4.12.3",
        "certifi==2024.12.14",
        "charset-normalizer==3.4.1",
        "idna==3.10",
        "python-dotenv==1.0.1",
        "requests==2.32.3",
        "soupsieve==2.6",
        "urllib3==2.3.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.13.1",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # 要求的 Python 版本
)