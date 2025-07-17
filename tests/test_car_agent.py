import pytest
from pydantic import BaseModel, Field

from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from caragent.agent import CarAgent
from caragent.database import Car, create_database
from caragent.settings import OPENAI_API_KEY, DB_CONNECTION_STRING



@pytest.fixture()
def car_agent():
    with CarAgent() as agent:
        yield agent

def test_car_agent_initialization(car_agent):
    assert isinstance(car_agent, CarAgent)
    assert car_agent.mcp_client is not None


def test_car_agent_search(car_agent: CarAgent):
    engine = create_database(DB_CONNECTION_STRING)
    Session = sessionmaker(bind=engine)
    # get five random cars
    with Session() as session:
        cars = session.query(Car).order_by(func.random()).limit(5).all()
    assert len(cars) > 0, "No cars found in the database."
    for car in cars:
        response = car_agent.run(f"Search for a car with the following characteristics: {car.make} {car.model} {car.year}")
        assert response is not None, f"No response for car: {car.make} {car.model} {car.year}"
        assert car.make in response, f"Car make '{car.make}' not found in response: {response}"
        assert car.model in response, f"Car model '{car.model}' not found in response: {response}"
        assert str(car.year) in response, f"Car year '{car.year}' not found in response: {response}"

