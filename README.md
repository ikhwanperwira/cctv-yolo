# CCTV YOLO

[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-%E2%89%A5%203.9.5-blue)](https://www.python.org/downloads/release/python-395/)

## Introduction

Welcome to the CCTV YOLO! This project offers realtime object detection through HTTP protocol and cloudflare tunneling:

These predictions are based on `yolov3-tiny` trained on comprehensive coco datasets.

## Getting Started

To get started with CCTV YOLO, follow these steps:

### Prerequisites

Before using CCTV YOLO, ensure you have the following in `requirements.txt` and `Python ≥ 3.9.5`.

### Installation

To install the CCTV YOLO, follow these steps:

1. **Create a Virtual Environment:**

    * On Windows:
      ```powershell
      python -m venv .venv
      ```
    * On Linux:
      ```bash
      python3 -m venv .venv
      ```

2. **Activate the Virtual Environment:**
    * On Windows:
      ```powershell
      .venv\Scripts\activate
      ```
    * On Linux:
      ```bash
      source .venv/bin/activate
      ```
3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Copy Environment Variables:**
    ```
    cp .env.example .env
    ```
    *Modify the values in the .env file according to your API configuration!*

### Start Server
Or you can just setup all and start the server directly according your operating systems.

  * On Windows:
    ```powershell
    ./start-server-windows.bat
    ```
  * On Linux:
    ```bash
    ./start-server-linux.sh
    ```

## About Cloudflared Tunneling
It's just optional feature where your CCTV+YOLO is hosted to the internet for free, here is you can setup the tunnel authentication through this [DOC](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/create-local-tunnel/). Therefore you can retrieve information about your CF authentication so that you can put it into `.env` file.

> **Note:** If you cloned this repo, **you don't need** download or install `cloudflared` since it's already downloaded in binary preinstalled in `bin/` folder.


## Support
If you encounter any issues or have questions, reach out to our support team at [ikhwanperwira@gmail.com](ikhwanperwira@gmail.com)

## Contributing
We welcome contributions! Whether it's bug reports, feature requests, or code contributions.

## License
CCTV YOLO is licensed under the MIT License - see the LICENSE file for details.
