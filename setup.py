from cx_Freeze import setup, Executable

# Pacotes necessários para o executável
buildOptions = {
    "packages": ["tkinter", "PIL", "requests"],  # Incluir "tkinter", "PIL" (Pillow) e "requests"
    "includes": ["urllib.parse", "io"],           # Incluir "urllib.parse" e "io"
    "include_files": ["Images/"]                  # Incluir a pasta de imagens
}

# Configuração do setup
setup(
    name="Book Recomendation",
    version="1.0",
    description="Recomendaçao de livros usando API do Google!",
    options={"build_exe": buildOptions},
    executables=[Executable("main.py", base="Win32GUI")]  # Nome do seu arquivo .py
)
