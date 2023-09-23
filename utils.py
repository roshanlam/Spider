import os
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def create_project_dir(directory: str) -> None:
    """
    Create a directory if it doesn't exist.
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f'Directory {directory} created successfully.')
    except Exception as e:
        logging.error(f"Error creating directory {directory}. Error: {e}")


def create_data_files(project_name: str, base_url: str) -> None:
    """
    Create data files for the project inside the Data directory.
    """
    try:
        project_dir = os.path.join('Data', project_name)
        create_project_dir(project_dir)

        queue_path = os.path.join(project_dir, 'queue.txt')
        crawled_path = os.path.join(project_dir, 'crawled.txt')

        if not os.path.isfile(queue_path):
            _write_to_file(queue_path, base_url)
        if not os.path.isfile(crawled_path):
            _write_to_file(crawled_path, '')
    except Exception as e:
        logging.error(f"Error creating data files for project {project_name}. Error: {e}")


def _write_to_file(path: str, data: str) -> None:
    """
    Write data to a file.
    """
    try:
        with open(path, 'w') as f:
            f.write(data)
    except Exception as e:
        logging.error(f"Error writing to file {path}. Error: {e}")


def append_to_file(path: str, data: str) -> None:
    """
    Append data to an existing file.
    """
    try:
        with open(path, 'a') as f:
            f.write(f"{data}\n")
    except Exception as e:
        logging.error(f"Error appending to file {path}. Error: {e}")


def delete_file_contents(path: str) -> None:
    """
    Delete the contents of a file.
    """
    try:
        with open(path, 'w') as f:
            pass
    except Exception as e:
        logging.error(f"Error deleting contents of file {path}. Error: {e}")


def file_to_set(file_path: str) -> set:
    """
    Convert the contents of a file to a set.
    """
    try:
        with open(file_path, 'r') as f:
            return {line.strip() for line in f}
    except FileNotFoundError:
        logging.warning(f"File {file_path} not found.")
        return set()
    except Exception as e:
        logging.error(f"Error reading file {file_path}. Error: {e}")
        return set()


def set_to_file(links: set, file_path: str) -> None:
    """
    Write the contents of a set to a file.
    """
    try:
        with open(file_path, "w") as f:
            for link in sorted(links):
                f.write(f"{link}\n")
    except Exception as e:
        logging.error(f"Error writing set to file {file_path}. Error: {e}")
