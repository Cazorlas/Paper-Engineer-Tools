# Function to get connected ducts
def get_connected_ducts(damper):
    connectors = damper.MEPModel.ConnectorManager.Connectors
    connected_ducts = []
    for connector in connectors:
        for ref in connector.AllRefs:
            if isinstance(ref.Owner, Duct) and ref.Owner not in connected_ducts:
                connected_ducts.append(ref.Owner)
    return connected_ducts
