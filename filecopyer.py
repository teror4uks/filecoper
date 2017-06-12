import os
import time
import shutil

class CopyFiler:
    def __init__(self, dir1, dir2, dst):
        self.dir1 = {}
        self.dir2 = {}
        self.queue = None
        self.dir1['path'] = dir1
        self.dir2['path'] = dir2
        self.dst = dst
        self.dir1['list'] = self._file_pathes(self.dir1['path'])
        self.dir2['list'] = self._file_pathes(self.dir2['path'])
        self.dir1['length_list'] = len(self.dir1['list'])
        self.dir2['length_list'] = len(self.dir2['list'])


    def run(self):
        self.check_folders()

    def check_folders(self):
        file_for_copies_in_dir1 = ""
        file_for_copies_in_dir2 = ""
        temp = self._file_pathes(self.dir1['path'])
        l = temp - self.dir1['list']
        if len(l) != 0:
            file_for_copies_in_dir1 = list(l)[0]

        temp = self._file_pathes(self.dir2['path'])
        l = temp - self.dir2['list']
        if len(l) != 0:
            file_for_copies_in_dir2 = list(l)[0]

        if len(file_for_copies_in_dir1) != 0 and len(file_for_copies_in_dir2) != 0 :
            biggest_file = self.get_biggest_file(file_for_copies_in_dir1, file_for_copies_in_dir2)
            print(biggest_file)
            locked = self.check_file(biggest_file)

            if not locked:
                shutil.copy2(biggest_file, self.dst)
            else:
                return

            self.dir1["list"].add(file_for_copies_in_dir1)
            self.dir2["list"].add(file_for_copies_in_dir2)
            self.upd_lenght()
            print(self.dir1)
            print(self.dir2)


    def upd_lenght(self):
        self.dir1['length_list'] = len(self.dir1['list'])
        self.dir2['length_list'] = len(self.dir2['list'])

    def check_file(self, file):
        locked = None
        file_object = None
        try:
            print("Trying to open %s." % file)
            buffer_size = 8
            # Opening file in append mode and read the first 8 characters.
            file_object = open(file, 'a', buffer_size)
            if file_object:
                print("%s is not locked." % file)
                locked = False
        except IOError as why:
            print("File is locked (unable to open in append mode). %s." % why)
            locked = True
        finally:
            if file_object:
                file_object.close()
                print("%s closed." % file)

        return locked


    def get_biggest_file(self, f1 , f2):
        s1 = os.path.getsize(self.dir1['path'] + os.sep + f1)
        s2 = os.path.getsize(self.dir2['path'] + os.sep + f2)
        if s1 >= s2:
            return self.dir1['path'] + os.sep + f1
        else:
            return self.dir2['path'] + os.sep + f2

    def copy_file(self):
        pass

    def _file_pathes(self, path):
        res = []
        for root, directories, files in os.walk(path):
            for file in files:
                reldir = os.path.relpath(root, path)
                filepath = os.path.join(reldir, file)
                res.append(filepath)

        return set(res)

if __name__ == "__main__":
    t = CopyFiler("/home/administrator/PycharmProjects/filecopyer/dir1",
                  "/home/administrator/PycharmProjects/filecopyer/dir2",
                  "/home/administrator/PycharmProjects/filecopyer/dir3")

    while True:
        t.run()
        time.sleep(5)

    print(t.dir1)
    print(t.dir2)
    print(t.dir1['list'] - t.dir2['list'])


