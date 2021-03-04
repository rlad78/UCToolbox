from pathlib import Path


def rm_dir(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_dir(child)
    pth.rmdir()
    

def get_output_folder() -> Path:
    output_folder = Path().cwd() / "OUTPUT"
    # make it empty
    if output_folder.is_dir():
        rm_dir(str(output_folder))
        output_folder.mkdir(parents=True, exist_ok=True)
    return output_folder
