# ROS2 Nodes and Topics: Understanding Robot Communication

This guide teaches ROS2 communication fundamentals using the Mini Pupper 2 robot visualization.

## Learning Objectives

By the end of this guide, students will:
1. **Understand node relationships** - How ROS2 nodes communicate through topics
2. **Observe live data flow** - See real-time topic messages as robot joints move

---

## Prerequisites

Ensure you have the visualization running:
```bash
source ~/sfkrobotics_ws/install/setup.bash
ros2 launch mini_pupper_description view_mp2.launch.py
```

You should see:
- **RViz window** showing the Mini Pupper 2 robot
- **Joint State Publisher GUI** with sliders for each joint

---

## Part 1: Understanding Node Relationships with rqt_graph

### What is rqt_graph?

**rqt_graph** is a visualization tool that shows:
- **Nodes** (circles/ovals) - Individual programs running in ROS2
- **Topics** (arrows) - Communication channels between nodes
- **Data flow direction** - Which nodes publish and which subscribe

Think of it like a **map of conversations** happening in your robot system.

---

### Step 1: Launch rqt_graph

Open a new terminal and run:
```bash
source ~/sfkrobotics_ws/install/setup.bash
rqt_graph
```

A window will open showing your ROS2 system's communication graph.

---

### Step 2: Configure the View

In the rqt_graph window:

1. **Set dropdown menus at the top:**
   - Nodes only: **"Nodes/Topics (all)"**
   - Hide: **Uncheck all boxes** (or check "Dead sinks" and "Leaf topics")
   - Group: **None**

2. **Click the refresh button** (circular arrow icon) to update the graph

You should now see a clear graph showing nodes and their connections!

---

### Step 3: Identify Key Nodes

Look for these important nodes in your graph:

#### 1. `/joint_state_publisher_gui`
- **Shape:** Oval/circle
- **Color:** Usually blue
- **Role:** Publishes joint positions when you move sliders
- **Outgoing arrow:** Points to `/joint_states` topic

#### 2. `/robot_state_publisher`
- **Shape:** Oval/circle
- **Color:** Usually blue
- **Role:** Converts joint positions to 3D transforms
- **Incoming arrow:** From `/joint_states` topic
- **Outgoing arrows:** To `/tf` and `/tf_static` topics

#### 3. `/rviz`
- **Shape:** Oval/circle
- **Color:** Usually blue
- **Role:** Visualizes the robot (what you see on screen)
- **Incoming arrows:** From `/tf` topic and `/robot_description` topic

---

### Step 4: Trace the Data Flow

Follow this communication path in the graph:

```
┌──────────────────────────────┐
│ joint_state_publisher_gui    │ ← User moves sliders here
└──────────────┬───────────────┘
               │ publishes to
               ↓
        /joint_states topic
        (sensor_msgs/JointState)
               │
               ↓ subscribes from
┌──────────────┴───────────────┐
│   robot_state_publisher      │ ← Calculates 3D positions
└──────────────┬───────────────┘
               │ publishes to
               ↓
           /tf topic
     (geometry_msgs/TransformStamped)
               │
               ↓ subscribes from
        ┌──────┴─────┐
        │   rviz     │ ← Displays robot
        └────────────┘
```

**Key Concept:** This is the **publish-subscribe pattern**:
- One node **publishes** data to a topic
- Other nodes **subscribe** to that topic to receive the data
- Nodes don't directly talk to each other - they communicate through topics!

---

### Understanding the Graph

#### Nodes (Ovals)
- Each oval represents a **running program**
- Nodes are independent - they can start/stop without affecting others
- Nodes communicate only through topics

#### Topics (Arrows)
- Arrows show the **direction of data flow**
- Arrow points **from publisher TO subscriber**
- Topic names appear on the arrows (like `/joint_states`)

#### Example Relationships

**Publisher → Topic → Subscriber:**
```
/joint_state_publisher_gui  →  /joint_states  →  /robot_state_publisher
```

Translation:
- "The GUI node publishes joint positions"
- "The state publisher node receives those positions"
- "They communicate through the /joint_states topic"

---

### Activity 1: Identify Relationships

Answer these questions using your rqt_graph:

1. **How many nodes are currently running?**
   - Count the ovals in the graph

2. **Which node publishes to `/joint_states`?**
   - Follow the arrow pointing TO the `/joint_states` topic
   - The oval at the arrow's start is the publisher

3. **Which nodes subscribe to `/tf`?**
   - Follow arrows pointing FROM the `/tf` topic
   - The ovals at the arrow's end are subscribers

4. **What would happen if you closed the joint_state_publisher_gui?**
   - The `/joint_states` topic would stop receiving updates
   - The robot would freeze in RViz (no new joint positions)

---

## Part 2: Observing Live Topic Data

Now let's see the **actual data** flowing through these topics!

---

### Step 1: Monitor Joint States

