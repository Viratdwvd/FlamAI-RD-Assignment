import matplotlib.pyplot as plt

from src.data_loader import load_data


DATA_PATH = "data/xy_data.csv"
OUTPUT_PATH = "results/raw_data.png"


def main():
    df = load_data(DATA_PATH)

    print("Dataset shape:", df.shape)
    print("\nSummary statistics:")
    print(df.describe())

    print("\nData ranges:")
    print(f"x: {df['x'].min():.4f} -> {df['x'].max():.4f}")
    print(f"y: {df['y'].min():.4f} -> {df['y'].max():.4f}")

    plt.figure(figsize=(9, 6))
    plt.scatter(df["x"], df["y"], s=8)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Observed XY Data")
    plt.grid(True, alpha=0.25)
    plt.tight_layout()

    plt.savefig(OUTPUT_PATH, dpi=180)
    plt.show()


if __name__ == "__main__":
    main()