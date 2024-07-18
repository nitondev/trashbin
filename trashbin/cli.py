import argparse
import datetime
import hashlib
import os
import shutil
import time

from rich.console import Console
from rich.table import Table

# Constants for paths
TRASHBIN = os.path.expanduser("~/.local/share/trashbin")
METADATA = os.path.expanduser("~/.cache/trashbin/metadata")
DELAY_BETWEEN_MOVES = 0.125  # 125ms delay between moves
VERSION = "0.1.0"

# Ensure directories exist
os.makedirs(TRASHBIN, exist_ok=True)
os.makedirs(os.path.dirname(METADATA), exist_ok=True)

# Initialize Rich for console output
console = Console()


def move_to_trash(file_paths):
    moved_count = 0  # Counter for successfully moved items
    with open(METADATA, "a", encoding="utf-8") as metadata_file:
        for path in file_paths:
            original_path = os.path.abspath(path)  # Get absolute path

            if os.path.exists(original_path):
                # Generate a unique filename based on file contents and timestamp
                unique_filename = generate_unique_filename(original_path)
                dest_path = os.path.join(TRASHBIN, unique_filename)

                # Move file to trash
                shutil.move(original_path, dest_path)

                # Record metadata with formatted datetime
                metadata_entry = (
                    f"{unique_filename}|{get_formatted_datetime()}|{original_path}\n"
                )
                metadata_file.write(metadata_entry)

                moved_count += 1  # Increment counter for each moved item

                # Delay between moves
                time.sleep(DELAY_BETWEEN_MOVES)
            else:
                # Print error message for non-existing paths
                console.print(f"[bold #d62121]trash:[/] '{path}' does not exist.")
                return

        console.print(
            f"[green]trash:[/] moved [green]{moved_count} item[/](s) to trash bin."
        )


def generate_unique_filename(path):
    # Calculate file hash
    file_hash = hashlib.sha256()

    if os.path.isfile(path):
        with open(path, "rb") as f:
            # Read file in chunks to handle large files
            while chunk := f.read(4096):
                file_hash.update(chunk)

    file_hash_hex = file_hash.hexdigest()

    # Calculate datetime hash
    datetime_hash = hashlib.sha256(get_formatted_datetime().encode()).hexdigest()

    # Combine hashes to generate unique filename
    unique_filename = hashlib.sha256(
        (file_hash_hex + datetime_hash).encode()
    ).hexdigest()

    # Determine if path is a file or directory
    if os.path.isfile(path):
        # If file, append file extension to unique filename
        filename, extension = os.path.splitext(os.path.basename(path))
        unique_filename += extension

    return unique_filename


def get_formatted_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")


def format_datetime(datetime_str):
    # Convert datetime string with milliseconds to datetime object
    dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S:%f")
    # Format datetime without milliseconds
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def list_trash():
    if not os.path.exists(METADATA) or os.path.getsize(METADATA) == 0:
        console.print("[green]trash:[/] Trash bin is empty. :sparkles:")
        return []

    print(f"trash: v{VERSION} \n")
    table = Table(show_header=True, box=False, header_style="cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Date", style="dim", width=19)
    table.add_column("File path", justify="left")

    trash_entries = []

    with open(METADATA, "r", encoding="utf-8") as metadata_file:
        for index, line in enumerate(metadata_file):
            parts = line.strip().split("|")
            if len(parts) == 3:
                unique_filename, deleted_time, original_path = parts
                # Format datetime string
                formatted_datetime = format_datetime(deleted_time)
                table.add_row(str(index + 1), formatted_datetime, original_path)
                trash_entries.append((unique_filename, original_path))

    console.print(table)
    return trash_entries


def restore_from_trash():
    if not os.path.exists(METADATA) or os.path.getsize(METADATA) == 0:
        console.print("[green]trash:[/] Trash bin is empty. :sparkles:")
        return

    trash_entries = list_trash()
    if not trash_entries:
        return

    try:
        index = int(
            input(f"\nSelect file in list [1..{len(trash_entries)}] to restore: ")
        )
        if 1 <= index <= len(trash_entries):
            unique_filename, original_path = trash_entries[index - 1]
            trash_path = os.path.join(TRASHBIN, unique_filename)

            if os.path.exists(trash_path):
                shutil.move(trash_path, original_path)
                remove_metadata_entry(unique_filename)
                filename = os.path.basename(original_path)
                console.print(f"[green]trash:[/] '{filename}' has been restored.")
            else:
                console.print(
                    f"[bold #d62121]trash:[/] '{trash_path}' does not exist in trash bin."
                )
        else:
            console.print("[bold #d62121]trash:[/] Invalid selection.")
    except ValueError:
        console.print("[bold #d62121]trash:[/] Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        console.print("\n[bold #d62121]trash:[/] Aborted by user.")


def remove_metadata_entry(unique_filename):
    if not os.path.exists(METADATA) or os.path.getsize(METADATA) == 0:
        return

    temp_metadata_path = METADATA + ".tmp"
    with open(METADATA, "r", encoding="utf-8") as metadata_file, open(
        temp_metadata_path, "w", encoding="utf-8"
    ) as temp_metadata_file:
        for line in metadata_file:
            if not line.startswith(unique_filename + "|"):
                temp_metadata_file.write(line)

    os.replace(temp_metadata_path, METADATA)


def empty_trash():
    if not os.path.exists(METADATA) or os.path.getsize(METADATA) == 0:
        console.print("[green]trash:[/] Trash bin is empty. :sparkles:")
        return

    try:
        console.print("[bold #FF5F15]trash:[/] This action is not reversible.")
        confirmation = input("Type 'yes' to confirm: ")
        if confirmation.lower() == 'yes':
            with open(METADATA, "r", encoding="utf-8") as metadata_file:
                trash_entries = [line.split("|")[0] for line in metadata_file]

            num_items = len(trash_entries)
            for unique_filename in trash_entries:
                trash_path = os.path.join(TRASHBIN, unique_filename)
                if os.path.exists(trash_path):
                    if os.path.isfile(trash_path):
                        os.remove(trash_path)
                    else:
                        shutil.rmtree(trash_path)

            # Clear metadata file
            open(METADATA, "w").close()

            console.print(f"[green]trash: {num_items} item[/](s) shredded.")
        else:
            console.print("[bold #d62121]trash:[/] Aborted by user.")
    except KeyboardInterrupt:
        print("\n[bold #d62121]trash:[/] Aborted by user.")


def main():
    parser = argparse.ArgumentParser(description="Manage trash bin")
    parser.add_argument(
        "--list", action="store_true", help="List contents of trash bin"
    )
    parser.add_argument(
        "--restore", action="store_true", help="Restore a file from trash bin"
    )
    parser.add_argument("--empty", action="store_true", help="Empty the trash bin")
    parser.add_argument(
        "paths", nargs="*", help="Paths to files or directories to move to trash"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Trashbin (trash) Version: {VERSION}",
    )

    args = parser.parse_args()

    if args.list:
        list_trash()
    elif args.restore:
        restore_from_trash()
    elif args.empty:
        empty_trash()
    elif args.paths:
        move_to_trash(args.paths)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
