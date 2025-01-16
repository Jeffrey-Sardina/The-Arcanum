import cv2

"""
Based on: https://stackoverflow.com/questions/57577445/list-available-cameras-opencv-python
"""
if __name__ == '__main__':
    working_ids = []
    for id_to_test in range(100): # I think these only go up to 99?
        id_works = True
        camera = cv2.VideoCapture(id_to_test)
        
        # see if we can start the camera
        if not camera.isOpened():
            id_works = False
            continue
        
        # see if we can read data from the camera
        is_reading, img = camera.read()
        w = camera.get(3)
        h = camera.get(4)
        if not is_reading:
            id_works = False
        
        # print ID if it works
        if id_works:
            working_ids.append(id_to_test)
    
    print()
    print('ERROR / WARN messages above are ok to ignore')
    print('Working camera IDs:')
    print(working_ids)
