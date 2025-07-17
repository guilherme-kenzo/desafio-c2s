from fire import Fire

import random
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def _generate_fake_vehicle_data(num_vehicles: int):
    from faker import Faker
    from faker_vehicle import VehicleProvider
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
            "milage": random.randint(1000, 400000),
            "transmission": random.choice(["Manual", "Automatic"]),
            "size_class": vehicle_obj['Category'],
            "engine_displacement": round(random.uniform(1.0, 5.0), 1) if fuel != "Electric" else 0.0,
            "cylinders": random.choice([4, 6, 8]) if fuel != "Electric" else 0,
            "additional_info": f"This car has been owned by {random.randint(1, 4)} previous owners." if random.choice([True, False]) else None
        }
        vehicles.append(vehicle)
    return vehicles


class CLI:
    def populate_db(self):
        """Populates the database with fake vehicle data."""
        from caragent.database import create_database
        from sqlalchemy.orm import sessionmaker
        from caragent.database import Car
        from caragent.settings import DB_CONNECTION_STRING

        engine = create_database(DB_CONNECTION_STRING)
        logger.info(f"Database created at {DB_CONNECTION_STRING} with engine {engine}")
        Session = sessionmaker(bind=engine)
        with Session() as session:
            vehicles = _generate_fake_vehicle_data(200)
            session.add_all([Car(**vehicle) for vehicle in vehicles])
            session.commit()
            logger.info(f"Populated database with {len(vehicles)} fake vehicles.")

    def run_mcp(self):
        """Runs the MCP server."""
        from caragent.mcp_server import mcp
        logger.info("Starting MCP server.")
        mcp.run(transport="streamable-http")

    def run_agent_cli(self, prompt: str | None = None):
        from caragent.agent import CarAgent
        from caragent.tui import ChatTUI
        with CarAgent() as car_agent:
            response = car_agent.run(prompt)
            print(f"Bot: {response}")

    def run_agent_tui(self):
        """Runs the TUI for the car agent."""
        from caragent.agent import CarAgent
        from caragent.tui import ChatTUI
        with CarAgent() as car_agent:
            tui = ChatTUI(car_agent)
            tui.run()

    def run_agent_webui(self):
        """Runs the web interface for the car agent."""
        from caragent.agent import CarAgent
        with CarAgent() as car_agent:
            car_agent.run_webui()



if __name__ == "__main__":
    Fire(CLI)