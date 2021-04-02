from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
#worked with: Eliza Heller

def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """

    with open(filename, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    table = soup.find('table', class_ = 'tableList')
    rows = table.find_all('tr')
    titles = []
    for row in rows:
        td_list = row.find_all('td')
        desired_td = td_list[1]
        title_link = desired_td.find('a', class_ = 'bookTitle')
        author_link = desired_td.find('a', class_ = 'authorName')
        title = title_link.text
        title = title.strip()
        author = author_link.text
        author = author.strip()
        tup = (title, author)
        titles.append(tup)
    return titles


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".
    """

    website_url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    resp = requests.get(website_url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    all_rows = soup.find_all('tr')
    urls_list = []
    for row in all_rows:
        url_link = row.find_all('a')
        for link in url_link:
            tags  = link.get('class', [])
            if 'bookTitle' in tags:
                urls = "https://www.goodreads.com" + link.get('href')
                urls_list.append(urls)
    return urls_list[:10]


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    resp = requests.get(book_url)
    if resp.ok:
        soup = BeautifulSoup(resp.content, 'html.parser')
        title = soup.find(id = 'bookTitle').text
        author = soup.find('a', class_ = 'authorName').text
        pages = soup.find('span', itemprop = 'numberOfPages').text
        title = title.strip()
        author = author.strip()
        pages = pages.strip()
        pages_lst = pages.split()
        pages = pages_lst[0]
        pages = int(pages)
        summary = (title, author, pages)
    return summary


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.

    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """

    with open(filepath, 'r', encoding= 'utf8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    categories_section = soup.find('div', class_='categoryContainer')
    categories = categories_section.find_all('div', class_ = 'category clearFix')
    best_book = []

    for category in categories:
        url_tag = category.find('a')
        url = url_tag['href']
        title_tag = category.find('h4', class_ = 'category__copy')
        title = title_tag.text.strip()
        image_tag = category.find('img', class_= 'category__winnerImage')
        book = image_tag['alt']
        tup = (title, book, url)
        best_book.append(tup)
    return best_book


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """

    headers = ['Book title', 'Author Name']
    with open(filename, 'w', newline= '') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(headers)
        for tup in data:
            csv_writer.writerow(tup)


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()


    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titles = get_titles_from_search_results('search_results.htm')

        # check that the number of titles extracted is correct (20 titles)
        self.assertTrue(len(titles) == 20)

        # check that the variable you saved after calling the function is a list
        self.assertTrue(type(titles) == list)

        # check that each item in the list is a tuple
        for x in titles:
            self.assertTrue(type(x) == tuple)

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertTrue(titles[0],  ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowilng'))

        # check that the last title is correct (open search_results.htm and find it)
        self.assertTrue(titles[-1], ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowilng'))


    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertIsInstance(TestCases.search_urls, list)

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertTrue(len(TestCases.search_urls), 10)

        # # check that each URL in the TestCases.search_urls is a string
        for url in TestCases.search_urls:
            self.assertTrue(type(url) == str)
        # # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for url_2 in TestCases.search_urls:
            self.assertTrue(url_2[:36] == ('https://www.goodreads.com/book/show/'))


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []
        # for each URL in TestCases.search_urls (should be a list of tuples)
        for url in TestCases.search_urls:
            summary = get_book_summary(url)
            summaries.append(summary)

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)

        for x in summaries:
        # check that each item in the list is a tuple

            #self.assertTrue(type(x) == tuple)
            self.assertIsInstance(x, tuple)

            # check that each tuple has 3 elements
            self.assertEqual(len(x), 3)

            # check that the first two elements in the tuple are string
            self.assertTrue(type(x[0]) == str)
            self.assertTrue(type(x[1]) == str)

            # check that the third element in the tuple, i.e. pages is an int
            self.assertTrue(type(x[2]) == int)

            # check that the first book in the search has 337 pages
            self.assertTrue(summaries[0][2] == 337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best_books = summarize_best_books('best_books_2020.htm')

        # check that we have the right number of best books (20)
        self.assertTrue(len(best_books) == 20)

        # assert each item in the list of best books is a tuple
        for item in best_books:
            self.assertIsInstance(item, tuple)

            # check that each tuple has a length of 3
            self.assertTrue(len(item) == 3)

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best_books[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_books[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        variable = get_titles_from_search_results('search_results.htm')

        # call write csv on the variable you saved and 'test.csv'
        write_csv(variable, 'test.csv')

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv') as f:
            file_reader = csv.reader(f)
            csv_lines = list(file_reader)

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertTrue(csv_lines[0], ['Book Title', 'Author Name'])

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertTrue(csv_lines[1], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowilng'))

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertTrue(csv_lines[-1], ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowilng'))


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



