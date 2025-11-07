# Magician Project – General Visual Perception

**Repository:** [magician-project/magician_general_visual_perception](https://github.com/magician-project/magician_general_visual_perception)
**Paper:** [Y-MAP-Net: Real-time depth, normals, segmentation, multi-label captioning and 2D human pose in RGB images](https://arxiv.org/abs/2411.10334)

---

## 🧠 Overview

This repository contains the **runtime implementation** of **Y-MAP-Net**, a unified neural architecture capable of performing **real-time visual perception tasks** from a single RGB image, including:

* **Depth estimation**
* **Surface normal prediction**
* **Semantic segmentation**
* **Multi-label image captioning**
* **2D human pose estimation**

Y-MAP-Net is designed for **real-time performance** on modern GPUs and supports flexible input sources such as webcam, image, or video files.

This work is part of the **Magician Project**, a European initiative focused on **multi-modal general AI perception systems**.

---

## 📄 Reference

> **Y-MAP-Net: Real-time depth, normals, segmentation, multi-label captioning and 2D human pose in RGB images**
> *Qammaz et al., 2024*
> [arXiv:2411.10334](https://arxiv.org/abs/2411.10334)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/magician-project/magician_general_visual_perception.git
cd magician_general_visual_perception
```

### 2. Run the Setup Script

A setup script is provided in `scripts/setup.sh`.
It automatically installs required system and Python dependencies and sets up the pretrained model.

Run:

```bash
scripts/setup.sh
```

This script will:

* Create a virtual environment (`venv/`)
* Install Python dependencies from `requirements.txt`
* Install TensorFlow with CUDA support (if available)
* Download pretrained model data if missing

This disables the virtual environment and installs dependencies globally in the Colab runtime.

---

## 🧩 Dependencies

Main Python dependencies (see `requirements.txt`):

* `tensorflow[and-cuda]`
* `tensorflow-model-optimization`
* `tf_keras`
* `opencv-python`
* `numba`
* `numpy`

System dependencies automatically handled by `setup.sh`:

```
python3-venv python3-pip zip wget libhdf5-dev libzstd-dev rsync numactl
```

---

## ⬇️ Pretrained Model Download

The setup script automatically downloads pretrained weights:

```bash
scripts/downloadPretrained.sh
```


---

## 🚀 Running Y-MAP-Net

The main runtime entry point is:

```bash
python3 runYMAPNet.sh
```

By default, it:

* Loads the pretrained model from `2d_pose_estimation/`
* Starts webcam-based real-time inference (640×480)
* Displays live visualization with detected keypoints, segmentation, and depth overlay

---

### 🧭 Command-line Options

| Option                    | Description                                                      |
| ------------------------- | ---------------------------------------------------------------- |
| `--from <path>`           | Use a video file or image instead of the webcam                  |
| `--scale <float>`         | Resize input frames (e.g., `--scale 0.5`)                        |
| `--size <width> <height>` | Set custom input resolution                                      |
| `--threshold <value>`     | Adjust keypoint detection threshold                              |
| `--border <int>`          | Emulate border pattern in visualization                          |
| `--crop <x> <y> <size>`   | Apply custom square crop on input                                |
| `--nocrop`                | Disable automatic cropping                                       |
| `--tile`                  | Enable tiled inference for large frames                          |
| `--blur <int>`            | Apply blur filter before inference                               |
| `--noise <float>`         | Add Gaussian noise to input (0.0–1.0)                            |
| `--profiling`             | Enable runtime performance profiling                             |
| `--engine <backend>`      | Choose inference backend (`tensorflow` or `onnx`)                |
| `--illustrate`            | Save output illustrations instead of displaying live             |
| `--save`                  | Save processed frames and generate output videos                 |
| `--headless`              | Run without visualization (for batch mode)                       |
| `--collab`                | Enable Colab-friendly mode (implies `--illustrate` and `--save`) |

---

### 🎮 Keyboard Controls (during live visualization)

| Key          | Action                              |
| ------------ | ----------------------------------- |
| `q` or `ESC` | Quit the application                |
| `s`          | Save a 3D point cloud (`.ply` file) |
| `u`          | Upload the current frame            |
| `a`          | Save a demo screenshot              |
| `←`          | Navigate left (reserved)            |

---

## 💾 Output Files

When `--save` is enabled, output frames and visualizations are stored as PNGs and later compiled into videos:

| Output                 | Description                      |
| ---------------------- | -------------------------------- |
| `*_lastRun3DHiRes.mp4` | 3D pose + depth output video     |
| `*_illustration.mp4`   | Visualization of network outputs |
| `colorFrame_*.png`     | Individual processed frames      |
| `composite_*.png`      | Composite visualization frames   |

---

## 🧰 Project Structure

```
magician_general_visual_perception/
│
├── 2d_pose_estimation/            # Pretrained model files (auto-downloaded)
├── scripts/
│   ├── setup.sh                   # Environment setup script
│   └── downloadPretrained.sh      # Model download helper
│
├── runYMAPNet.sh                  # Main runtime entry script
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🔬 Citation

If you use this repository or Y-MAP-Net in your research, please cite:

```bibtex
@article{qammaz2024ymapnet,
  title={Y-MAP-Net: Real-time depth, normals, segmentation, multi-label captioning and 2D human pose in RGB images},
  author={A. Qammaz, N. Vasilikopoulos, I. Oikonomidis and A.A. Argyros},
  journal={arXiv preprint arXiv:2411.10334},
  year={2024}
}
```

---
 

---

## 📜 License

This repository is distributed under the **FORTH license** (see `LICENSE` file).


---

Would you like me to tailor it slightly for **academic presentation style** (e.g., for inclusion in an arXiv-linked code repo), or keep it **developer-oriented** as above?

