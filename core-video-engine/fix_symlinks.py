import os
from pathlib import Path
import shutil

hub = Path("/Users/thientm/.cache/huggingface/hub")
for link in hub.rglob("*"):
    if link.is_symlink():
        target = os.readlink(link)
        if not os.path.isabs(target):
            target = link.parent / target
        target = target.resolve()
        link.unlink()
        shutil.copy2(target, link)
print("Symlinks fixed!")
