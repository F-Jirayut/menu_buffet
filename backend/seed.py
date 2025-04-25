import importlib
import argparse

SEEDS = [
    'app.seeds.role_seed',
    'app.seeds.user_seed',
    'app.seeds.permission_seed',
    'app.seeds.role_permission_root_seed',
    'app.seeds.menu_category_seed',
    ]

def run_seed(seed):
    """รัน seed ทีละตัว"""
    try:
        print(f"Running seed: {seed}...")
        module = importlib.import_module(seed)
        module.run()  # เรียกใช้ฟังก์ชัน run ในแต่ละ module seed
        print(f"{seed} completed.\n")
    except Exception as e:
        print(f"Failed to run {seed}: {e}")

def run_all_seeds():
    """รันทุก seed"""
    for seed in SEEDS:
        run_seed(seed)

def main():
    parser = argparse.ArgumentParser(description="Seed Database")
    parser.add_argument(
        "--seed",
        type=str,
        help="ระบุชื่อ seed ที่ต้องการรัน (เช่น user_seed, role_seed)",
    )
    args = parser.parse_args()

    if args.seed:
        # หากระบุชื่อ seed ให้รัน seed ที่ระบุ
        seed = f"app.seeds.{args.seed}"
        if seed in SEEDS:
            run_seed(seed)
        else:
            print(f"Seed {args.seed} not found in available seeds.")
    else:
        # หากไม่ระบุ seed ให้รันทั้งหมด
        run_all_seeds()

if __name__ == "__main__":
    main()
