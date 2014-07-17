import os
def usr_det():
    print(os.getuid())
    print(os.getlogin())
    print(os.getgid())
    print(os.getgroups())
usr_det()
