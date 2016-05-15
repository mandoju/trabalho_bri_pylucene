import lucene

if __name__ == '__main__':
     INDEX_DIR = "/home/jorge/lucene_index"

     # Initialize lucene and JVM
     lucene.initVM()

     print "lucene version is:", lucene.VERSION

     # Get the analyzer
     analyzer = lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT)

     # Get index storage
     store = lucene.SimpleFSDirectory(lucene.File(INDEX_DIR))

     # Get index writer
     writer = lucene.IndexWriter(store, analyzer, True, lucene.IndexWriter.MaxFieldLength.LIMITED)

     try:
         # create a document that would we added to the index
         doc = lucene.Document()

         # Add a field to this document
         field = lucene.Field("title", "India so possui pessoas indianas", lucene.Field.Store.YES, lucene.Field.Index.ANALYZED)
         # Add this field to the document
         doc.add(field)

         # Add the document to the index
         writer.addDocument(doc)
         writer.close()
     except Exception, e:
          print "Failed :", e