Open a **new terminal** and run:
```bash
source ~/sfkrobotics_ws/install/setup.bash
ros2 topic echo /joint_states
```

You'll see output like:
```yaml
header:
  stamp:
    sec: 1234567890
    nanosec: 123456789
  frame_id: ''
name:
- base_lf1
- lf1_lf2
- lf2_lf3
- lf3_lffoot
- base_rf1
- rf1_rf2
- rf2_rf3
- rf3_rffoot
- base_lb1
- lb1_lb2
- lb2_lb3
- lb3_lbfoot
- base_rb1
- rb1_rb2
- rb2_rb3
- rb3_rbfoot
position:
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
velocity: []
effort: []
```

**What you're seeing:**
- `name`: List of all joint names (16 joints for 4 legs)
- `position`: Current angle of each joint (in radians)
- `velocity`: How fast each joint is moving (empty if stationary)
- `effort`: Force/torque applied to each joint

---

### Step 2: Move a Joint and Watch the Data Change

1. **Keep the terminal visible** showing `ros2 topic echo /joint_states`

2. **Go to the Joint State Publisher GUI window**

3. **Slowly move the slider for `base_lf1`** (left front leg, hip joint)

4. **Watch the terminal** - you'll see the `position` array update in real-time!

**Example:**
```yaml
position:
- 0.523599   # <-- This value changes as you move the slider!
- 0.0
- 0.0
# ... rest of joints
```

**Key Observation:** The data is being **published continuously** at ~10 Hz (10 times per second)

---

### Step 3: Cleaner Output - Show Only Positions

For a cleaner view, show just the joint positions:

```bash
ros2 topic echo /joint_states --field position
```

Now you'll only see:
```yaml
[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
```

Move different sliders and watch specific values change:
- **Slider 1 (base_lf1)** → Changes index [0]
- **Slider 2 (lf1_lf2)** → Changes index [1]
- **Slider 3 (lf2_lf3)** → Changes index [2]
- And so on...

---

### Step 4: Check the Publish Rate

In another terminal, check how often messages are published:

```bash
ros2 topic hz /joint_states
```

Output:
```
average rate: 10.002
    min: 0.099s max: 0.101s std dev: 0.00045s window: 11
```

This shows the GUI is publishing at **10 Hz** (10 messages per second).

**Why does this matter?**
- Higher frequency = smoother robot motion
- Too high = wasted computation
- 10 Hz is good for visualization, but real robot control needs 100-1000 Hz!

---

## Part 3: Understanding Topic Information

### View Topic Details

Get information about the `/joint_states` topic:

```bash
ros2 topic info /joint_states
```

Output:
```
Type: sensor_msgs/msg/JointState
Publisher count: 1
Subscription count: 2
```

**What this tells us:**
- **Type:** The message format (sensor_msgs/JointState)
- **Publisher count: 1** - One node is publishing (joint_state_publisher_gui)
- **Subscription count: 2** - Two nodes are subscribing (robot_state_publisher and possibly rviz)

---

### Inspect the Message Structure

See what data the message contains:

```bash
ros2 interface show sensor_msgs/msg/JointState
```

Output:
```
std_msgs/Header header
string[] name
float64[] position
float64[] velocity
float64[] effort
```

**Message breakdown:**
- `header`: Timestamp and metadata
- `name[]`: Array of joint names (strings)
- `position[]`: Array of joint angles in radians (floats)
- `velocity[]`: Array of joint speeds (optional)
- `effort[]`: Array of joint forces/torques (optional)

---

## Part 4: Hands-On Activities

### Activity 2: Multi-Terminal Demo

Set up this demo to show the complete data flow:

**Terminal 1:** Launch the system
```bash
ros2 launch mini_pupper_description view_mp2.launch.py
```

**Terminal 2:** Show node graph
```bash
rqt_graph
```

**Terminal 3:** Echo joint states
```bash
ros2 topic echo /joint_states --field position
```

**Terminal 4:** Show publish rate
```bash
ros2 topic hz /joint_states
```

**Now demonstrate:**
1. Point to the graph in Terminal 2
2. Show the data flowing in Terminal 3
3. Move a slider in the GUI
4. Students see:
   - **Graph:** Static visualization of connections
   - **Data:** Live values changing
   - **Rate:** Consistent 10 Hz updates
   - **RViz:** Visual representation

---

### Activity 3: Predict and Verify

1. **"What happens if we close the joint_state_publisher_gui?"**
   - Prediction: No more joint_states messages
   - Verify: Close GUI, watch Terminal 3 stop updating

2. **"Which joint does slider #5 control?"**
   - Look at output: `name: [base_lf1, lf1_lf2, lf2_lf3, lf3_lffoot, base_rf1, ...]`
   - Index [4] → base_rf1 (right front hip)
   - Verify: Move slider 5, watch index [4] change

3. **"Can multiple nodes subscribe to the same topic?"**
   - Check: `ros2 topic info /joint_states`
   - Answer: Yes! Subscription count > 1

