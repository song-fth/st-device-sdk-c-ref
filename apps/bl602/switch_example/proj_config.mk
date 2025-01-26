#
#compiler flag config domain
#
#CONFIG_TOOLPREFIX :=
#CONFIG_OPTIMIZATION_LEVEL_RELEASE := 1
#CONFIG_M4_SOFTFP := 1

#
#board config domain
#
CONFIG_BOARD_FLASH_SIZE := 2

#firmware config domain
#

#set CONFIG_ENABLE_ACP to 1 to enable ACP, set to 0 or comment this line to disable
#CONFIG_ENABLE_ACP:=1
CONFIG_BL_IOT_FW_AP:=1
CONFIG_BL_IOT_FW_AMPDU:=0
CONFIG_BL_IOT_FW_AMSDU:=0
CONFIG_BL_IOT_FW_P2P:=0
CONFIG_ENABLE_PSM_RAM:=1
#CONFIG_ENABLE_CAMERA:=1
#CONFIG_ENABLE_BLSYNC:=1
#CONFIG_ENABLE_VFS_SPI:=1
CONFIG_ENABLE_VFS_ROMFS:=1
CONFIG_ADC_ENABLE_TSEN:=1
CONFIG_EASYFLASH_ENABLE:=1

CONFIG_COMPONENT_BUGKILLER_ENABLE:=1

CONFIG_FREERTOS_TICKLESS_MODE:=1

CONFIG_SYS_APP_TASK_STACK_SIZE:=4096
CONFIG_SYS_APP_TASK_PRIORITY:=15
CONFIG_SYS_VFS_ENABLE:=1
CONFIG_SYS_VFS_UART_ENABLE:=1
CONFIG_SYS_AOS_CLI_ENABLE:=1
CONFIG_SYS_AOS_LOOP_ENABLE:=1
CONFIG_SYS_BLOG_ENABLE:=1
CONFIG_SYS_DMA_ENABLE:=1
CONFIG_SYS_USER_VFS_ROMFS_ENABLE:=1

CONFIG_BT:=1
CONFIG_USE_XTAL32K:=0
CONFIG_ENABLE_STACK_OVERFLOW_CHECK:=0

#mbedtls
CONFIG_MBEDTLS_AES_USE_HW:=1
CONFIG_MBEDTLS_BIGNUM_USE_HW:=1
CONFIG_MBEDTLS_ECC_USE_HW:=1

#wifi diagnosis
CONFIG_TD_DIAGNOSIS_STA:=1

#blog enable components format :=blog_testc cli vfs helper
LOG_ENABLED_COMPONENTS:=blog_testc hosal loopset looprt bloop blestack
ifeq ($(CONFIG_BT_MESH_SYNC),1)
LOG_ENABLED_COMPONENTS += blsync_ble
endif
CONFIG_BL602_USE_ROM_DRIVER:=1
CONFIG_BL602_USE_1M_FLASH:=0

CONFIG_BT_STACK_PTS:=0

CONF_ENABLE_COREDUMP:=1

# STDK config

CONFIG_STDK_IOT_CORE:=y
CONFIG_STDK_IOT_CORE_BSP_SUPPORT_BL602:=y
CONFIG_STDK_IOT_CORE_OS_SUPPORT_FREERTOS:=y
CONFIG_STDK_IOT_CORE_USE_MBEDTLS:=y
CONFIG_STDK_IOT_CORE_NET_MBEDTLS:=y
CONFIG_STDK_IOT_CORE_EASYSETUP_HTTP=y
CONFIG_LWIP_USE_HTTPD_FOR_EASYSETUP=y
CONFIG_STDK_IOT_CORE_SECURITY_BACKEND_SOFTWARE:=y
