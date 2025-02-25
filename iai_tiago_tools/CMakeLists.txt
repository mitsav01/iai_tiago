cmake_minimum_required(VERSION 3.5)
project(iai_tiago_tools)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

install(DIRECTORY
        script
        DESTINATION share/${PROJECT_NAME}/)
      
install(PROGRAMS
        script/giskard_e_stop.py
        DESTINATION lib/${PROJECT_NAME})

ament_package()