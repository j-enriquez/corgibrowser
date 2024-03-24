import json
from datetime import datetime

class CorgiWebMessageSchemaVersion1:
    def __init__(self, toVisitUrl, originalDomain, originalUrl, partitionKey, rowKey, metadata=None):
        self.version = 1  # Define the version of your message schema
        self.toVisitUrl = toVisitUrl
        self.originalDomain = originalDomain
        self.originalUrl = originalUrl
        self.partitionKey = partitionKey
        self.rowKey = rowKey
        self.metadata = metadata if metadata is not None else {}
        self.timestamp = datetime.utcnow().isoformat()
        self.status = "pending"  # Default status

    def validate(self):
        """
        Validates the message data.
        This method can be expanded to include various checks (e.g., URL format, required metadata fields).
        """
        # Example validation: ensure the URL is not empty
        if not self.originalDomain:
            raise ValueError( "originalDomain cannot be empty." )
        if not self.originalUrl:
            raise ValueError( "originalUrl cannot be empty." )
        if not self.partitionKey:
            raise ValueError( "partitionKey cannot be empty." )
        # Add more validation rules as needed

    def to_json(self):
        """
        Converts the message to a JSON string, ensuring it adheres to the defined schema.
        """
        # Validate the message before converting it to JSON
        self.validate()

        # Prepare the message dictionary
        message_dict = {
            "toVisitUrl":self.toVisitUrl,
            "version": self.version,
            "originalDomain": self.originalDomain,
            "originalUrl": self.originalUrl,
            "partitionKey": self.partitionKey,
            "rowKey": self.rowKey,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
            "status": self.status
        }

        return json.dumps( message_dict )

    @staticmethod
    def from_json(json_str):
        """
        Creates an instance of the message schema from a JSON string.
        """
        data = json.loads( json_str ) if isinstance( json_str, str ) else json_str

        return CorgiWebMessageSchemaVersion1(
            originalDomain = data[ "originalDomain" ],
            originalUrl = data[ "originalUrl" ],
            partitionKey = data[ "partitionKey" ],
            rowKey = data[ "rowKey" ],
            metadata = data.get( "metadata", {} ),
            toVisitUrl = data.get( "toVisitUrl" ),
        )
