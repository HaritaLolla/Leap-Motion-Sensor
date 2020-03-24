# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 12:01:08 2019

@author: HARITA LOLLA

"""
import Leap
import sys


class LeapMotionSensor(Leap.Listener):
    # All the fingers have 4 bones(except the thumb) and 3 links
    all_fingers = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    all_bones = ['Distal Phalanx', 'Middle Phalanx', 'Proxial Phalanx', 'Metacarpals']

    # The controller object has been called first time
    def on_init(self, controller):
        print 'Initiated'   

    def on_connect(self, controller):
        """
        checks if the sensor is connected and lists of all plugged in Leap Motion controller devices.
        Currently, the list will only contain one device, no matter how many are attached to a computer.
        i.e if we print controller.devices[1] then it will return invalid device
        :param controller:
        :return:
        """
        device = controller.devices[0]
        print device

    # The sensor has been disconnected from the PC
    def on_disconnect(self, controller):
        print'Motion sensor is Disconnected'

    # The sensor is plugged in but fails to operate properly
    def on_device_failure(self, controller):
        failed = controller.FailedDevice()
        print failed
        print 'The device has failed to operate, please reconnect or use a new sensor'

    # Tracking data
    def on_frame(self, controller):
        """
        getting the controller properties
        :param controller:
        :return:
        """
        frame = controller.frame()
        fps = frame.current_frames_per_second 
        print fps
        # n is number of bones in a finger
        n = 4
        frameID = "Frame ID:" + str(frame.id)
        timeStamp = 'TimeStamp:' + str(frame.timestamp)
        hands_in_frame = 'Hands:' + str(len(frame.hands))

        for hands in frame.hands:

            # getting the palm and wrist co-ordinates
            palm_cord = 'Palm cordinates:' + str(hands.palm_position)
            wrist_cord = 'Wrist cordinates:' + str(hands.wrist_position)
            print frameID, timeStamp, hands_in_frame

            position = hands.palm_position # 3dcoordinate of the palm center point in mm from the Leap Motion origin
            velocity = hands.palm_velocity # instantaneous motion of the hand in mm/s.
            direc = hands.direction # direction the fingers point from palm center 

            # These functions are defined in the Vector class.
            pitch = 'Pitch:' + str(hands.direction.pitch)  # Pitch - It is the angle around the x-axis ,
            yaw = 'Yaw:' + str(hands.direction.yaw)  # Yaw - It is the angle around the y-axis,
            roll = 'Roll:' + str(hands.palm_normal.roll)  # Roll - It is the angle around the z-axis
            hand_scale_motion = hands.scale_factor(frame) # A positive value representing the heuristically determined scaling change ratio.

            if hands.is_right:
                side = 'Right Hand'
            else:
                side = 'Left Hand'
            print side + ',' + palm_cord + ', ' + wrist_cord
            print 'Postion:'+ str(position) + ', velocity:' + str(velocity)+ ', direction vector:'+str(direc)
            print pitch + ',' + yaw + ',' + roll
            hand_scale_motion = hand.scale_factor(start_frame)

            # Transforming Finger Coordinates into the Hand’s Frame of Reference
            hand_x_basis = hands.basis.x_basis  # The basis orients the x-axis sideways across the hand,
            hand_y_basis = hands.basis.y_basis  # the y-axis parallel with the palm normal.
            hand_z_basis = hands.basis.z_basis  # the z-axis pointing forward,
            hand_origin = hands.palm_position  # The origin of the transform is the palm_position.

            # Transforming Finger coordinates to Hand's Frame of reference.
            hand_transform = Leap.Matrix(hand_x_basis, hand_y_basis, hand_z_basis, hand_origin)
            hand_transform = hand_transform.rigid_inverse()
            print hand_transform

            # getting data for each finger
            for finger in hands.fingers:
                pos = 'Transformed Position:'
                direc = 'Transformed Direction:'
                # getting the finger_type from all_fingers list
                finger_type = self.all_fingers[finger.type]

                # Transform matrix is created using the Leap Matrix class and it transform direction and positions.
                transformed_position = hand_transform.transform_point(finger.tip_position)
                transformed_direction = hand_transform.transform_direction(finger.direction)
                print 'Finger:' + finger_type
                print pos, transformed_position, direc, transformed_direction

                # getting the bone data for each individual finger
                for bones in range(0, n):
                    # getting the bone_type from all_bones list
                    bone_type = str(self.all_bones[finger.bone(bones).type])
                    # getting the direction vector all 4 bones in a finger. For thumb the distal will always be (0,0,0)
                    dir_vec = str(finger.bone(bones).direction)
                    print bone_type, dir_vec

    # New images are available
    def on_images(self, controller):
        print 'New images are available'

    # The controller instance is stopped
    def on_exit(self, controller):
        print "Stopped capturing data from the sensor"


def main():
    listener = LeapMotionSensor()
    controller = Leap.Controller()
    controller.add_listener(listener)

    print "Press Enter to EXIT & [Ctrl+c] to FORCE QUIT"
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()