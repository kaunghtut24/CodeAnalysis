import os
for root, dirs, files in os.walk("."):
    for name in dirs + files:
        print(os.path.join(root, name))