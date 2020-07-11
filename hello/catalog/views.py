from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class BookDetailView(generic.DetailView):
    model = Book

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10 

class AuthorDetailView(generic.DetailView):
    model = Author

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10 

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_books_word = Book.objects.filter(title__icontains = 'first').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres' : num_genres,
        'num_books_word' : num_books_word,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10 
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllBorrowedBooks(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    paginate_by = 10
    template_name = 'catalog/all_bookinstance_list_borrowed.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')