from pathlib import Path
import shutil

from categories import FILE_CATEGORIES


def validate_directory(directory):
    """Valida o caminho informado e devolve um objeto Path."""
    directory_path = Path(directory).expanduser()

    if not directory_path.exists():
        raise FileNotFoundError("A pasta informada não existe.")

    if not directory_path.is_dir():
        raise NotADirectoryError("O caminho informado não é uma pasta.")

    return directory_path


def find_files(directory_path):
    """Encontra somente os arquivos presentes na raiz da pasta."""
    return [item for item in directory_path.iterdir() if item.is_file()]


def classify_file(file_path):
    """Retorna a categoria correspondente à extensão do arquivo."""
    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Outros"


def create_safe_destination(file_path, destination_folder):
    """Cria um novo nome quando já existe um arquivo no destino."""
    destination = destination_folder / file_path.name

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = f"{file_path.stem}_{counter}{file_path.suffix}"
        destination = destination_folder / new_name

        if not destination.exists():
            return destination

        counter += 1


def organize_directory(directory):
    """Organiza os arquivos da pasta e retorna um resumo da execução."""
    directory_path = validate_directory(directory)
    files = find_files(directory_path)
    summary = {
        "analisados": len(files),
        "movidos": 0,
        "erros": 0,
        "categorias": {},
    }

    for file_path in files:
        category = classify_file(file_path)
        destination_folder = directory_path / category

        try:
            destination_folder.mkdir(exist_ok=True)
            destination = create_safe_destination(file_path, destination_folder)
            shutil.move(str(file_path), str(destination))

            summary["movidos"] += 1
            summary["categorias"][category] = (
                summary["categorias"].get(category, 0) + 1
            )
            print(f"[MOVIDO] {file_path.name} -> {category}/{destination.name}")

        except (PermissionError, OSError) as error:
            summary["erros"] += 1
            print(f"[ERRO] Não foi possível mover {file_path.name}: {error}")

    return summary
