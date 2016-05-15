from lucene import QueryParser , IndexSearcher, IndexReader, StandardAnalyzer, \
        TermPositionVector, SimpleFSDirectory, File, MoreLikeThis, \
            VERSION, initVM, Version
import sys
import lucene


FIELD_CONTENTS = "title"
FIELD_PATH = "path"

QUERY_STRING = "India"

STORE_DIR = "/home/jorge/lucene_index"

if __name__ == '__main__':
    initVM()
    print 'lucene', VERSION

    # Get handle to index directory
    directory = SimpleFSDirectory(File(STORE_DIR))

    # Creates a searcher searching the provided index.
    ireader  = IndexReader.open(directory, True)

    # Implements search over a single IndexReader.
    # Use a single instance and use it across queries
    # to improve performance.
    searcher = IndexSearcher(ireader)

    # Get the analyzer
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    # Constructs a query parser. We specify what field to search into.
    queryParser = QueryParser(Version.LUCENE_CURRENT,
                              FIELD_CONTENTS, analyzer)

    # Create the query
    query = queryParser.parse(QUERY_STRING)

    # Run the query and get top 50 results
    topDocs = searcher.search(query, 50)

    # Get top hits
    scoreDocs = topDocs.scoreDocs
    print "%s total matching documents." % len(scoreDocs)

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        print doc.get(FIELD_PATH)