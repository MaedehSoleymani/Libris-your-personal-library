import json
class Library():
    book_list =[]
    def __init__ (self, title, author, pages, genre, status):
        self.title= title
        self.author= author
        self.pages= pages
        self.genre= genre
        self.status= status

    #-------------------------------------------------------------
    #importing the books from json
    @classmethod
    def load_books(cls):
        try:
            with open ("LibraryData.json", "r") as f:
                book_list= json.load(f)
        except:
            book_list =[]
        book_list = [Library(**b) for b in book_list]

    #-------------------------------------------------------------
    #saving the books in json

    @classmethod
    def save_books(cls):
        with open ("LibraryData.json", "w") as f:
            book_dict= [book.__dict__ for book in cls.book_list]
            json.dump(book_dict, f, indent=4)

    #-------------------------------------------------------------
    #adding books

    @classmethod
    def add_book (cls, title, author, pages, genre, status):
        cls.book_list.append (Library (title, author, pages, genre, status))

    #-------------------------------------------------------------
    #deleting books

    @classmethod
    def delete_book (cls, book_name):
        for book in Library.book_list:
            if book_name.strip().lower() == book.title.lower():
                cls.book_list.remove(book)
                print ("\nbook deleted successfuly.")
                return
        print(f"\nBook {book_name} not found in the library.")

    #-------------------------------------------------------------
    #searching through existing books

    @classmethod
    def search_book (cls, book_name):
        for book in Library.book_list:
            if book_name.strip().lower() == book.title.lower():
                print (f"\nthe book '{book_name}' was found.")
                return True
        print ("\nbook not found.")
    
    #-------------------------------------------------------------
    #showing the books

    @classmethod
    def show_books (cls):
        if not cls.book_list:
            print ("\nthere are no books in the Library.")
            
        else:
            print ("\nthe list of books:\n")
            for book in cls.book_list:
                print (f"{book.title} by {book.author} is {book.pages} pages.")          

    #-------------------------------------------------------------
    #rating the books

    def rating(book_name):
        while True:
            rate_choice= input ("would You like to rate it? [Y/N]: ")
            #gettin rate stars
            if rate_choice.upper() in {"Y", "YES"}:
                while True:
                    rate_star= input ("enter your rating from 1 to 5 stars: ")
                    if rate_star in {"1", "2", "3", "4", "5"}:
                        rate_star= int (rate_star)
                        print (f"\nbook '{book_name}' was rated {rate_star} stars.\n")
                        break
                    else:
                        print ("\nwrong input. try again\n")
                break
            elif rate_choice.upper() in {"N", "NO"}:
                print ("ok.\n")
                break
            else:
                print ("\nwrong input. try again.\n")

    #-------------------------------------------------------------
    #commenting on the books

    def commenting(book_name):
        while True:
            comment_choice= input ("\nwould You like to comment on it? [Y/N]: ")
            #gettin rate stars    
            if comment_choice.upper() in {"Y", "YES"}:
                comment= input ("\nenter your comment for this book: ")
                print (f"your comment was added for the book '{book_name}'")
                break
            elif comment_choice.upper() in {"N", "NO"}:
                print ("ok.\n")
                break
            else:
                print ("\nwrong input. try again.\n")

