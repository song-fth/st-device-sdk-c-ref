import os
import subprocess
import sys

def install_dependencies():
    print("Starting to install necessary tools...")
    try:
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'make', 'gtkterm'], check=True)
        print("Installation completed.")
    except subprocess.CalledProcessError:
        print("Installation failed. Please ensure there are no errors during the installation process.")
        sys.exit(1)

def is_git_submodule(bsp_name):
    try:
        subprocess.run(['git', 'submodule', 'status', f'bsp/{bsp_name}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def apply_patch(target_dir, patch_dir, is_git):
    print(f"apply-patch : {target_dir}")
    os.chdir(target_dir)
    
    for patch in os.listdir(patch_dir):
        if patch.endswith('.patch'):
            patch_path = os.path.join(patch_dir, patch)
            if is_git:
                subprocess.run(['git', 'am', patch_path])
            else:
                subprocess.run(['patch', '-f', '-p1', '<', patch_path], shell=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <BSP_NAME>")
        sys.exit(1)

    bsp_name = sys.argv[1]
    stdk_ref_path = os.getenv("STDK_REF_PATH")  # Assuming STDK_REF_PATH is set in the environment
    bsp_path = os.path.join(stdk_ref_path, 'bsp', bsp_name)
    patch_path = os.path.join(stdk_ref_path, 'patches', bsp_name)

    install_dependencies()

    is_git = is_git_submodule(bsp_name)

    os.chdir(bsp_path)
    subprocess.run(['git', 'submodule', 'update', '--init', '--recursive'])
    subprocess.run(['git', 'submodule', 'foreach', '--recursive', 'git', 'reset', '--hard'])

    apply_patch(bsp_path, patch_path, is_git)