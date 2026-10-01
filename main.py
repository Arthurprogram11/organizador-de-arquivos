from organizer import find_files, organize_directory, validate_directory


def show_summary(summary):
    print("\nOrganização concluída.")
    print(f"Arquivos analisados: {summary['analisados']}")
    print(f"Arquivos movidos: {summary['movidos']}")
    print(f"Erros: {summary['erros']}")

    if summary["categorias"]:
        print("\nArquivos por categoria:")

        for category, quantity in summary["categorias"].items():
            print(f"- {category}: {quantity}")


def main():
    print("=== Organizador Automático de Arquivos ===")
    directory = input("Informe a pasta que deseja organizar: ").strip().strip('"')

    if not directory:
        print("Nenhuma pasta foi informada.")
        return

    try:
        directory_path = validate_directory(directory)
        files = find_files(directory_path)

        if not files:
            print("Nenhum arquivo foi encontrado na pasta.")
            return

        print(f"\nForam encontrados {len(files)} arquivo(s):")

        for file_path in files:
            print(f"- {file_path.name}")

        confirmation = input("\nDeseja organizar esses arquivos? [s/N]: ").strip().lower()

        if confirmation not in {"s", "sim"}:
            print("Operação cancelada. Nenhum arquivo foi alterado.")
            return

        summary = organize_directory(directory_path)
        show_summary(summary)

    except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
        print(f"Erro: {error}")
    except OSError as error:
        print(f"Erro inesperado ao acessar a pasta: {error}")


if __name__ == "__main__":
    main()
