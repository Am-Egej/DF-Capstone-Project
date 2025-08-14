import kagglehub
import os
import pandas as pd

def fetch_and_save_dataset(dataset_id="dissfya/atp-tennis-2000-2023daily-pull", output_dir=r"data/raw"):
    try:
        print(f"📦 Downloading dataset: {dataset_id}")
        path = kagglehub.dataset_download(dataset_id)

        print("✅ Download complete.")
        print("📁 Path to dataset files:", path)

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Loop through files and save as CSV if needed
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if file.endswith(".csv"):
                df = pd.read_csv(file_path)
                output_path = os.path.join(output_dir, file)
                df.to_csv(output_path, index=False)
                print(f"📄 Saved: {output_path}")
            else:
                print(f"⚠️ Skipped non-CSV file: {file}")

    except Exception as e:
        print("❌ Error during dataset fetch:", str(e))

if __name__ == "__main__":
    fetch_and_save_dataset()
