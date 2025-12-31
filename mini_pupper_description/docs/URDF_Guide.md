# URDF Guide for Mini Pupper 2

This guide provides a comprehensive overview of URDF (Unified Robot Description Format) files, with examples from the Mini Pupper 2 quadruped robot.

## Table of Contents
1. [What is a URDF File](#what-is-a-urdf-file)
2. [Links in URDF](#links-in-urdf)
3. [Joints in URDF](#joints-in-urdf)
4. [Mini Pupper 2 Robot Structure](#mini-pupper-2-robot-structure)

---

## What is a URDF File

URDF (Unified Robot Description Format) is an XML-based file format used in ROS (Robot Operating System) to describe robot models. A URDF file contains:

- **Links**: Rigid bodies that represent the robot's physical components
- **Joints**: Connections between links that define how they move relative to each other
- **Visual elements**: 3D meshes and colors for visualization
- **Collision geometry**: Simplified shapes for physics simulation
- **Inertial properties**: Mass and moment of inertia for dynamics

### General Structure

```xml
<?xml version="1.0" ?>
<robot name="robot_name" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Links define the robot's physical components -->
  <link name="link_name">
    <!-- visual, collision, and inertial properties -->
  </link>

  <!-- Joints connect links together -->
  <joint name="joint_name" type="joint_type">
    <!-- parent, child, axis, and limits -->
  </joint>

</robot>
```

**Reference**: [mini_pupper_description.urdf.xacro](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro)

---

## Links in URDF

Links represent the rigid bodies of the robot. Each link can have three main components: visual, collision, and inertial properties.

### General Structure of a Link

```xml
<link name="link_name">
  <visual>
    <!-- How the link looks -->
  </visual>
  <collision>
    <!-- Simplified geometry for physics -->
  </collision>
  <inertial>
    <!-- Mass and inertia properties -->
  </inertial>
</link>
```

### Visual Element

The `<visual>` tag defines how the link appears in visualization tools like RViz.

**Example from Mini Pupper 2** - [base_link:30-37](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L30-L37):

```xml
<link name="base_link">
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <mesh filename="file://$(find mini_pupper_description)/meshes/mini_pupper_2/base_link.stl" scale="1 1 1"/>
    </geometry>
    <material name="opaque252525"/>
  </visual>
  <!-- collision and inertial omitted for brevity -->
</link>
```

### Types of Geometries Used in URDF

URDF supports several geometry types:

#### 1. Mesh (Most Common for Complex Shapes)

Used for detailed 3D models like robot bodies and legs.

**Example** - [lf1 link:60-66](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L60-L66):

```xml
<visual>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <mesh filename="file://$(find mini_pupper_description)/meshes/mini_pupper_2/lf1.stl" scale="1 1 1"/>
  </geometry>
  <material name="opaque666666"/>
</visual>
```

#### 2. Box

Rectangular prism defined by size (length, width, height).

**Example** - [camera_link:1244-1254](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L1244-L1254):

```xml
<link name="camera_link">
  <visual>
    <geometry>
      <box>
        <size>0.02 0.02 0.02</size>
      </box>
    </geometry>
    <material>
      <ambient>0 0 1 1</ambient>
      <diffuse>0 0 1 1</diffuse>
    </material>
  </visual>
</link>
```

#### 3. Cylinder

Defined by radius and length. Used for wheels or cylindrical parts.

```xml
<geometry>
  <cylinder radius="0.05" length="0.1"/>
</geometry>
```

#### 4. Sphere

Defined by radius. Less common but useful for simple shapes.

```xml
<geometry>
  <sphere radius="0.05"/>
</geometry>
```

### Origin - rpy and xyz

The `<origin>` tag specifies the position and orientation of the geometry relative to the link's frame.

- **xyz**: Position offset [x, y, z] in meters
- **rpy**: Orientation [roll, pitch, yaw] in radians

**Example** - [Body_front:313-316](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L313-L316):

```xml
<visual>
  <origin xyz="-0.089299 0 0.015543" rpy="0 0 0"/>
  <geometry>
    <mesh filename="file://$(find mini_pupper_description)/meshes/mini_pupper_2/Body_front.stl" scale="1 1 1"/>
  </geometry>
  <material name="opaque2552210"/>
</visual>
```

This means the mesh is translated -0.089299m in X, 0m in Y, and 0.015543m in Z, with no rotation.

### Material

Materials define the color and appearance of the link in visualization.

**Mini Pupper 2 Materials** - [materials.xacro](../urdf/mini_pupper_2/materials.xacro):

```xml
<material name="opaque2552210">
  <color rgba="1.0 0.8666666666666667 0.0 1.0"/>
</material>
```

RGBA values range from 0.0 to 1.0:
- **R**: Red channel
- **G**: Green channel
- **B**: Blue channel
- **A**: Alpha (transparency), where 1.0 is fully opaque

**Usage Example** - [lf1:65](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L65):

```xml
<material name="opaque666666"/>
```

### Collision

The `<collision>` tag defines simplified geometry for physics simulation and collision detection. It typically mirrors the visual geometry but may use simpler shapes for performance.

**Example** - [base_link:38-43](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L38-L43):

```xml
<collision>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <mesh filename="file://$(find mini_pupper_description)/meshes/mini_pupper_2/base_link.stl" scale="1 1 1"/>
  </geometry>
</collision>
```

### Inertial

The `<inertial>` tag specifies the mass and moment of inertia for physics simulation. This is crucial for accurate dynamics.

**Example** - [lf1:55-59](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L55-L59):

```xml
<inertial>
  <origin xyz="0.020109 0.002332 0.006500" rpy="0 0 0"/>
  <mass value="0.020769"/>
  <inertia ixx="2.494061e-6" iyy="3.735906e-6" izz="3.222909e-6"
           ixy="-7.662e-9" iyz="-0.014e-9" ixz="-33.565e-9"/>
</inertial>
```

Components:
- **origin**: Center of mass location relative to link frame
- **mass**: Mass in kilograms
- **inertia**: 3x3 inertia tensor:
  - `ixx, iyy, izz`: Diagonal elements (moments of inertia)
  - `ixy, iyz, ixz`: Off-diagonal elements (products of inertia)

**Example with xacro property** - [rffoot:423-427](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L423-L427):

```xml
<link name="rffoot">
  <inertial>
    <origin xyz="${feet_centre_of_mass}" rpy="0 0 0"/>
    <mass value="${feet_weight}"/>
    <inertia ixx="41.995e-9" iyy="62.40e-9" izz="29.798e-9"
             ixy="0.0e-9" iyz="0.0e-9" ixz="1.616e-9"/>
  </inertial>
  <!-- visual and collision omitted -->
</link>
```

Where xacro properties are defined as:
```xml
<xacro:property name="feet_weight" value="0.001405" />
<xacro:property name="feet_centre_of_mass" value="-0.014 0.00025 0.002488" />
```

---

## Joints in URDF

Joints connect links and define how they can move relative to each other. They are the "actuators" of the robot.

### General Structure of a Joint

```xml
<joint name="joint_name" type="joint_type">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <origin xyz="x y z" rpy="roll pitch yaw"/>
  <axis xyz="x y z"/>
  <limit lower="min" upper="max" effort="max_force" velocity="max_vel"/>
  <dynamics damping="damping_value" friction="friction_value"/>
</joint>
```

### Types of Joints

#### 1. Revolute (Rotational with Limits)

A hinge joint that rotates around an axis with joint limits. Most common for robot limbs.

**Example** - [base_lf1:702-708](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L702-L708):

```xml
<joint name="base_lf1" type="revolute">
  <origin xyz="0.05 0.0235 0.0" rpy="0 0 0"/>
  <parent link="base_link"/>
  <child link="lf1"/>
  <axis xyz="1.0 0.0 0.0"/>
  <limit upper="0.425" lower="-0.550" effort="20" velocity="1.5"/>
</joint>
```

This joint:
- Connects `base_link` (parent) to `lf1` (child, left front leg link 1)
- Located at position (0.05, 0.0235, 0.0) relative to parent
- Rotates around X-axis (1, 0, 0)
- Has limits from -0.550 to 0.425 radians
- Maximum torque: 20 Nm
- Maximum velocity: 1.5 rad/s

#### 2. Continuous (Unlimited Rotation)

Similar to revolute but with no joint limits. Used for wheels.

```xml
<joint name="wheel_joint" type="continuous">
  <parent link="base_link"/>
  <child link="wheel_link"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
</joint>
```

#### 3. Fixed (No Movement)

A rigid connection between two links. Used for sensors, cosmetic parts, or structural connections.

**Example** - [base_link_to_base_inertia:696-700](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L696-L700):

```xml
<joint name="base_link_to_base_inertia" type="fixed">
  <parent link="base_link"/>
  <child link="base_inertia"/>
  <origin rpy="0 0 0" xyz="0 0 0"/>
</joint>
```

**Another Example** - [rf3_foot:828-832](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L828-L832):

```xml
<joint name="rf3_foot" type="fixed">
  <origin xyz="0 0 -0.056" rpy="0 0 0"/>
  <parent link="rf3"/>
  <child link="rffoot"/>
</joint>
```

#### 4. Prismatic (Linear Sliding)

Translates along an axis. Used for linear actuators.

```xml
<joint name="slider_joint" type="prismatic">
  <parent link="base_link"/>
  <child link="slider_link"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="0.0" upper="0.5" effort="100" velocity="1.0"/>
</joint>
```

#### 5. Planar (2D Movement)

Allows movement in a plane. Rarely used.

#### 6. Floating (6 DOF)

Unconstrained motion in all 6 degrees of freedom. Used for free-floating objects.

### Parent and Child Link

- **Parent link**: The reference frame for the joint
- **Child link**: The link that moves relative to the parent

The kinematic chain flows from parent to child. For Mini Pupper 2:
```
base_link → lf1 → lf2 → lf3 → lffoot
```

**Example chain** - [lf1_lf2:710-716](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L710-L716):

```xml
<joint name="lf1_lf2" type="revolute">
  <origin xyz="-4E-05 0.0197 0" rpy="0 0 0"/>
  <parent link="lf1"/>
  <child link="lf2"/>
  <axis xyz="0.0 1.0 0.0"/>
  <limit upper="2.40" lower="0.55" effort="20" velocity="1.5"/>
</joint>
```

### Origin and Axis

#### Origin

Defines where the child link's frame is positioned relative to the parent's frame when the joint is at zero position.

**Example** - [base_lb1:774-775](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L774-L775):

```xml
<joint name="base_lb1" type="revolute">
  <origin xyz="-0.066 0.0235 0.0" rpy="0 0 0"/>
  <!-- ... -->
</joint>
```

This places the left back leg joint 0.066m behind the base and 0.0235m to the left.

#### Axis

Defines the axis of rotation (for revolute/continuous) or translation (for prismatic).

**Example** - [lf2_lf3:718-723](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L718-L723):

```xml
<joint name="lf2_lf3" type="revolute">
  <origin xyz="0 0.00475 -0.05" rpy="0 0 0"/>
  <parent link="lf2"/>
  <child link="lf3"/>
  <axis xyz="0.0 1.0 0.0"/>
  <limit upper="-0.22" lower="-2.18" effort="20" velocity="1.5"/>
</joint>
```

The axis `(0, 1, 0)` means rotation around the Y-axis (pitch motion for the leg).

### Dynamics

The `<dynamics>` tag specifies friction and damping for the joint. These are used in physics simulation.

```xml
<dynamics damping="0.1" friction="0.05"/>
```

- **damping**: Opposes velocity (Nm·s/rad for revolute, N·s/m for prismatic)
- **friction**: Static/kinetic friction (Nm for revolute, N for prismatic)

Note: The Mini Pupper 2 URDF doesn't explicitly define dynamics in the joint definitions, but Gazebo parameters are set elsewhere in the file.

### Limit

The `<limit>` tag defines constraints on joint motion and actuator properties.

**Example** - [base_rf1:726-731](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L726-L731):

```xml
<joint name="base_rf1" type="revolute">
  <origin xyz="0.05 -0.0235 0.0" rpy="0 0 0"/>
  <parent link="base_link"/>
  <child link="rf1"/>
  <axis xyz="1.0 0.0 0.0"/>
  <limit upper="0.550" lower="-0.425" effort="20" velocity="1.5"/>
</joint>
```

Parameters:
- **lower**: Minimum joint value (radians for revolute, meters for prismatic)
- **upper**: Maximum joint value
- **effort**: Maximum force/torque (Nm for revolute, N for prismatic)
- **velocity**: Maximum speed (rad/s for revolute, m/s for prismatic)

---

## Mini Pupper 2 Robot Structure

### Robot Overview

The Mini Pupper 2 is a quadruped robot with:
- **1 base link**: Main body
- **12 leg links**: 3 links per leg × 4 legs
- **4 foot links**: One per leg
- **Various body parts**: Front shell, PCB board, connectors, lidar, camera
- **12 revolute joints**: 3 per leg for leg actuation
- **Multiple fixed joints**: For sensors and structural components

### Leg Structure

Each leg (Left Front shown as example):

```
base_link
    ↓ (revolute: base_lf1, axis=[1,0,0])
   lf1  ← Hip abduction/adduction
    ↓ (revolute: lf1_lf2, axis=[0,1,0])
   lf2  ← Hip flexion/extension
    ↓ (revolute: lf2_lf3, axis=[0,1,0])
   lf3  ← Knee flexion/extension
    ↓ (fixed: lf3_foot)
 lffoot ← Contact point
```

### Joint Example with Full Details

**Complete joint example** - [rb1_rb2:758-764](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L758-L764):

```xml
<joint name="rb1_rb2" type="revolute">
  <origin xyz="-4E-05 -0.0197 0" rpy="0 0 0"/>
  <parent link="rb1"/>
  <child link="rb2"/>
  <axis xyz="0.0 1.0 0.0"/>
  <limit upper="2.40" lower="0.55" effort="20" velocity="1.5"/>
</joint>
```

Breaking it down:
1. **Name**: `rb1_rb2` connects right back leg segment 1 to segment 2
2. **Type**: `revolute` allows rotation with limits
3. **Origin**: Child frame is at (-0.00004, -0.0197, 0) relative to parent
4. **Parent**: `rb1` (upper leg segment)
5. **Child**: `rb2` (middle leg segment)
6. **Axis**: `(0, 1, 0)` rotates around Y-axis (knee bend)
7. **Limits**:
   - Range: 0.55 to 2.40 radians (~31° to 137°)
   - Max torque: 20 Nm
   - Max velocity: 1.5 rad/s

### Sensor Integration Examples

#### Lidar

**Joint** - [pcb_lidar:822-826](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L822-L826):

```xml
<joint name="pcb_lidar" type="fixed">
  <origin xyz="0.009 0.024 0.042" rpy="0 0 1.57" />
  <parent link="Board_PCB" />
  <child link="lidar_link" />
</joint>
```

The lidar is mounted on the PCB board with a 90° yaw rotation (1.57 rad).

#### Camera

**Joint** - [bodyfront_camera_joint:1257-1261](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L1257-L1261):

```xml
<joint name="bodyfront_camera_joint" type="fixed">
  <parent link="Body_front"/>
  <child link="camera_link"/>
  <origin xyz="0.02 0 0.02" rpy="0 0 0"/>
</joint>
```

#### IMU

**Joint** - [imu_joint:1224-1227](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro#L1224-L1227):

```xml
<joint name="imu_joint" type="fixed">
  <parent link="base_link"/>
  <child link="imu_link"/>
</joint>
```

### Visualization

To visualize the Mini Pupper 2 URDF model, use the launch file:

```bash
ros2 launch mini_pupper_description view_mp2.launch.py
```

This will:
1. Load the URDF from [mini_pupper_description.urdf.xacro](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro)
2. Start robot_state_publisher
3. Launch joint_state_publisher_gui for interactive joint control
4. Open RViz2 with the configured view

**Launch file reference**: [view_mp2.launch.py](../launch/view_mp2.launch.py)

---

## Additional Resources

- [ROS URDF Tutorials](http://wiki.ros.org/urdf/Tutorials)
- [URDF XML Specification](http://wiki.ros.org/urdf/XML)
- [Xacro Documentation](http://wiki.ros.org/xacro)
- Mini Pupper 2 Files:
  - [URDF Definition](../urdf/mini_pupper_2/mini_pupper_description.urdf.xacro)
  - [Materials](../urdf/mini_pupper_2/materials.xacro)
  - [Launch File](../launch/view_mp2.launch.py)
