# This script converts .zip files downloaded from mangakatana.com into individual .cbz files.
# Each .zip typically contains 10 chapters of a manga, organized as separate folders.

import os
import zipfile

def main():
    # Path to the root folder containing the .zip files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_folder = script_dir

    # Iterate over .zip files in the root folder
    for filename in os.listdir(root_folder):
        if filename.endswith('.zip'):
            zip_path = os.path.join(root_folder, filename)

            # Extract the chapter name from the .zip filename
            chapter_name = os.path.splitext(filename)[0]
            series_name = '-'.join(chapter_name.split('_')[:-2])

            cbz_folder = os.path.join(root_folder, 'cbz')
            if not os.path.exists(cbz_folder):
                os.makedirs(cbz_folder)

            try:
                count = 0
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    for entry in zip_ref.namelist():
                        # Identify each subfolder except the top-level one
                        if entry.endswith('/') and entry != chapter_name + '/':
                            count += 1
                            subfolder_name = os.path.basename(entry[:-1])
                            cbz_path = os.path.join(cbz_folder, f'{series_name}_{subfolder_name}.cbz')

                            with zipfile.ZipFile(cbz_path, 'w', compression=zipfile.ZIP_DEFLATED) as cbz:
                                for file_in_zip in zip_ref.namelist():
                                    if file_in_zip.startswith(entry):
                                        file_data = zip_ref.read(file_in_zip)
                                        file_path_cbz = os.path.join(subfolder_name, os.path.basename(file_in_zip))
                                        cbz.writestr(file_path_cbz, file_data)

                print(f'Finished processing {filename}: {count} CBZ files created, {len(os.listdir(cbz_folder))} total in "{cbz_folder}"')

            except Exception as e:
                print(f'Error reading ZIP file: {zip_path}\n{e}')

    print('All done!')

if __name__ == '__main__':
    main()
