cmake_minimum_required(VERSION 3.15.2  FATAL_ERROR)

#Set CMake tools location
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/Tools/CMake)

#Global Options
set(CMAKE_FIND_PACKAGE_PREFER_CONFIG ON)# Opposite module/PCF order for `find_package`

include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

##############################################
#Project 

project(SoulEditor
	VERSION 0.0.1
	DESCRIPTION "Soul Engine editor and project interface."
	LANGUAGES CXX
)


##############################################
#Dependencies

find_package("SoulEngine")


##############################################
#Targets

add_executable(${PROJECT_NAME} "")

set_target_properties(${PROJECT_NAME} 
    PROPERTIES 
        LINKER_LANGUAGE CXX
        CXX_EXTENSIONS OFF  
        CXX_STANDARD 20
        USE_FOLDERS ON
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        synodic::SoulEngine
)

##############################################
#Sources

file(GLOB_RECURSE SOURCES CONFIGURE_DEPENDS Source/*)

target_sources(${PROJECT_NAME}
    PRIVATE
        ${SOURCES}
)

#Provides Visual Studio filter support
get_target_property(PROJECT_SOURCES ${PROJECT_NAME} SOURCES)
source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR} FILES ${PROJECT_SOURCES})


##############################################
#Installation

#TODO: Proper resource handling via Conan probably. No need to pass around all these janky files
add_custom_command( TARGET ${PROJECT_NAME} 
                    POST_BUILD
                    COMMAND ${CMAKE_COMMAND} -E copy_directory 
                    ${CONAN_USER_SOULENGINE_ENGINE_PATH}/Resources
                    ${CMAKE_BINARY_DIR}/Resources)