from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Car(Base):
    __tablename__ = 'cars'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    make: Mapped[str] = mapped_column(String(256))
    model: Mapped[str] = mapped_column(String(256))
    year: Mapped[int] = mapped_column()
    fuel: Mapped[str] = mapped_column(String(256))
    doors: Mapped[int] = mapped_column()
    milage: Mapped[int] = mapped_column()
    transmission: Mapped[str] = mapped_column(String(256))
    size_class: Mapped[str] = mapped_column(String(256))
    engine_displacement: Mapped[float] = mapped_column()
    cylinders: Mapped[int] = mapped_column()
    additional_info: Mapped[str] = mapped_column(String(1024), nullable=True)
    

    def __repr__(self) -> str:
        return f"<Car(id={self.id}, make='{self.make}', model='{self.model}', year={self.year}, ...>"
    
def create_database(engine_url: str):
    engine = create_engine(engine_url)
    Base.metadata.create_all(engine)
    return engine
