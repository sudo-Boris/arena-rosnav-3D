# arena-rosnav-3D

This repository combines the 3D ROS simulator Gazebo with Pedsim to provide realistic dyanmic 3D scenarios and tasks to evaluate and and benchmark ROS navigation approaches. It is fully compatible with the planning algorithms trained and developed with arena-rosnav (2D). This presents an essential step in deploying the navigation approaches from arena-rosnav towards real robots.

The repo currently contains:

- Task generator with 3 modes: random, scenario and manual tasks
- Multiple detailed scenario-worlds
- Different robot models
- Creation of random 3D-words with static and dynamic obstacles
- Realistic behavior patterns and semantic states of dynamic obstacles (by including pedsim's extended social force model)
- Implementation of intermediate planner classes to combine local DRL planner with global map-based planning of ROS Navigation stack
- Testing a variety of planners (learning based and model based) within specific scenarios
- Integration with [arena-tools](https://github.com/ignc-research/arena-tools) map generator and [LIRS-World_Construction_Tool](https://gitlab.com/LIRS_Projects/LIRS-WCT). Providing seamless conversion from randomly generated ROS maps to actual Gazebo worlds.
- "Random world" task mode, where with each Task reset, a new Gazebo world is loaded
- Modular structure for extension of new functionalities and approaches

## 1. Installation

Please refer to [Installation.md](docs/Installation.md) for detailed explanations about the installation process.

## 2. Usage

Please refer to [Usage.md](docs/Usage.md) for detailed explanations about agent, policy and training setups.

**Sample usage**

After successful installation, run the following command with your python-env activated (`workon rosnav`).

```bash
roslaunch arena_bringup start_arena_gazebo.launch local_planner:=teb task_mode:=random world:=small_warehouse actors:=6 
```
## 3. Examples

### Random mode
https://user-images.githubusercontent.com/41898845/135458175-eb1634a9-f1e4-48d1-9696-b5248bcc5718.mp4

### Arena Generated

https://user-images.githubusercontent.com/41898845/135459990-dac33393-76a6-4173-8abe-fc25d0b95643.mp4


### Scenario mode

- Use the supplied scenario or create your own using [arena-tools](https://github.com/ignc-research/arena-tools).
- In scenario mode, all objects will be spawned at their specified position and everything will reset back to this position once the robot reaches its goal.

https://user-images.githubusercontent.com/41898845/135480113-e5ae02bf-5268-45b8-be29-011be0e65c61.mp4


### Training

**_Arena-Rosnav's training functionality is not yet included_**

## Miscellaneous

- [How to include further world files](docs/Miscellaneous.md#How-to-include-further-world-files)
- [How to create more world files](docs/Miscellaneous.md#How-to-create-more-world-files)
- [How to speed-up gazebo simulation speed](docs/Miscellaneous.md#How-to-speed-up-gazebo-simulation-speed)
- [How to include further scenarios](docs/Miscellaneous.md#How-to-include-further-scenarios)
- [Further improvement ideas](docs/project_report.md#Open-topics)
- [Detailed description of changes to arena-rosnav](docs/project_report.md) (currently in progress)

# Used third party repos:

- ROS navigation stack: http://wiki.ros.org/navigation
- Pedsim: https://github.com/srl-freiburg/pedsim_ros
- Small-warehouse world: https://github.com/aws-robotics/aws-robomaker-small-warehouse-world
- Small-house world: https://github.com/aws-robotics/aws-robomaker-small-warehouse-world
- Turtlebot3-robot & house-world: https://github.com/ROBOTIS-GIT/turtlebot3_simulations
- LIRS_World_Construction_Tool https://gitlab.com/LIRS_Projects/LIRS-WCT
- ros_maps_to_pedsim https://github.com/fverdoja/ros_maps_to_pedsim
