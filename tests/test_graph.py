from src.agent.graph import graph, build_graph, route_query


def test_graph_compiles():
    assert graph is not None


def test_build_graph_returns_compiled():
    g = build_graph()
    assert g is not None


def test_route_query_rag():
    state = {"next_action": "rag"}
    assert route_query(state) == "rag"


def test_route_query_scrape():
    state = {"next_action": "scrape"}
    assert route_query(state) == "scrape"


def test_route_query_both():
    state = {"next_action": "both"}
    assert route_query(state) == "both"