---

## Part 5: Key Concepts Summary

### Publish-Subscribe Pattern

**Publisher:**
- A node that **sends** data to a topic
- Doesn't know who's listening
- Example: `/joint_state_publisher_gui`

**Subscriber:**
- A node that **receives** data from a topic
- Doesn't know who's sending
- Example: `/robot_state_publisher`

**Topic:**
- A named **channel** for communication
- Has a specific message **type**
- Can have multiple publishers and subscribers
- Example: `/joint_states` (type: sensor_msgs/msg/JointState)

---

### Why This Design?

**Advantages:**
1. **Loose coupling** - Nodes don't need to know about each other
2. **Modularity** - Can add/remove nodes without breaking the system
3. **Reusability** - Multiple nodes can use the same data
4. **Testing** - Can replace real nodes with test nodes easily

**Example:**
- Want to record joint positions? Add a node that subscribes to `/joint_states`
- Want to control joints differently? Replace `joint_state_publisher_gui` with your own node
- System keeps working because the **topic interface stays the same**

---

## Part 6: Common Commands Reference

### Node Commands
```bash
# List all running nodes
ros2 node list

# Get info about a specific node
ros2 node info /joint_state_publisher_gui

# See what topics a node publishes/subscribes to
ros2 node info /robot_state_publisher
```

### Topic Commands
```bash
# List all active topics
ros2 topic list

# Show topic information
ros2 topic info /joint_states

# Echo (print) topic messages
ros2 topic echo /joint_states

# Show only specific fields
ros2 topic echo /joint_states --field position

# Check publish frequency
ros2 topic hz /joint_states

# See topic message type structure
ros2 interface show sensor_msgs/msg/JointState
```

### Visualization Commands
```bash
# Show node/topic graph
rqt_graph

# Launch full RQt suite (many tools)
rqt
```

---

## Part 7: Troubleshooting

### Graph is Empty

**Problem:** rqt_graph shows nothing

**Solution:**
1. Make sure view_mp2.launch.py is running
2. Click the refresh button (circular arrow)
3. Check dropdown settings:
   - Set to "Nodes/Topics (all)"
   - Uncheck "Hide: Dead sinks"

---

### No Data in Topic Echo

**Problem:** `ros2 topic echo /joint_states` shows nothing

**Solutions:**
1. **Check if topic exists:**
   ```bash
   ros2 topic list | grep joint_states
   ```

2. **Check if anyone is publishing:**
   ```bash
   ros2 topic info /joint_states
   # Should show "Publisher count: 1" or more
   ```

3. **Verify GUI is running:**
   ```bash
   ros2 node list | grep joint_state_publisher_gui
   ```

---

### "Package not found" Error

**Problem:** `ros2 launch mini_pupper_description view_mp2.launch.py` fails

**Solution:** You didn't source your workspace!
```bash
source ~/sfkrobotics_ws/install/setup.bash
```

Add to `~/.bashrc` to do automatically:
```bash
echo "source ~/sfkrobotics_ws/install/setup.bash" >> ~/.bashrc
```

---

## Part 8: Advanced Exploration

### Record and Replay Data

**Record joint movements:**
```bash
ros2 bag record /joint_states
```

Move sliders, then press `Ctrl+C` to stop recording.

**Replay recorded data:**
```bash
ros2 bag play rosbag2_<timestamp>
```

The robot will move exactly as you recorded!

---

### Create Your Own Publisher

**Challenge:** Write a simple Python node that publishes fake joint states!

See [ROS2 Tutorials](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html) for examples.

---

### Visualize TF Tree

See the coordinate frame tree:
```bash
ros2 run tf2_tools view_frames
```

Opens a PDF showing how all the robot parts are connected geometrically.

---

## Learning Checkpoints

Students should now be able to:

**Identify nodes and topics** in rqt_graph
**Trace data flow** from publisher to subscriber
**Monitor live topic data** using `ros2 topic echo`
**Observe real-time changes** as robot joints move
**Understand the publish-subscribe pattern**
**Use ros2 CLI tools** to inspect the system
**Explain why ROS2 uses topics** for communication

---

## Next Steps

After mastering nodes and topics, students can explore:
- **Services** - Request-response communication
- **Actions** - Long-running tasks with feedback
- **Parameters** - Dynamic configuration
- **Launch files** - Starting multiple nodes together
- **Writing custom nodes** - Creating your own publishers/subscribers

---

## Additional Resources

- [ROS2 Documentation](https://docs.ros.org/en/humble/)
- [Understanding Nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html)
- [Understanding Topics](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
- [URDF Guide](URDF_Guide.md) - Understanding robot structure
- [Gazebo Simulation Guide](../../mini_pupper_simulation/docs/Gazebo_Simulation_Guide.md) - Running full simulation

---

**Last Updated:** 2025-12-31
**ROS2 Version:** Humble
**Robot Model:** Mini Pupper 2
