# Introduction
Arena-rosnav-3D is structurally very similar to arena-rosnav to allow easy switching between 2D and 3D environments. Currently, three custom worlds and a random world generator are supported. In our detailed custom worlds you can generate dynamic obstacles either in a scenario mode or in a random mode where the obstacle trajectories are determined randomly. 

# Worlds
We provide the following four worlds for your use: 
|<img width="250" height="240" src="/img/aws_house-2.png">|<img width="250" height="240" src="/img/turtlebot3_house.png">|<img width="250" height="240" src="/img/small_warehouse-2.png">|<img width="250" height="240" src="/img/outside.png">|
|:--:       |              :--:|             :--:|          :--:| 
| *aws_house* | *turtlebot3_house* | *small_warehouse* | *random world* |
## Pre-build world
To select one of our pre-build worlds, specify your scenario by selecting **aws_house**,  turtlebot3_house, small_warehouse *(bold is your default world)* in your startup file:
```bash
roslaunch arena_bringup start_arena_gazebo.launch world:=turtlebot3_house
```
Since our pre-build worlds are very detailed we do not spawn further static obstacles. For obstacle and robot task-management see [here](#task-mode). 

To implement your own custom world file see [here](/docs/Miscellaneous.md#How-to-include-further-world-files)

## Random world
To select our custom world generator specify the outside argument with `true` (default is false)
```bash
roslaunch arena_bringup start_arena_gazebo.launch outside:=true
```
The custom world generator creates a map with a set number of static and dynamic obstacles of a randomly determined size (and shape).

If you want to change the number of static obstacles you do this [here](https://github.com/eliastreis/arena-rosnav-3D/blob/18ed507bfbf31015002c5727f2ab9aef3a05ca9b/task_generator/task_generator/tasks.py#L304)

If you want to change the number of dynamic obstacles you do this [here](https://github.com/eliastreis/arena-rosnav-3D/blob/18ed507bfbf31015002c5727f2ab9aef3a05ca9b/task_generator/task_generator/tasks.py#L26)

---
# Task-Mode
We currently support a random and a dynamic mode (you can also set the robot goal manually using Rviz).

Select either **random** or scenario and run:
```bash
roslaunch arena_bringup start_arena_gazebo.launch task_mode:=random
```
## Random Mode
In random mode arena-rosnav chooses the robot start and goal position, as well as the trajectory of the dynamic obstacles randomly. 

If you want to change the number of dynamic obstacles you do this [here](https://github.com/eliastreis/arena-rosnav-3D/blob/18ed507bfbf31015002c5727f2ab9aef3a05ca9b/task_generator/task_generator/tasks.py#L26)

Find the associated code [here](https://github.com/eliastreis/arena-rosnav-3D/blob/18ed507bfbf31015002c5727f2ab9aef3a05ca9b/task_generator/task_generator/tasks.py#L104).
## Scenario Mode
In scenario mode, object obstacle and robot behavior is scripted. We support currently one scenario per world. To extend this and build your own custom scenarios see [here](/docs/Miscellaneous.md#How-to-include-further-scenarios).

Find the associated code [here](https://github.com/eliastreis/arena-rosnav-3D/blob/18ed507bfbf31015002c5727f2ab9aef3a05ca9b/task_generator/task_generator/tasks.py#L245).

---
# Local Planer
local_planner ToDo

---
# Advanced Parameters
You can further customize the simulation altering the following parameters:

| Name  | Options   | Description   |
|:--:   | :--:      | :--:          |  
| train_mode | true, **false** | Since training mode is not yet implemented `false` should stay selected. (This would deactivate e.g. the task_generator) |
| disable_scenario | true, **false** | This parameter would e.g. disable the task generator and other selected notes. This should only be changed with caution |
| reset | **true**, false | Determines whether the scenario should be reset (or terminated) after reaching its objective (Robot has reached navigation goal) |
| enable_pedsim | **true**, false | Pedsim is used to for dynamic obstacle management. Setting this to false should disable dynamic obstacles |
ToDo
---

  # List of all Parameters
  ```xml
  <arg name="train_mode"        default="false"/>
  <arg name="local_planner"     default="dwa"         doc = "local_planer type [tep, dwa, rlca]"/>
  <arg name="rviz_file"         default="nav_LP"/>
  <arg name="disable_scenario"  default="false"/>
  <arg name="reset"             default="true"/>
  <arg name="enable_pedsim"     default="true"/>
  <arg name="outside"           default="false"/>
  <arg name="world"             default="aws_house"   unless="$(arg outside)"/>
  <arg name="world"             default="outside"     if="$(arg outside)"/>
  <arg name="model"             default="burger" 
  <arg name="scenario_file"     default="$(arg world).json"/>
  <arg name="step_size"         default="0.01"/>
  <arg name="update_rate"       default="250"/>
  <arg name="show_viz"          default="true"/>
  <arg name="viz_pub_rate"      default="30" />
  <arg name="use_rviz"          default="true"/>
  <arg name="map_path"          default="$(find simulator_setup)/maps/map_$(arg world)/map.yaml" />
  <arg name="task_mode"         default="random"/> 
  <arg name="obs_vel"           default="0.3" />
  <arg name="action_frequency"  default="10"/>
  <arg name="global_frame_id"   value="map"/>
  <arg name="odom_frame_id"     value="odom"/>
  <arg name="base_frame_id"     value="base_footprint"/>
  <arg name="odom_ground_truth" default="/odometry/ground_truth"/>
  ```