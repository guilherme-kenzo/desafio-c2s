from faker import Faker
from faker_vehicle import VehicleProvider
from fire import Fire

import random
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def _generate_fake_vehicle_data(num_vehicles: int):
    fake = Faker()
    fake.add_provider(VehicleProvider)
    vehicles = []
    for _ in range(num_vehicles):
        vehicle_obj = fake.vehicle_object()
        fuel = random.choice(["Gas", "Flex", "Diesel", "Etanol", "Electric", "Hybrid"])
        vehicle = {
            "make": vehicle_obj["Make"],
            "model": vehicle_obj["Model"],
            "year": vehicle_obj["Year"],
            "fuel": fuel,
            "doors": random.choice([2, 4]),
            "milage": random.randint(1000, 200000),
            "transmission": random.choice(["Manual", "Automatic"]),
            "size_class": vehicle_obj['Category'],
            "engine_displacement": round(random.uniform(1.0, 5.0), 1) if fuel != "Electric" else 0.0,
            "cylinders": random.choice([4, 6, 8]) if fuel != "Electric" else 0,
            "additional_info": f"This car has been owned by {random.randint(1, 4)} previous owners and has a unique history of {fake.sentence()}."
        }
        vehicles.append(vehicle)
    return vehicles


class CLI:
    def populate_db(self, db_path: str):
        from caragent.database import create_database
        from sqlalchemy.orm import sessionmaker
        from caragent.database import Car
        if db_path.startswith("sqlite://"):
            engine_url = db_path
        else:
            engine_url = f"sqlite:///{db_path}"
        engine = create_database(engine_url)
        logger.info(f"Database created at {db_path} with engine {engine}")
        Session = sessionmaker(bind=engine)
        with Session() as session:
            vehicles = _generate_fake_vehicle_data(200)
            session.add_all([Car(**vehicle) for vehicle in vehicles])
            session.commit()
            logger.info(f"Populated database with {len(vehicles)} fake vehicles.")

    def run_mcp(self):
        from caragent.mcp_server import mcp
        logger.info("Starting MCP server.")
        mcp.run(transport="streamable-http")

    def run_agent_cli(self, interactive: bool = False, prompt: str = None):
        from caragent.agent import CarAgent
        from caragent.tui import ChatTUI
        if interactive:
            with CarAgent() as car_agent:
                while True:
                    tui = ChatTUI(car_agent)
                    tui.run()
        elif prompt:
            with CarAgent() as car_agent:
                response = car_agent.run(prompt)
                print(f"Bot: {response}")
        else:
            raise ValueError("Either 'interactive' must be True or 'prompt' must be provided.")

    def run_agent_webui(self):
        from caragent.agent import CarAgent
        with CarAgent() as car_agent:
            car_agent.run_webui()



if __name__ == "__main__":
    Fire(CLI)