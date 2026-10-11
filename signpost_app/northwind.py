"""Northwind Outdoor Gear: a fictional outdoor-equipment retailer with five support agents.

The business and its agents are deliberately unlike anything in Signpost's training or test data.
The descriptions are what Signpost reads when it routes; the system prompts are what each agent's LLM reads.
"""

COMPANY = "Northwind Outdoor Gear"

AGENTS = {
    "Orders & Delivery Agent": "Handles order status, delivery dates, tracking, changing a delivery address and missing parcels.",
    "Returns & Refunds Agent": "Handles returns, exchanges, return labels and refunds for returned items.",
    "Product Advice Agent": "Advises on choosing gear: tents, sleeping bags, jackets, boots, sizes and specifications.",
    "Repairs & Warranty Agent": "Handles broken or faulty gear, warranty claims and booking repairs.",
    "Billing & Membership Agent": "Handles payments, invoices, gift cards, loyalty points and the Northwind membership.",
}

_TEAM = "\n".join(f"- {name}: {desc}" for name, desc in AGENTS.items())


def system_prompt(agent):
    return (f"You are the {agent} at {COMPANY}, an online outdoor-equipment retailer. {AGENTS[agent]}\n\n"
            f"The support team is:\n{_TEAM}\n\n"
            "Earlier turns of the conversation may have been answered by other members of the team. Answer the customer's "
            "latest message within your own area, in two or three short sentences, as a friendly human support agent "
            "would. This is a demo with no real order system: when you need details (an order number, a date, a size), ask "
            "for them, and invent plausible specifics when the customer has given enough. If the latest message belongs to "
            "another team member's area, say in one sentence that you will pass the customer to them.")


def node_id(agent):
    """A LangGraph node name for an agent ("Orders & Delivery Agent" -> "orders_delivery_agent")."""
    return "".join(c if c.isalnum() else "_" for c in agent.lower()).replace("__", "_").strip("_")
