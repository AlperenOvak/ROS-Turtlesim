#!/usr/bin/env python3

from first_pkg.srv import GiveLocation,GiveLocationResponse
import rospy

### Fetch required rosparam
waypoints=rospy.get_param("/waypoints")

i=0
x=0
y=0

def handle_give_location(target_num): #Server function
    global x,y,i,waypoints,s
    if i==6:
        print("Arrived")
        return GiveLocationResponse(x,y)
    x=waypoints[i][0]  #We know that our rosparam is a list. Moreover, it contains another lists
    y=waypoints[i][1]  #Thus, we can reach x and y like that
    print(i)
    i+=1 # i goes up when our turtle reach the target 
    print("Returning %s Location %s,%s]"%(target_num,x,y))
    return GiveLocationResponse(x,y)

def give_location_server():
    global i,s
    rospy.init_node('Give_Location_Server')
    s = rospy.Service('give_location', GiveLocation, handle_give_location)
    print("Ready to add target_num.")     
    rospy.spin()

if __name__ == "__main__":
    give_location_server()


