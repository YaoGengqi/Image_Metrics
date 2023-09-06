import os
import shutil

if __name__ == '__main__':
    
    root = 'REDS4'

    dirs = os.listdir(root)
    
    for dir in dirs:

        if dir[:3] == '000':
            continue

        files = os.listdir(os.path.join(root, dir))

        for file in files:
            if int(file[:-4]) in [10, 30, 50, 70, 90]:
                src = os.path.join(root, dir, file)
                dst = os.path.join(root, dir, dir + '_' + file)
                os.rename(src, dst)
                src, dst = dst, os.path.join(root, dir + '_' + file)
                shutil.move(src, dst)
                print(src, '->', dst)