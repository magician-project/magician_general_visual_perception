cmake_minimum_required(VERSION 3.5)
project(magician_general_visual_perception)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  ymapnet_node.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()

