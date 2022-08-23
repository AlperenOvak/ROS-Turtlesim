#!/usr/bin/env python3

import rospy
from first_pkg.srv import GiveLocation,GiveLocationResponse
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math


x=0
y=0
yaw=0

def takepose(pose_message): ### pose sub function
    global x, y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta
    
x_goal=0
y_goal=0

def give_location_client(): ### client function
    rospy.wait_for_service('give_location')
    try:
        give_location = rospy.ServiceProxy('give_location', GiveLocation)
        resp1 = give_location()
        return resp1
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


    


def go_to_goalpose():
    rospy.init_node("controller", anonymous=True)
    global x, y, yaw,x_goal, y_goal

    location=give_location_client()
    x_goal=location.x
    y_goal=location.y

    ### Fetch required rosparams
    distance=rospy.get_param("/distance")
    max_linear_velocity=rospy.get_param("/max_linear_velocity")
    max_angular_velocity=rospy.get_param("/max_angular_velocity")
    delta=rospy.get_param("/delta")

    velocity_message = Twist()
    
    target_counter=0

    rate=rospy.Rate(2)

    while True:
        #OUR MOVEMENT COMMANDS
            ##Linear Speed
        K_linear = 0.4
        cur_distance = abs(math.sqrt((((x_goal - x) ** 2) + ((y_goal - y) ** 2))))
        linear_speed = cur_distance * K_linear
            ##Angular Speed
        K_angular = 4.0
        desired_angle_goal = math.atan2(y_goal - y, x_goal-x)
        angular_speed = (desired_angle_goal - yaw) * K_angular
            ##Speed Limiter
        if linear_speed>max_linear_velocity:
            linear_speed=max_linear_velocity
        if angular_speed>max_angular_velocity:
            angular_speed=max_angular_velocity
            ## Publishing the linear and angular speed
        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed
        velocity_publisher.publish(velocity_message)
        #

        ##Float equality
        strdel=str(delta) 
        prec=len(strdel.split('.')[1])
        cur_distance=round(cur_distance,prec)

        print("distance= %s *** Goal=(%s,%s)"%(cur_distance,x_goal,y_goal))

        if (cur_distance <= distance): #Arrived the current goal
            
            location=give_location_client()
            x_goal=location.x
            y_goal=location.y
            target_counter+=1
            rate.sleep() 

        if target_counter==6: #Our turtle arrived all goals
            break
          
        


if __name__=="__main__":
    try:
        velocity_publisher = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
        pose_subscriber = rospy.Subscriber("/turtle1/pose", Pose, takepose)
        go_to_goalpose()
        
    except rospy.ROSInterruptException:
        pass

