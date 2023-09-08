#does fcvapp work as a module? We'll see...

import sys

if hasattr(sys, "_MEIPASS"):
    # if file is frozen by pyinstaller add the MEIPASS folder to path:
    #FCVA_update_resources has the sys.path.append(sys._MEIPASS)
    pass
else:
    # if you're making your own app, you don't need this else block. This is just vanity code so I can run this from main FastCVApp folder or from the examples subfolder.
    # this example is importing from a higher level package if running from cmd: https://stackoverflow.com/a/41575089
    import os

    # add the right path depending on if you're running from examples or from main folder:
    if "examples" in os.getcwd().split(os.path.sep)[-1]:
        sys.path.append(
            ".."
        )  # when running from examples folder, append the upper level
    elif "examples" not in os.getcwd().split(os.path.sep)[-1]:
        # assume they're in main folder trying `python examples/example_backgroundsubtraction.py`
        sys.path.append("../FastCVApp")  # when running from main folder
        import site
        site_packages_dirs = site.getsitepackages()
        print(site_packages_dirs)
        sys.path.append(os.path.join(*site_packages_dirs, "FastCVApp"))

print(sys.path)

#     else:
#         sys.path.append(os.path.dirname(FastCVApp.__file__))
# import os, FastCVApp
# sys.path.append(os.path.dirname(FastCVApp.__file__))

# https://sparkbyexamples.com/python/find-the-location-of-python-site-packages-directory/#:~:text=A%20quick%20way%20to%20find,%E2%80%9Csite%2Dpackages%E2%80%9D%20directory.
# Import site module
# import site

# # # Get the list of directories 
# site_packages_dirs = site.getsitepackages()
# print()
# # Find the "site-packages" directory in the list
# for dir in site_packages_dirs:
#     if dir.endswith("site-packages"):
#         target_dir = dir
#         break
#     else:
#         target_dir=None
# # print(target_dir)
# target = os.path.join(target_dir, "fastCVApp")
# print(target)
# sys.path.append(target)


from FastCVApp.FCVAutils import FCVA_update_resources
sourcelocation = os.path.join("examples", "creativecommonsmedia", "Elephants Dream charstart2FULL_265.mp4") 
FCVA_update_resources(sourcelocationVAR=sourcelocation)
print("this worked???")
import cv2

from collections import deque


def identity_func(*args):
    try:
        inputdeque = args[0]
        # FCVAWidget_shared_metadata_dictVAR3 = args[1]
        bufferlenVAR = args[2]
        answerdeque = deque(maxlen=bufferlenVAR)
        landmarkerVAR = args[3]
        raw_dequeKEYSVAR = args[4]
        force_monotonic_increasingVAR = args[5]

        #you can even just return the inputdeque but showing this for consistency with examples        
        while len(inputdeque) > 0:
            image = inputdeque.popleft()
            #do literally nothing, identity maps an obj to itself
            answerdeque.append(image)
        return answerdeque

    except Exception as e:
        print("identity_func subprocess died! ", e, flush=True)

# from fastapi import FastAPI

if __name__ == "__main__":
    # import FastCVApp
    # pathguy = os.path.dirname(FastCVApp.__file__)
    # print(pathguy)
    # sys.path.append(pathguy)
    # print(sys.path)
    # print("what is modulename really? it better be a pathname...", FastCVApp, FastCVApp.__file__)
    # print(dir(FastCVApp))
    from FastCVApp import FastCVApp
    app = FastCVApp.FCVA()
    # app = FastCVApp.FCVA()

    app.appliedcv = identity_func
    # / and \ works on windows, only / on mac tho 
    # C:\Personalize\CODING\FastCVApp\fastcvapp\examples\creativecommonsmedia\Elephants Dream charstart2FULL.webm
    # C:\Personalize\CODING\FastCVApp\FastCVApp\examples\creativecommonsmedia\Elephants Dream charstart2.webm
    app.source = sourcelocation
    # app.source = "examples/creativecommonsmedia/Elephants Dream charstart2FULL.webm"
    # app.source = "examples/creativecommonsmedia/Elephants Dream charstart2.webm"
    # app.source = "examples/creativecommonsmedia/JoJo-s Bizarre Adventure - S05E25 - DUAL 1080p WEB H.264 -NanDesuKa (NF) (1).1080.mp4"
    app.fps = 1 / 30
    app.title = "Identity example by Pengindoramu"
    app.run()
