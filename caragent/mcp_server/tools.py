from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from .server import mcp
from ..settings import DB_CONNECTION_STRING
from ..database import Car, create_database


def _format_argument(arg: str, value: str | int | float | list[str|int]):
    if value is None:
        return
    if arg.endswith("_min"):
        return getattr(Car, arg[:-4]) >= value
    elif arg.endswith("_max"):
        return getattr(Car, arg[:-4]) <= value
    elif arg.endswith("_contains"):
        return getattr(Car, arg[:-9]).contains(value)
    else:
        db_field = getattr(Car, arg)
        return db_field.in_(value) if isinstance(value, list) else db_field == value

@mcp.tool()
def query_car_database(
    make: str | list[str] | None = None,
    model: str | list[str] | None = None,
    year_min: int | None = None,
    year_max: int | None = None,
    fuel: str | list[str] | None = None,
    doors: int | list[int] | None = None,
    milage_min: int | None = None,
    milage_max: int | None = None,
    transmission: str | list[str] | None = None,
    size_class_contains: str | list[str] | None = None,
    engine_displacement_min: float | None = None,
    engine_displacement_max: float | None = None,
    cylinders_min: int | None = None,
    cylinders_max: int | None = None,
    additional_info_contains: str | None = None,
) -> str:
    """Consulta o banco de dados de carros com filtros.

    Todos os argumentos são filtros que serão usados ao consultar o banco de dados. Apenas argumentos que não são None serão usados.
    Args:
        make (str | list[str] | None, optional): O(s) fabricante(s) do carro a ser usado como filtro. Padrão é None.
        model (str | list[str] | None, optional): O modelo do carro a ser usado como filtro. Padrão é None.
        year_min (int | None, optional): O ano mínimo. Padrão é None.
        year_max (int | None, optional): O ano máximo. Padrão é None.
        fuel (str | list[str] | None, optional): O tipo de combustível ("Gas", "Flex", "Diesel", "Etanol", "Electric" ou "Hybrid"). Padrão é None.
        doors (int | list[int] | None, optional): A quantidade de portas. Padrão é None.
        milage_min (int | None, optional): A quilometragem mínima. Padrão é None.
        milage_max (int | None, optional): A quilometragem máxima. Padrão é None.
        transmission (str | list[str] | None, optional): O tipo de transmissão ("Manual" ou "Automatic"). Padrão é None.
        size_class_contains (str | None, optional): A classe de tamanho (Convertible, Van/Minivan, Coupe, SUV, Pickup, Sedan, Wagon ou Hatchback). Padrão é None.
        engine_displacement_min (float | None, optional): A cilindrada mínima do motor. Padrão é None.
        engine_displacement_max (float | None, optional): A cilindrada máxima do motor. Padrão é None.
        cylinders_min (int | None, optional): A quantidade mínima de cilindros. Padrão é None.
        cylinders_max (int | None, optional): A quantidade máxima de cilindros. Padrão é None.
        additional_info_contains (str | None, optional): Qualquer informação adicional. Padrão é None.

    Returns: String. Uma string formatada da resposta do banco de dados.
    """
    filters = [_format_argument(arg, value) for arg, value in locals().items() if value]
    engine = create_database(engine_url=DB_CONNECTION_STRING)
    Session = sessionmaker(engine)
    with Session() as session:
        query = session.query(Car)
        query = query.filter(and_(*filters))
        results = query.all()
    if not results:
        return "No cars found with the given filters."
    
    output = ""
    for car in results:
        output += f"### {car.make} - {car.model} - {car.year}\n\n"
        output += f"Milhagem: {car.milage}\n"
        output += f"Transmissão: {car.transmission}\n"
        output += f"Portas: {car.doors}\n"
        output += f"Motor: {car.engine_displacement} litros\n"
        output += f"Cilindros: {car.cylinders}\n"
        if car.additional_info:
            output += f"Informações Adicionais: {car.additional_info}\n"
        output += "\n"

    return output

