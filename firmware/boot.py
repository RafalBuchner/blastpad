import storage

# renaming storage to BlastPad
storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = "BlastPad"
storage.remount("/", readonly=True)
