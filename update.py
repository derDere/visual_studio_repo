"""Copies all CodeSnippets to all Visual Studio folders.
"""

import os
import shutil
import subprocess

def get_documents_path():
  """Returns the path to the Documents folder. using "powershell [Environment]::GetFolderPath('MyDocuments')"
  """
  cmd = ["powershell", "[Environment]::GetFolderPath('MyDocuments')"]
  process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True
  )
  stdout, stderr = process.communicate()
  if process.returncode != 0:
    raise subprocess.CalledProcessError(process.returncode, " ".join(cmd), stdout, stderr)
  return stdout.strip()


def get_all_visual_studio_folders():
  """Returns a list of all Visual Studio folders.
  """
  documents_path = get_documents_path()
  visual_studio_folders = []
  for folder in os.listdir(documents_path):
    if folder.startswith("Visual Studio"):
      visual_studio_folders.append(os.path.join(documents_path, folder))
  return visual_studio_folders


def copy_and_replace_files_recursively(source, destination):
  """Copies all files from source to destination, replacing any existing files.
  """
  file_filter = [
    ".snippet"
  ]
  for folder in os.listdir(source):
    if os.path.isdir(os.path.join(source, folder)):
      copy_and_replace_files_recursively(
        os.path.join(source, folder),
        os.path.join(destination, folder)
      )
  for file in os.listdir(source):
    if os.path.isfile(os.path.join(source, file)):
      if any(file.endswith(extension) for extension in file_filter):
        print(f"    - {file}")
        shutil.copyfile(
          os.path.join(source, file),
          os.path.join(destination, file)
        )


def main():
  """Main function.
  """
  source = os.getcwd()
  print(f"Source Directory: {source}")
  visual_studio_folders = get_all_visual_studio_folders()
  for folder in visual_studio_folders:
    print(f"Copying files to: {folder}")
    copy_and_replace_files_recursively(source, folder)


if __name__ == "__main__":
  main()
