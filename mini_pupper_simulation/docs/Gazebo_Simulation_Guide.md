# Mini Pupper Gazebo Simulation Guide

This guide covers how to launch and control the Mini Pupper 2 robot in Gazebo simulation.

## Table of Contents
- [Quick Start](#quick-start)
- [Launch Methods](#launch-methods)
- [Teleoperation](#teleoperation)
- [Architecture Overview](#architecture-overview)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites
Ensure your workspace is built and sourced:
```bash
cd ~/sfkrobotics_ws  # or your workspace path
colcon build
source install/setup.bash
```

### Launch the Simulation
```bash
ros2 launch mini_pupper_simulation main.launch.py
```

This will:
1. Start Gazebo with the default world
2. Spawn the Mini Pupper 2 robot
3. Launch all necessary controllers
4. Robot will automatically stand in its default pose

### Control the Robot
In a new terminal (make sure to source):
```bash
source ~/sfkrobotics_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

**Controls:**
- `i` - Move forward
- `k` - Stop
- `,` - Move backward
- `j` - Turn left
- `l` - Turn right
- `u` - Move forward-left
- `o` - Move forward-right
- `m` - Move backward-left
- `.` - Move backward-right
- `q/z` - Increase/decrease max speeds
- `w/x` - Increase/decrease only linear speed
- `e/c` - Increase/decrease only angular speed

---

## Launch Methods

### Method 1: All-in-One Launch (Recommended)

**Command:**
```bash
ros2 launch mini_pupper_simulation main.launch.py
```

**What it does:**
- Launches Gazebo simulator
- Spawns robot at default position
- Starts robot description publisher
- Launches Champ high-level gait controllers
- Starts ROS2 low-level joint controllers
- Initializes contact sensors

**Optional arguments:**
```bash
ros2 launch mini_pupper_simulation main.launch.py \
    world:=/path/to/custom.world \
    world_init_x:=1.0 \
    world_init_y:=2.0 \
    world_init_z:=0.066 \
    world_init_heading:=1.57
```

---

### Method 2: Step-by-Step Launch (Advanced)

For debugging or learning, you can launch components individually:

#### Terminal 1: Launch Gazebo
```bash
ros2 launch mini_pupper_simulation gazebo.launch.py
```
- Starts empty Gazebo world
- Useful for testing different environments

#### Terminal 2: Launch Robot Description & Controllers
```bash
ros2 launch mini_pupper_bringup bringup.launch.py \
    use_sim_time:=True \
    hardware_connected:=False
```
- Publishes robot URDF to `/robot_description` topic
- Starts Champ quadruped controller for gait planning
- Starts state estimator for odometry

#### Terminal 3: Spawn Robot
```bash
ros2 run gazebo_ros spawn_entity.py \
    -topic robot_description \
    -entity mini_pupper_2 \
    -x 0 -y 0 -z 0.066
```
- Spawns robot into Gazebo at specified position
- Robot appears in lying down position initially

#### Terminal 4: Launch ROS2 Controllers
```bash
ros2 launch mini_pupper_simulation ros2_controllers.launch.py
```
- Spawns `joint_state_broadcaster` (publishes joint states)
- Spawns `joint_group_effort_controller` (receives trajectory commands)
- **Robot will stand up after this step**

---

## Teleoperation

### Keyboard Control

**Install (if not already installed):**
```bash
sudo apt install ros-humble-teleop-twist-keyboard
```

**Launch:**
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

The teleop node publishes to `/cmd_vel` topic which the robot subscribes to.

---

### Custom Velocity Commands

You can publish custom velocity commands directly:

```bash
# Move forward at 0.1 m/s
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
    "{linear: {x: 0.1, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

# Turn in place at 0.5 rad/s
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
    "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}"
```

**Velocity Limits** (defined in [gait.yaml](../mini_pupper_description/config/champ/mini_pupper_2/gait.yaml)):
- Max linear velocity X: 0.15 m/s
- Max linear velocity Y: 0.15 m/s
- Max angular velocity Z: 1.0 rad/s

---

## Architecture Overview

### Control Flow
```
User Input (teleop)
    ↓
/cmd_vel topic
    ↓
Champ Quadruped Controller (gait planning)
    ↓
/joint_group_effort_controller/joint_trajectory topic
    ↓
ROS2 Joint Controller (Gazebo plugin)
    ↓
Gazebo Physics (robot movement)
```

### Key Components

#### 1. Robot Description
- **Package:** `mini_pupper_description`
- **Launch file:** [mini_pupper_description.launch.py](../../mini_pupper_description/launch/mini_pupper_description.launch.py)
- **Purpose:** Publishes robot URDF model to ROS2

#### 2. Champ Controllers
- **Package:** `champ_base`
- **Launch file:** [champ_controllers.launch.py](../../mini_pupper_bringup/launch/champ_controllers.launch.py)
- **Nodes:**
  - `quadruped_controller_node` - High-level gait planning
  - `state_estimation_node` - Odometry and pose estimation
  - `curvature_compensation` - Drift correction

#### 3. ROS2 Controllers
- **Package:** `mini_pupper_simulation`
- **Launch file:** [ros2_controllers.launch.py](../launch/ros2_controllers.launch.py)
- **Controllers:**
  - `joint_state_broadcaster` - Publishes joint positions
  - `joint_group_effort_controller` - Executes joint trajectories

#### 4. Gazebo Plugins
- **gazebo_ros2_control** - Bridges ROS2 controllers to Gazebo
- **Contact sensors** - Detects foot contact with ground
- **Camera plugin** - Simulates robot camera
- **IMU plugin** - Simulates inertial measurement unit

---

## Troubleshooting

### Robot Spawns but Doesn't Stand

**Symptoms:** Robot lies on ground motionless

**Cause:** ROS2 controllers didn't start properly

**Solution:**
```bash
# Check if controllers are running
ros2 control list_controllers

# You should see:
# joint_state_broadcaster[joint_state_broadcaster/JointStateBroadcaster] active
# joint_group_effort_controller[effort_controllers/JointGroupEffortController] active

# If not, manually spawn them:
ros2 launch mini_pupper_simulation ros2_controllers.launch.py
```

---

### Robot Moves Erratically/Jitters

**Symptoms:** Robot vibrates, bounces, or moves unpredictably without commands

**Possible Causes:**
1. Physics timestep issues
2. Controller gains too high
3. Spawn position too low causing ground contact issues

**Solutions:**

1. **Check spawn height:**
   Default is 0.066m. Try spawning slightly higher:
   ```bash
   ros2 launch mini_pupper_simulation main.launch.py world_init_z:=0.1
   ```

2. **Verify no velocity commands are being sent:**
   ```bash
   ros2 topic echo /cmd_vel
   # Should show nothing or all zeros
   ```

3. **Check joint limits in URDF:**
   Ensure joints are within their limit ranges defined in:
   [mini_pupper_description.urdf.xacro](../../mini_pupper_description/urdf/mini_pupper_2/mini_pupper_description.urdf.xacro)

---

### Controllers Fail to Load

**Symptoms:** Error messages about controller_manager service not available

**Cause:** Gazebo plugin `gazebo_ros2_control` failed to load

**Solution:**
1. Check that URDF contains gazebo_ros2_control plugin
2. Verify controller config file exists:
   ```bash
   ls ~/sfkrobotics_ws/install/mini_pupper_description/share/mini_pupper_description/config/ros_control/
   ```
3. Check Gazebo logs for errors:
   ```bash
   # Look in terminal where gazebo was launched
   ```

---

### Gazebo Crashes or Won't Start

**Symptoms:** Gazebo window doesn't open or crashes immediately

**Solutions:**

1. **Check Gazebo installation:**
   ```bash
   gazebo --version
   # Should show Gazebo 11.x
   ```

2. **Update Gazebo models:**
   ```bash
   cd ~/.gazebo/models
   wget -r -R "index\.html*" http://models.gazebosim.org/
   ```

3. **Clear Gazebo cache:**
   ```bash
   rm -rf ~/.gazebo/cache/
   ```

---

## Useful ROS2 Commands

### Monitor Topics
```bash
# List all active topics
ros2 topic list

# Monitor velocity commands
ros2 topic echo /cmd_vel

# Monitor joint states
ros2 topic echo /joint_states

# Monitor odometry
ros2 topic echo /odom
```

### Inspect Controllers
```bash
# List all controllers
ros2 control list_controllers

# Get controller info
ros2 control list_hardware_interfaces
```

### View Transforms
```bash
# View TF tree
ros2 run tf2_tools view_frames

# Echo specific transform
ros2 run tf2_ros tf2_echo base_link lffoot
```

---

## Configuration Files

### Key Config Files
- **Joints:** [joints.yaml](../../mini_pupper_description/config/champ/mini_pupper_2/joints.yaml)
- **Links:** [links.yaml](../../mini_pupper_description/config/champ/mini_pupper_2/links.yaml)
- **Gait:** [gait.yaml](../../mini_pupper_description/config/champ/mini_pupper_2/gait.yaml)
- **PID Gains:** [mini_pupper_2_controller.yaml](../../mini_pupper_description/config/ros_control/mini_pupper_2_controller.yaml)

### Modifying Gait Parameters
Edit [gait.yaml](../../mini_pupper_description/config/champ/mini_pupper_2/gait.yaml):
```yaml
gait:
  nominal_height: 0.06        # Standing height (meters)
  max_linear_velocity_x: 0.15 # Max forward speed (m/s)
  max_angular_velocity_z: 1.0 # Max turn speed (rad/s)
  swing_height: 0.017         # How high legs lift (meters)
  stance_duration: 0.2        # Time per step (seconds)
```

After modifying, rebuild:
```bash
cd ~/sfkrobotics_ws
colcon build --packages-select mini_pupper_description
source install/setup.bash
```

---

## Additional Resources

- [URDF Guide](../../mini_pupper_description/docs/URDF_Guide.md) - Understanding robot model files
- [Champ Documentation](https://github.com/chvmp/champ) - Quadruped controller details
- [ROS2 Control Documentation](https://control.ros.org/humble/index.html) - Controller framework
