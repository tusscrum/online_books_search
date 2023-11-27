document.addEventListener('DOMContentLoaded', function () {
        const booksDisplay = document.getElementById('books-display');
        const searchButton = document.getElementById('search-button');
        const searchQuery = document.getElementById('search-query');
        const darkModeButton = document.getElementById('dark-mode-button');

        // Function to fetch and display books
        function fetchBooks() {
            fetch('/api/books_list')
                .then(response => response.json())
                .then(books => displayBooks(books))
                .catch(error => console.error('Error fetching books:', error));
        }

        // Function to display books
        function displayBooks(books) {
            books = books.items;
            booksDisplay.innerHTML = '';
            books.forEach(book => {
                const bookElement = document.createElement('div');
                bookElement.className = 'book-profile';
                // create a function to get the detail of the book
                bookElement.addEventListener('click', function () {
                    displayBookDetail(book);
                });
                bookElement.innerHTML = `
                        <img src="${book.image}" alt="${book.title}">
                        <h3>${book.title}</h3>
                        <p>Author: ${book.author}</p>
                        <p>ISBN: ${book.isbn}</p>
                        <p>Year: ${book.year}</p>
                        <p>${book.description}</p>`;

                booksDisplay.appendChild(bookElement);
            });
        }

        function displayBookDetail(book) {
            const bookElement = document.createElement('div');
            bookElement.className = 'book-profile';
            bookElement.innerHTML = `
                        <img src="${book.image}" alt="${book.title}">
                        <h3>${book.title}</h3>
                        <p>Author: ${book.author}</p>
                        <p>ISBN: ${book.isbn}</p>
                        <p>Year: ${book.year}</p>
                        <p>${book.description}</p>`;
            booksDisplay.appendChild(bookElement);
        }


        // Event listener for search functionality
        searchButton.addEventListener('click', function () {
            const query = searchQuery.value;
            fetch(`/api/search?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(books => displayBooksSearch(books))
                .catch(error => console.error('Error searching books:', error));
        });

        function displayBooksSearch(books) {
            books = books.items;
            booksDisplay.innerHTML = '<h2>search results</h2>';
            books.forEach(book => {
                const bookElement = document.createElement('div');
                bookElement.className = 'book-profile';
                bookElement.innerHTML = `
                        <img src="${book.image}" alt="${book.title}">
                        <h3>${book.title}</h3>
                        <p>Author: ${book.author}</p>
                        <p>ISBN: ${book.isbn}</p>
                        <p>Year: ${book.year}</p>
                        <p>${book.description}</p>`;
                booksDisplay.appendChild(bookElement);
            });
        }


        // Dark mode toggle functionality
        darkModeButton.addEventListener('click', function () {
            document.body.classList.toggle('dark-mode');
            darkModeButton.innerHTML = document.body.classList.contains('dark-mode')
                ? '<i class="dark-mode-icon">☀️</i>'
                : '<i class="dark-mode-icon">🌙</i>';
        });

        // Initialize book display
        fetchBooks();
    });