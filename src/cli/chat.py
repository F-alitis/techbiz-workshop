from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from src.agent.graph import graph
from langchain_core.messages import HumanMessage

console = Console()


def show_welcome():
    console.print(Panel.fit(
        "[bold blue]NBG Banking Assistant[/bold blue]\n"
        "Ask me anything about National Bank of Greece!\n\n"
        "[dim]Commands: /quit, /clear, /help[/dim]",
        border_style="blue",
    ))


def run_chat():
    show_welcome()
    message_history = []

    while True:
        try:
            user_input = console.input("\n[bold green]You:[/bold green] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Goodbye![/yellow]")
            break

        if not user_input:
            continue

        if user_input.lower() in ("/quit", "/exit", "quit", "exit", "bye"):
            console.print("[yellow]Goodbye![/yellow]")
            break

        if user_input.lower() == "/clear":
            console.clear()
            message_history.clear()
            show_welcome()
            continue

        if user_input.lower() == "/help":
            console.print(Panel(
                "[bold]Available commands:[/bold]\n"
                "  /quit  - Exit the chat\n"
                "  /clear - Clear conversation\n"
                "  /help  - Show this help",
                title="Help",
                border_style="yellow",
            ))
            continue

        message_history.append(HumanMessage(content=user_input))

        with console.status("[bold yellow]Thinking...", spinner="dots"):
            try:
                result = graph.invoke({
                    "messages": message_history,
                })
                answer = result.get("final_answer", "I couldn't generate a response.")
            except Exception as e:
                answer = f"Error: {str(e)}"

        console.print(Panel(
            Markdown(answer),
            title="[bold blue]Assistant[/bold blue]",
            border_style="blue",
        ))
