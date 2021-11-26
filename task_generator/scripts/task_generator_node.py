#! /usr/bin/env python3

import rospkg
import rospy
import time
from nav_msgs.msg import Odometry
from task_generator.tasks import get_predefined_task
from std_msgs.msg import Int16, String
from nav_msgs.msg import Odometry
from nav_msgs.srv import LoadMap
from std_srvs.srv import Empty
# from pedsim_srvs.srv import SetObstacles
from gazebo_msgs.srv import SetModelState, SpawnModelRequest, SpawnModel, DeleteModel
import subprocess

# for clearing costmap
from clear_costmap import clear_costmaps
import pathlib
import re


class TaskGenerator:
    def __init__(self):

        self.sr = rospy.Publisher('/scenario_reset', Int16, queue_size=1)
        self.nr = 0
        mode = rospy.get_param("~task_mode")

        scenarios_json_path = rospy.get_param("~scenarios_json_path")
        paths = {"scenario": scenarios_json_path}
        self.task = get_predefined_task("", mode, PATHS=paths)
        self.rospack = rospkg.RosPack()

        # if auto_reset is set to true, the task generator will automatically reset the task
        # this can be activated only when the mode set to 'ScenarioTask'
        auto_reset = rospy.get_param("~auto_reset")
        self.start_time_ = time.time()

        self.arena_gen = rospy.get_param("~world") == "arena_generated"

        # arena generated mode
        if (self.arena_gen):
            self.load_map_service_client = rospy.ServiceProxy(
                "change_map", LoadMap)
            set_obstacles_service_name = "pedsim_simulator/set_obstacles"
            rospy.wait_for_service(set_obstacles_service_name, 6.0)
            self.pedsimMap_client_ = rospy.ServiceProxy(
                set_obstacles_service_name, SetObstacles)
            self.spawn_map_client = rospy.ServiceProxy(
                '/gazebo/spawn_sdf_model', SpawnModel)
            folder = pathlib.Path(self.rospack.get_path(
                "simulator_setup") + '/maps/')
            map_folders = [p for p in folder.iterdir() if p.is_dir()]
            names = [p.parts[-1] for p in map_folders]
            # get only the names that are in the form of f"map{index}"
            prefix = "map"
            pat = re.compile(f"{prefix}\d+$", flags=re.ASCII)
            self.filtered_names = [
                name for name in names if pat.match(name) != None]
            new_map = self.filtered_names.pop()
            map_yaml = folder / new_map / "map.yaml"

            self.load_map_service_client(str(
                map_yaml))
            request = SpawnModelRequest()
            f = open(self.rospack.get_path(
                "simulator_setup") + "/models/" + new_map + "/model.sdf")
            request.model_xml = f.read()
            request.model_name = "map"
            self.spawn_map_client(request)
            self.pedsimMap_client_(new_map)
        # if the distance between the robot and goal_pos is smaller than this value, task will be reset
        # self.timeout_= rospy.get_param("~timeout")
        self.timeout_ = rospy.get_param("~timeout", 2.0)
        self.timeout_ = self.timeout_*60             # sec
        self.start_time_ = time.time()                # sec
        self.delta_ = rospy.get_param("~delta")
        robot_odom_topic_name = rospy.get_param(
            "robot_odom_topic_name", "odom")

        auto_reset = auto_reset and (mode == "scenario" or mode == "random")
        self.curr_goal_pos_ = None

        if auto_reset:
            rospy.loginfo(
                "Task Generator is set to auto_reset mode, Task will be automatically reset as the robot approaching the goal_pos")
            self.reset_task()
            self.robot_pos_sub_ = rospy.Subscriber(
                robot_odom_topic_name, Odometry, self.check_robot_pos_callback)

            rospy.Timer(rospy.Duration(0.5), self.goal_reached)

        else:
            # declare new service task_generator, request are handled in callback task generate
            self.reset_task()
            self.task_generator_srv_ = rospy.Service(
                'task_generator', Empty, self.reset_srv_callback)

        self.err_g = 100

    def goal_reached(self, event):

        if self.err_g < self.delta_:
            print(self.err_g)
            print("reached goal")
            self.reset_task()
        if(time.time()-self.start_time_ > self.timeout_):
            print("timeout")
            self.reset_task()

    def clear_costmaps(self):
        bashCommand = "rosservice call /move_base/clear_costmaps"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print([output, error])

    def reset_srv_callback(self, req):
        rospy.loginfo("Task Generator received task-reset request!")
        self.task.reset()
        # return EmptyResponse()

    def reset_task(self):
        if self.arena_gen and len(self.filtered_names) > 0:
            del_model_prox = rospy.ServiceProxy(
                'gazebo/delete_model', DeleteModel)
            del_model_prox("map")
            new_map = self.filtered_names.pop()
            sim = self.rospack.get_path(
                "simulator_setup")
            self.load_map_service_client(sim + f"/maps/{new_map}/map.yaml")
            request = SpawnModelRequest()
            f = open(sim + f"/models/{new_map}/model.sdf")
            request.model_xml = f.read()
            request.model_name = "map"
            self.spawn_map_client(request)
            self.pedsimMap_client_(new_map)
            clear_costmaps()

        self.start_time_ = time.time()
        info = self.task.reset()

        # set goal position
        if info is not None:
            self.curr_goal_pos_ = info['robot_goal_pos']
        rospy.loginfo("".join(["="]*80))
        rospy.loginfo("goal reached and task reset!")
        rospy.loginfo("".join(["="]*80))
        self.sr.publish(self.nr)
        self.nr += 1

    def check_robot_pos_callback(self, odom_msg):
        # type: (Odometry) -> Any
        robot_pos = odom_msg.pose.pose.position
        robot_x = robot_pos.x
        robot_y = robot_pos.y
        goal_x = self.curr_goal_pos_[0]
        goal_y = self.curr_goal_pos_[1]

        self.err_g = (robot_x-goal_x)**2+(robot_y-goal_y)**2


if __name__ == '__main__':
    rospy.init_node('task_generator')
    rospy.wait_for_service('/static_map')
    task_generator = TaskGenerator()
    rospy.spin()
