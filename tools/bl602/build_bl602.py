#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

def validate_args():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <BSP_NAME> <PROJECT_TITLE> <COMMAND> [MONITOR_PORT]")
        print("Available commands: build, clean, erase_flash, flash, monitor")
        sys.exit(1)

    bsp_name = sys.argv[1]
    project_title = sys.argv[2]
    command = sys.argv[3]
    monitor_port = sys.argv[4] if len(sys.argv) > 4 else None

    return bsp_name, project_title, command, monitor_port

def setup_paths(bsp_name, project_title):
    stdk_path = Path(os.getcwd()).absolute()
    core_path = stdk_path / "iot-core"
    iot_apps_path = stdk_path / "apps" / bsp_name
    project_path = iot_apps_path / project_title
    build_output_path = project_path / "build_out"
    bsp_path = stdk_path / "bsp" / bsp_name
    flash_tool = bsp_path / "tools/flash_tool/bflb_iot_tool-ubuntu"
    partition_table = bsp_path / "tools/flash_tool/chips/bl602/partition/partition_cfg_2M.toml"
    app_firmware = build_output_path / f"{project_title}.bin"

    os.environ.update({
        "CHIP_NAME": "BL602",
        "BSP_NAME": bsp_name,
        "PROJECT_TITLE": project_title,
        "STDK_PATH": str(stdk_path),
        "CORE_PATH": str(core_path)
    })

    return {
        "project_path": project_path,
        "build_output_path": build_output_path,
        "flash_tool": flash_tool,
        "partition_table": partition_table,
        "app_firmware": app_firmware,
        "baudrate": "2000000",
        "uart_port": "/dev/ttyACM0"
    }

def run_make():
    make_cmd = [
        "make",
        "CONFIG_CHIP_NAME=BL602",
        "CONFIG_LINK_ROM=1",
        "CONFIG_BLE_TP_SERVER=1",
        "CONFIG_BLECONTROLLER_LIB=all",
        "-j",
        "PTS_GAP_SLAVER_CONFIG_INDICATE_CHARC=1",
        "CONFIG_BT_STACK_PTS=1"
    ]
    subprocess.run(make_cmd, check=True)

def handle_command(command, paths, monitor_port=None):
    os.chdir(paths["project_path"])

    if command == "build":
        run_make()
    elif command == "clean":
        if paths["build_output_path"].exists():
            subprocess.run(["rm", "-rf", str(paths["build_output_path"])], check=True)
    elif command == "erase_flash":
        subprocess.run([
            str(paths["flash_tool"]),
            "--chipname=BL602",
            f"--baudrate={paths['baudrate']}",
            f"--port={paths['uart_port']}",
            f"--pt={paths['partition_table']}",
            "--dts=",
            f"--firmware={paths['app_firmware']}",
            "--erase"
        ], check=True)
    elif command == "flash":
        if not paths["build_output_path"].exists():
            run_make()
        subprocess.run([
            str(paths["flash_tool"]),
            "--chipname=BL602",
            f"--baudrate={paths['baudrate']}",
            f"--port={paths['uart_port']}",
            f"--pt={paths['partition_table']}",
            "--dts=",
            f"--firmware={paths['app_firmware']}"
        ], check=True)
    elif command == "monitor":
        if not monitor_port:
            print("Monitor command requires port argument")
            sys.exit(1)
        monitor_script = Path(os.environ["STDK_PATH"]) / "tools" / os.environ["BSP_NAME"] / "monitor.py"
        subprocess.run([
            "/usr/bin/python3",
            str(monitor_script),
            monitor_port
        ], check=True)
    else:
        print(f"Invalid command: {command}")
        sys.exit(1)

def main():
    try:
        bsp_name, project_title, command, monitor_port = validate_args()
        paths = setup_paths(bsp_name, project_title)
        handle_command(command, paths, monitor_port)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error {e.returncode}: {e.cmd}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
