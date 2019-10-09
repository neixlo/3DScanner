'''
scanner.py is the script to to coordinate the image shooting process with the control of the stepper motor via stepper.py and the camera over an seperate serial interface. 
'''

import stepper
import gphoto2 as gp
import os
import time
import subprocess

class scanner:
    def __init__(self):
        try:
            self.camera = gp.check_result(gp.gp_camera_new())
            gp.check_result(gp.gp_camera_init(self.camera))
            print('Camera initialized.\n')
        except:
            print('ERROR: Seems that you need to unmount your camera before using it via this interface. \n To unmount the camera: Open your file system / explorer, go to Devices and click the "unmount" icon to the right of the camera device.')
        try:
            self.stp = stepper.stepper()
            self.stp.on()
            print('\nScanner fully initialized.\n')
        except:
            print("ERROR: Can't initialize stepper motor")
                
    def cam_shot(self, target_dir, name):
        photo = gp.check_result(gp.gp_camera_capture(self.camera, gp.GP_CAPTURE_IMAGE))
        path = os.path.join(target_dir, name+'.JPEG')
        print('Copying image to', path)
        camera_file = gp.check_result(gp.gp_camera_file_get(self.camera, photo.folder, photo.name, gp.GP_FILE_TYPE_NORMAL))
        gp.check_result(gp.gp_file_save(camera_file, path))
        
    def show_photo(self, path):
        subprocess.call(['xdg-open', path])
      
    def start(self):
        self.stp = stepper.stepper()
        self.stp.on()

    def end(self):
        self.stp.off()
        self.stp.disconnect_serial()
        print('Serial connection closed.')

    def scan360(self, target_dir, filename, deg_steps):
        cnt_img = int(360/deg_steps)
        for s in range(1, cnt_img+1):
            name = str(filename + '_{}').format(deg_steps*s)     
            self.stp.move_to(deg_steps*s)
            time.sleep(0.25)
            self.cam_shot(target_dir, name)

        self.stp.reset()

    def scan_process(self, directory, obj_name, deg_steps):
        main_dir = os.path.abspath(os.curdir)
        directory = os.path.join(directory, obj_name)
        target_dir = os.path.join(os.path.abspath(directory), 'photos')
        
        if not os.path.exists(directory):
            os.makedirs(directory)
            os.chdir(directory)
            os.mkdir('3d_obj')
            os.mkdir('photos')
        else:
            return "ERROR: \n Can't create directory. This directory might exist already."

        while True:
            
            print('\n')
            pos_name = input('Enter a name for the scanning position:')
            print('\n')

            os.chdir(target_dir)
            os.mkdir(pos_name)
            pos_dir = os.path.join(target_dir, pos_name)
            self.scan360(pos_dir, obj_name, deg_steps)

            print('\n')
            background = input('Ready to take a backgound photo? (y/n)')
            print('\n')
            
            if background == 'y':
                self.cam_shot(pos_dir, 'background')
            elif background == 'n':
                pass
            
            print('\n')
            cont = input('Continue with another 360deg scan? (y/n)')
            print('\n')
            
            if cont == 'y':
                pass
            elif cont == 'n': 
                break
        os.chdir(main_dir) # return to main dir
        print("Finished scan.")
            
    def scanX(self, target_dir, filename, deg_step):
        step = int(deg_step)
        name = str(filename + '_{}').format(step) 
        self.stp.move_to(step)
        time.sleep(0.25)
        self.cam_shot(target_dir, name)


