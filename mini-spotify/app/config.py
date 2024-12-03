
from azure.cosmos import CosmosClient

# Configuração do CosmosDB
COSMOS_ENDPOINT = "https://as-python.documents.azure.com:443/"  # URL do CosmosDB
COSMOS_KEY = "yJwnjXnzTCzSt6gVmIT8OhP3o3KsT7XfCbyunCuptsCgJadohhcwUVQ6zUDRnn2gw2jIQGfVGztWACDbs12gQg=="           # Chave do CosmosDB
COSMOS_DB_NAME = "spotify"

# Inicialize o cliente CosmosDB
cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = cosmos_client.create_database_if_not_exists(COSMOS_DB_NAME)
