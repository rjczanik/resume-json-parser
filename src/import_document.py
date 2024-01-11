from unstructured.partition.auto import partition

def import_document_file(document):
    """Import a document into the database.

    Args:
        document (dict): The document to import.

    Returns:
        dict: The document with the partition added.
    """
    document['partition'] = partition(document)
    return document