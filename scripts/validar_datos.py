"""Valida la presencia y legibilidad de los insumos de Demografía de Empresas."""

from app.data.catalog import CUADROS_DIR, REQUIRED_FILES, ROOT_DIR, XLSX_FILES
from app.data.excel_loader import profile_excel


def main() -> int:
    """Comprueba archivos requeridos e inspecciona la primera hoja de cada Excel."""
    missing = [path for path in REQUIRED_FILES if not path.exists()]
    if missing:
        print("Faltan archivos de datos:")
        for path in missing:
            print(f"- {path.relative_to(ROOT_DIR)}")
        return 1

    errors: list[str] = []
    print(f"Archivos requeridos presentes: {len(REQUIRED_FILES)}")
    print("\nEstructura de cuadros estadísticos:")

    for name in XLSX_FILES:
        path = CUADROS_DIR / name
        try:
            profile = profile_excel(path)
            columns = ", ".join(profile.columns)
            print(f"- {profile.file} | hoja={profile.sheet!r} | filas={profile.rows} | columnas=[{columns}]")
        except Exception as exc:  # Se informa cada libro defectuoso sin ocultar los demás.
            errors.append(f"{name}: {exc}")

    if errors:
        print("\nErrores de lectura:")
        for error in errors:
            print(f"- {error}")
        return 2

    print(f"\nValidación Python correcta: {len(XLSX_FILES)} Excel legibles y {len(REQUIRED_FILES)} archivos presentes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
