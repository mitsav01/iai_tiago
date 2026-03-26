# iai_tiago ROS2 Workspace

This repository provides the **iai_tiago** ROS2 workspace along with all its required dependencies vendored in the `dep` directory.

## Workspace Structure

```
iai_tiago
├── dep                  # Vendored dependencies
├── iai_robotiq_gripper  # Robotiq gripper packages
├── iai_tiago            # Core Tiago packages
├── iai_tiago_bringup    # Launch and bringup files
├── iai_tiago_description# URDF and description files
├── iai_tiago_jazzy.repos# Repository manifest for vcs import
├── iai_tiago_tools      # Utility and tool packages
└── readme.md            # This documentation
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/mitsav01/iai_tiago.git
cd iai_tiago
```

> **Note:** If you have already installed dependencies, you can skip steps 2 and 3.

### 2. Import Vendored Dependencies

```bash
mkdir dep
vcs import dep < iai_tiago_jazzy.repos
```

This will download all required external repositories into the `dep` directory.

### 3. Install System Dependencies

```bash
cd ..
rosdep install --from-paths iai_tiago --ignore-src -r -y
```

### 4. Build the Workspace

```bash
colcon build --symlink-install
source install/setup.bash
```

### 5. Verify Installation

Launch a simple package to ensure everything is set up correctly:

```bash
ros2 launch iai_tiago_description display.launch.py
```
