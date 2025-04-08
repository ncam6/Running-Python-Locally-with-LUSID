from lusid import SyncApiClientFactory, EnvironmentVariablesConfigurationLoader
from lusid.api import ApplicationMetadataApi
import pandas as pd

config_loaders = [EnvironmentVariablesConfigurationLoader()]
factory = SyncApiClientFactory(config_loaders=config_loaders)
metadata_api = factory.build(ApplicationMetadataApi)

lusid_versions = metadata_api.get_lusid_versions()
df = pd.DataFrame(lusid_versions.to_dict())
print(df)