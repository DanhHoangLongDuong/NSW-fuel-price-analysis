import load
import clean

if __name__ == "__main__":
    table = load.load_raw(load.folder_path)
    table.to_parquet(path=load.output_path, index=False)
    table = clean.clean(table)
    table.to_parquet(path=clean.output_path, index=False)