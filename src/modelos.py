from datetime import datetime


class Solicitud:

    def __init__(
        self,
        codigo: str,
        solicitante: str,
        descripcion: str,
        hora_llegada: str | None = None
    ) -> None:

        self.codigo: str = codigo
        self.solicitante: str = solicitante
        self.descripcion: str = descripcion

        if hora_llegada is None:
            self.hora_llegada: str = datetime.now().strftime("%H:%M:%S")
        else:
            self.hora_llegada = hora_llegada


    def __str__(self) -> str:
        return (
            f"Código: {self.codigo} | "
            f"Solicitante: {self.solicitante} | "
            f"Descripción: {self.descripcion} | "
            f"Hora: {self.hora_llegada}"
        )
