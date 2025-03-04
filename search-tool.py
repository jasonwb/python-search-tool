import os
import argparse
import fnmatch

def search_files_or_dirs(root_dir, pattern, search_type, case_insensitive, quiet, verbose):
    results = []
    try:
        for root, dirs, files in os.walk(root_dir):
            if search_type == 'd':
                items = dirs
            elif search_type == 'f':
                items = files
            else:
                return []

            for item in items:
                if case_insensitive:
                    if fnmatch.fnmatch(item.lower(), pattern.lower()):
                        full_path = os.path.join(root, item)
                        if verbose:
                            results.append(get_verbose_info(full_path))
                        else:
                            results.append(full_path)
                else:
                    if fnmatch.fnmatch(item, pattern):
                        full_path = os.path.join(root, item)
                        if verbose:
                            results.append(get_verbose_info(full_path))
                        else:
                            results.append(full_path)

    except OSError as e:
        if not quiet:
            print(f"Error accessing {root_dir}: {e}")
    return results

def get_verbose_info(file_path):
    try:
        stat_info = os.stat(file_path)
        file_size = stat_info.st_size
        modified_time = stat_info.st_mtime
        return f"{file_path} (Size: {file_size} bytes, Modified: {modified_time})"
    except OSError:
        return file_path

def search_string_in_file(file_path, search_string, case_insensitive, quiet):
    try:
        with open(file_path, 'r', errors='ignore') as file:
            for line_number, line in enumerate(file, start=1):
                if case_insensitive:
                    if search_string.lower() in line.lower():
                        return f"{file_path}:{line_number}: {line.strip()}"
                else:
                    if search_string in line:
                        return f"{file_path}:{line_number}: {line.strip()}"
    except FileNotFoundError:
        if not quiet:
            print(f"File not found: {file_path}")
    except OSError as e:
        if not quiet:
            print(f"Error reading {file_path}: {e}")
    return None

def main():
    parser = argparse.ArgumentParser(description="Search files or directories.")
    parser.add_argument("pattern", help="Search pattern (e.g., *.txt, my_dir*)")
    parser.add_argument("-d", action="store_true", help="Search directories")
    parser.add_argument("-f", action="store_true", help="Search files")
    parser.add_argument("-i", action="store_true", help="Case-insensitive search")
    parser.add_argument("-q", action="store_true", help="Quiet mode, surpresses errors")
    parser.add_argument("-r", "--root", default=".", help="Root directory to start search (default: current directory)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output (file size, modification time)")
    parser.add_argument("-s", "--search", help="Search for a string inside files")

    args = parser.parse_args()

    if not args.d and not args.f and not args.search:
        print("Please specify either -d (directory), -f (file), or -s (search string).")
        return

    if args.search and not args.f:
        print("String search (-s) requires file search (-f).")
        return

    search_type = 'd' if args.d else 'f'

    results = search_files_or_dirs(args.root, args.pattern, search_type, args.i, args.q, args.verbose)

    if args.search:
        for result in results:
            string_result = search_string_in_file(result, args.search, args.i, args.q)
            if string_result:
                print(string_result)
    else:
        for result in results:
            print(result)

if __name__ == "__main__":
    main()
