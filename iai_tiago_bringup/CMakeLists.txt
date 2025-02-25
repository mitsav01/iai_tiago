cmake_minimum_required(VERSION 3.5)
project(iai_tiago_bringup)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY configs launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()