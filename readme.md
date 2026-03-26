# iai_tiago ROS2 Workspace

This repository provides the **iai_tiago** ROS2 workspace along with all its required dependencies vendored in the `dep` directory.

## Workspace Structure

```
iai_tiago
    ├── dep (vendored dependencies)
    ├── iai_robotiq_gripper
    ├── iai_tiago
    ├── iai_tiago_bringup
    ├── iai_tiago_description
    ├── iai_tiago_jazzy.repos
    ├── iai_tiago_tools
    └── readme.md
```

## Getting Started

### 1. Clone the repository

```bash
mkdir -p ~/tiago_ws/src
cd ~/tiago_ws/src

git clone https://github.com/mitsav01/iai_tiago.git
```

### 2. Import vendored dependencies

```bash
cd iai_tiago
vcs import dep < iai_tiago.repos
```

This will download all required external repositories into the `dep` directory.

### 3. Install system dependencies

```bash
cd ..
rosdep install --from-paths src --ignore-src -r -y
```

### 4. Build the workspace

```bash
colcon build --symlink-install
source install/setup.bash
```

### 5. Verify installation

Try launching a simple package, e.g.:

```bash
ros2 launch iai_tiago_description display.launch.py
```

---