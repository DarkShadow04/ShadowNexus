from core.config import load_config, save_config

def workspace_manager():
    cfg = load_config()
    print(f"Current Workspace: {cfg['workspace']}")
    new = input("New workspace name (blank cancel): ").strip()
    if new:
        cfg["workspace"] = new
        save_config(cfg)
    input("Press Enter...")
