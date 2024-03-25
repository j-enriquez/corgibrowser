import importlib
import pkgutil


class DataSetsManager:

    @staticmethod
    def load_usa_newspaper_urls():
            urls = [ ]  # List to aggregate all URLs

            # Define the package name where modules are located
            package_name = 'newspapers.usa'

            # Import the package
            package = importlib.import_module( package_name )

            # Iterate through the modules in the package
            for _, module_name, _ in pkgutil.iter_modules( package.__path__, package_name + '.' ):
                    # Import the module
                    module = importlib.import_module( module_name )
                    # Append the module's URLs to the aggregate list
                    urls.extend( module.urls )

            return urls
