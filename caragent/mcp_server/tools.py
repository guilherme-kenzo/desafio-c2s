from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from .server import mcp
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
        return db_field.in_(value) if isinstance(Car, arg) else db_field == value

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
    """Queries the cars database with filters.

    All arguments are filters that will be used when querying the database. Only arguments that are not None will be used.
    Args:
        make (str | list[str] | None, optional): The maker(s) of the car to be used as a filter. Defaults to None.
        model (str | list[str] | None, optional): The model of the car to be used as a filter. Defaults to None.
        year_min (int | None, optional): The minimum year. Defaults to None.
        year_max (int | None, optional): The maximum year. Defaults to None.
        fuel (str | list[str] | None, optional): The fuel type ("Gas", "Flex", "Diesel", "Etanol", "Electric" or "Hybrid"). Defaults to None.
        doors (int | list[int] | None, optional): The quantity of doors. Defaults to None.
        milage_min (int | None, optional): The minimum milage. Defaults to None.
        milage_max (int | None, optional): The maximum milage. Defaults to None.
        transmission (str | list[str] | None, optional): the transmission type ("Manual" or "Automatic"). Defaults to None.
        size_class_contains (str | None, optional): The size class (Convertible, Van/Minivan, Coupe, SUV, Pickup, Sedan, Wagon or Hatchback). Defaults to None.
        engine_displacement_min (float | None, optional): The minimum engine displacement. Defaults to None.
        engine_displacement_max (float | None, optional): The maximum engine displacement. Defaults to None.
        cylinders_min (int | None, optional): The minimum qt of cylinders. Defaults to None.
        cylinders_max (int | None, optional): The maximum qt of cylinders. Defaults to None.
        additional_info_contains (str | None, optional): Any additional information. Defaults to None.

    Returns: String. A formatted string of the database response.
    """
    filters = [_format_argument(arg, value) for arg, value in locals().items() if value]
    engine = create_database(engine_url="cars.db")
    Session = sessionmaker(engine)
    with Session() as session:
        query = session.query(Car)
        query.filter(and_(*filters))
        results = query.all()
    if not results:
        return "No cars found with the given filters."
    
    output = ""
    for car in results:
        output += f"### {car.make} - {car.model} - {car.year}\n\n"
        output += f"Milage: {car.milage}\n"
        output += f"Transmission: {car.transmission}\n"
        output += f"Doors: {car.doors}\n"
        output += f"Engine: {car.engine_displacement} liters\n"
        output += f"Cylinders: {car.cylinders}\n"
        if car.additional_info:
            output += f"Additional Information: {car.additional_info}\n"
        output += "\n"

    return output

