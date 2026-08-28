import os
import uuid

from PIL import Image
from werkzeug.utils import secure_filename


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.abspath(
    os.path.join(BASE_DIR, '..', 'uploads')
)

ALLOWED_EXTENSIONS = {
    'png',
    'jpg',
    'jpeg',
    'gif',
    'webp'
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


def allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def save_image(file_storage, subfolder=''):
    """
    Valida e salva uma imagem enviada através de request.files.

    Retorna o caminho relativo da imagem salva.
    """

    if not file_storage or not file_storage.filename:
        return None

    filename = secure_filename(file_storage.filename)

    if not filename:
        raise ValueError("Nome de arquivo inválido")

    if not allowed_file(filename):
        raise ValueError("Tipo de arquivo não permitido")

    # Verifica o tamanho do arquivo
    file_storage.seek(0, os.SEEK_END)
    file_size = file_storage.tell()
    file_storage.seek(0)

    if file_size > MAX_IMAGE_SIZE:
        raise ValueError(
            "A imagem deve ter no máximo 5 MB"
        )

    # Verifica o conteúdo real da imagem
    try:
        image = Image.open(file_storage)
        image.verify()

    except Exception:
        raise ValueError(
            "O arquivo enviado não é uma imagem válida"
        )

    # Volta o ponteiro para o início antes de salvar
    file_storage.seek(0)

    # Gera nome aleatório
    extension = filename.rsplit('.', 1)[1].lower()
    new_filename = f"{uuid.uuid4().hex}.{extension}"

    folder_path = os.path.join(
        UPLOAD_FOLDER,
        subfolder
    )

    os.makedirs(
        folder_path,
        exist_ok=True
    )

    file_path = os.path.join(
        folder_path,
        new_filename
    )

    file_storage.save(file_path)

    return (
        f"{subfolder}/{new_filename}"
        if subfolder
        else new_filename
    )
