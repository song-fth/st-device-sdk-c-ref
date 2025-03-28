armino_component_register(SRCS "main.c"
                            "device_control.c"
                            "iot_cli_cmd.c"
                            "iot_uart_cli.c"
                            "caps_switch.c"
                    EMBED_FILES "device_info.json"
                                "onboarding_config.json"
                    )

set(PROJECT_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../")
set(STDK_IOT_CORE_USE_DEFINED_CONFIG "y")
set(STDK_CORE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../../../../iot-core")
message(STATUS "Using local path: ${STDK_CORE_PATH}")
add_subdirectory(${STDK_CORE_PATH} iotcore)
target_link_libraries(${COMPONENT_LIB} PUBLIC iotcore)
