cmake_minimum_required(VERSION 3.5)
project(iai_tiago_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY urdf launch rviz2
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
