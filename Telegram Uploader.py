from telethon import TelegramClient
import os
import shutil
from tqdm import tqdm

# Replace these with your actual API_ID and API_HASH
api_id = 1234567  # Your actual API_ID as an integer
api_hash = 'your_actual_api_hash'  # Your actual API_HASH as a string

# Folder paths
input_folder = 'Input File'
done_folder = './Input File/Done'

# Create the Telegram client
client = TelegramClient('telegram_session', api_id, api_hash)

async def list_groups_or_channels(option):
    if option == '1':
        print("Listing Telegram Groups...")
        dialogs = await client.get_dialogs()
        groups = [d for d in dialogs if d.is_group]
        for i, group in enumerate(groups, 1):
            print(f"{i}: {group.title}")
        return groups
    elif option == '2':
        print("Listing Telegram Channels...")
        dialogs = await client.get_dialogs()
        channels = [d for d in dialogs if d.is_channel]
        for i, channel in enumerate(channels, 1):
            print(f"{i}: {channel.title}")
        return channels

async def upload_files_to_target(target):
    if not os.path.exists(done_folder):
        os.makedirs(done_folder)

    files = os.listdir(input_folder)
    total_files = len(files)

    for idx, file_name in enumerate(files):
        file_path = os.path.join(input_folder, file_name)
        if os.path.isfile(file_path):
            # Get file size in KB or MB
            file_size = os.path.getsize(file_path)
            if file_size < 1024 * 1024:  # Less than 1 MB
                size_display = f"{file_size / 1024:.2f} KB"
            else:
                size_display = f"{file_size / (1024 * 1024):.2f} MB"

            # Use fixed-width formatting for alignment
            file_number = f"{idx + 1}/{total_files}".ljust(10)  # Reserve 10 characters for numbering
            size_info = f"Size: {size_display}".ljust(15)       # Reserve 15 characters for size info

            # Add space before each progress bar
            print()  # This print statement adds a blank line

            # Display all information in one line using tqdm
            with tqdm(total=100, desc=f"File {file_number}", ncols=100, 
                      bar_format="{l_bar}{bar} {percentage:3.0f}% | " + size_info) as progress_bar:
                await client.send_file(
                    target, 
                    file_path, 
                    force_document=True, 
                    progress_callback=lambda current, total: progress_bar.update(100 * current // total - progress_bar.n)
                )
            
            shutil.move(file_path, os.path.join(done_folder, file_name))
        else:
            print(f"Skipped: {file_name} (not a file)")

async def main():
    # Start the client
    await client.start()

    print("Choose where to upload files:")
    print("1: Telegram Group")
    print("2: Telegram Channel")
    option = input("Enter your choice (1 or 2): ")

    if option not in ['1', '2']:
        print("Invalid option selected. Exiting...")
        return

    targets = await list_groups_or_channels(option)
    selected_index = int(input("Enter the number of the target you want to upload to: ")) - 1

    if selected_index < 0 or selected_index >= len(targets):
        print("Invalid target selected. Exiting...")
        return

    target = targets[selected_index].entity

    print(f"Selected: {targets[selected_index].title}")
    start_upload = input("Do you want to start the upload? (yes/no): ").strip().lower()

    if start_upload == 'yes':
        await upload_files_to_target(target)
        print("All files have been uploaded!")
    else:
        print("Upload canceled.")

    await client.disconnect()

with client:
    client.loop.run_until_complete(main())
