import subprocess
import sys
import os

from pathlib import Path
from Utilities import Task

def Setup():

    print("Updating the C++ environment")

    buildPath = Path().absolute() / "Build"
    buildPathString = str(buildPath)

    conanFilePath = Path().absolute() / "Tools" / "Conan"
    conanFilePathString = str(conanFilePath)

    #Set the conan remote
    Task("conan", "remote", "add", "--force", "bincrafters", "https://api.bintray.com/conan/bincrafters/public-conan")

    #Create build directory if it does not exist
    if not os.path.exists(buildPath):
        os.makedirs(buildPath)

    #install conan dependencies
    Task("conan", "install", conanFilePathString, "-if", buildPathString,"-l", conanFilePathString, "-s", "build_type=Debug")
    Task("conan", "install", conanFilePathString, "-if", buildPathString,"-l", conanFilePathString, "-s", "build_type=Release")

    print("Finished setup")