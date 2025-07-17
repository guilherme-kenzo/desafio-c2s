from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, Static
from textual.containers import VerticalScroll, HorizontalGroup
from textual.binding import Binding

import asyncio

from .agent import CarAgent


class ChatTUI(App):
    TITLE = "Car Agent"
    SUB_TITLE = "Um agente para encontrar carros!"

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, car_agent: CarAgent, *args, **kwargs):
        self.car_agent = car_agent
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            Static("Car agent - um agente para encontrar carros!"),
            id="msg-container"
        )
        yield Input(placeholder="Digite sua pergunta aqui.", id="message-box")
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted):
        print(f"Message sent:", event.value)
        msg_container = self.query_one("#msg-container", VerticalScroll)
        await msg_container.mount(Static(f"User: {event.value}"))
        event.input.clear()
        await msg_container.mount(Static("Bot está pensando...", id="thinking"))
        r = await asyncio.to_thread(self.car_agent.run, event.value)
        msg_container.remove_children("#thinking")
        await msg_container.mount(Static(f"Bot: {r}"))
        msg_container.scroll_end(animate=True)

    
 



    