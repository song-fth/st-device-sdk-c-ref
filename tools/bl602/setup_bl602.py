#!/usr/bin/env python

import sys
import os
import shutil

BSP_NAME = sys.argv[1]
CORE_PATH = os.path.join(os.environ["STDK_CORE_PATH"])
BSP_PATH = os.path.join(os.environ["STDK_REF_PATH"], "bsp", "bl602")
PATCH_PATH = os.path.join(os.environ["STDK_REF_PATH"], "patches", "bl602")

CONFIG_PATH = os.path.join(BSP_PATH, "components", "iot-core_config")

os.chdir(BSP_PATH)
os.system("git submodule update --init --recursive")
os.system("git submodule foreach --recursive git reset --hard")

if os.path.isdir(PATCH_PATH):
    os.chdir(BSP_PATH)
    for patchfile in sorted(os.listdir(PATCH_PATH)):
        if patchfile.endswith(".patch"):
            os.system("git am " + os.path.join(PATCH_PATH, patchfile))

if not os.path.isdir(CONFIG_PATH):
    if os.path.exists(CONFIG_PATH):
        os.remove(CONFIG_PATH)
    os.makedirs(CONFIG_PATH)
cmake_file = open(os.path.join(CONFIG_PATH, "CMakeLists.txt"), "w")
cmake_file.write("idf_component_register()")
cmake_file.close()
shutil.copy(os.path.join(CORE_PATH, "src", "Kconfig"), os.path.join(BSP_PATH, "components", "iot-core_config", "Kconfig"))
