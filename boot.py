# boot.py - Executed first on hardware power-up
import uos # type: ignore
import vfs # type: ignore
import gc
from nvvfs import NVVFS_BlockDevice 

print("[BOOT]: Mounting custom secure file layout allocation matrix...")

try:
    # 1. Initialize the custom memory sector blocks
    bdev = NVVFS_BlockDevice(block_size=512, num_blocks=128)
    
    # 2. Make directory hook if it's missing
    try:
        uos.mkdir("/matrix_secure")
    except OSError:
        pass
        
    # 3. Mount securely so main.py can access files instantly
    vfs.mount(vfs.VfsFat(bdev), "/matrix_secure")
    print("[BOOT]: Virtual allocation mount successful.")
except Exception as mount_error:
    print("[BOOT WARNING]: Mounting failed. Partition schema corrupt:", mount_error)

# Run internal trash collection to maximize RAM for my 570+ lines of code
gc.collect()