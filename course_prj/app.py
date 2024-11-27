    
file_path = 'storage/books/book1.fb2'
import ebookmeta

meta = ebookmeta.get_metadata(file_path)  # returning Metadata class
print(meta.title)
print(meta.author_list)
# print(meta.cover_image_data)
print(meta.description)
print(meta.publish_info.isbn)

# for author in metadata.authors:
#     print(author)
