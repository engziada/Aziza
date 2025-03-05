import os
import shutil

def copy_directory(src, dst):
    """
    Copy a directory from src to dst.
    
    Args:
        src (str): Source directory
        dst (str): Destination directory
    """
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        
        if os.path.isdir(s):
            copy_directory(s, d)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime > os.stat(d).st_mtime:
                shutil.copy2(s, d)

def main():
    """Copy templates and static files to the new structure."""
    # Copy templates
    copy_directory('templates', 'app/templates')
    
    # Copy static files
    copy_directory('static', 'app/static')
    
    print("Templates and static files copied successfully!")

if __name__ == '__main__':
    main()
