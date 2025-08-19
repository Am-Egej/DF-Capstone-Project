import kagglehub
import os
import pandas as pd

def fetch_and_save_dataset(datasets = ["dissfya/wta-tennis-2007-2023-daily-update", "dissfya/atp-tennis-2000-2023daily-pull" ], output_dir=r"data/raw"):
    count = 0
    for dataset_id in datasets:
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
                    df = pd.read_csv(file_path, low_memory=False)
                    output_path = os.path.join(output_dir, file)
                    df.to_csv(output_path, index=False)
                    print(f"📄 Saved: {output_path}")
                    count += 1
                else:
                    print(f"⚠️ Skipped non-CSV file: {file}")
            print(f"{count} csv file(s) saved")
        
        except Exception as e:
            print("❌ Error during dataset fetch:", str(e))
    
    return count


if __name__ == "__main__":
    datasets = ["dissfya/wta-tennis-2007-2023-daily-update", "dissfya/atp-tennis-2000-2023daily-pull" ]
    fetch_and_save_dataset(datasets)
