'''
3Dscanner.py is the PC serial interface to my initial scanning rig setup

Dependencies:
- python                    3.6.6
- pyserial                  3.4
- gphoto2                   1.8.5

Access via command line:
nixi@nixis ~ $                      source activate 3D_scanning_env
(3D_scanning_env) nixi@nixis ~ $    python
>>>                                 import scanner
>>>                                 sc = scanner.scanner()
>>>                                 sc.cam_shot('filepath', 'filename')
>>>                                 sc.scan360('target_dir', 'filename', 'deg_steps')
>>>                                 sc.scan_process('directory', 'obj_name', 'deg_steps')




todo:
-init
-main
-class serial interface
-arguments to control from command line

'''


'''
import ------------------------------------------------------------
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
        path = os.path.join(target_dir, name)
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

        directory = os.path.join(directory, obj_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
            os.chdir(directory)
            os.mkdir('3d_obj')
            os.mkdir('photos')
        else:
            return "ERROR: \n Can't create directory."

        target_dir = os.path.join(directory, 'photos')
        
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
        print("Finished scan.")
            
    def scanX(self, target_dir, filename, deg_step):
        step = int(deg_step)
        name = str(filename + '_{}').format(step) 
        self.stp.move_to(step)
        time.sleep(0.25)
        self.cam_shot(target_dir, name)

    def moveX(self, deg_steps):
        print('tbd')
        

'''
main ------------------------------------------------------------
'''






if __name__ == '__main__':
    print('tbd')
    #main()



