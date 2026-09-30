from pathlib import Path


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".tif",
    ".tiff"
}

def find_images(image_directory: str) -> list[Path]:
    """
    Find all supported image files recursively.

    Parameters
    ----------
    image_directory : str
        Root directory containing plant images.

    Returns
    -------
    list[Path]
        Sorted list of image paths.

    """
    root = Path(image_directory)
    if not root.exists():
        raise FileNotFoundError(
            f"image directory does not exist: {root}"
        )
    
    images = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return sorted(images)