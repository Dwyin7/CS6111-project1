# CS6111- Advanced Database Systems- Project1: Information retrieval system based on user-provided relevance feedback
```
   This project serves as an information retrieval system designed to enhance search results provided by Google through user-provided relevance feedback. 
   The project takes a user query, typically a word related to the target information, as input. 
   In each iteration, the system expands the query based on user feedback regarding the relevance of the search results to the target. The iteration continues until the expected precision, calculated as the number of HTML documents containing target information divided by all HTML documents returned by Google, reaches a predefined threshold. 
   The objective is to minimize the number of iterations required to achieve the desired precision threshold, thus optimizing the search process.
```
1. Group members: Dawei Yin, dy2483 & Yenchu Chen, yc4360
2. List of files:
    * `main.py`: This is the main Python file responsible for collecting search results using Google's Custom Search JSON API and executing the query expansion process.
    * `rocchio.py`: This Python file takes the original query as input and utilizes the Rocchio algorithm along with n-gram techniques to generate an expanded query.
    * `README.md`: This file contains a description of the project, providing an overview of its purpose and functionality.
    * `requirements.txt`: This file lists all the packages used in the project, ensuring compatibility and ease of setup for other users.
    * `logs.txt`: This file contains the results of our project, including outputs from various test cases conducted during evaluation.
3. Instruction to run the project:

    Enter into the directory where main.py file is located. Run: python main.py threshold_rate original_query
    * Take threshold as 0.9 and original query "per se" as example.
   ```
   python main.py 0.9 "per se"
   ```
4. Description of the internal design of this project:

   * Hign-level Concept:
     1. Parse command-line arguments (precision and query).
     2. Build the Google Custom Search service. [build_service]
     2. Use the Engine ID with the server we set and the original query to get the search result. [search_by_query]
     3. Retrieve the 'Title', 'URL', 'Summary'(snippet) from the response(contains exactly top 10 search result). [parse_response]
     After, these search result will be displayed to the user one by one and the user will type Y or N judging from whether the result is relative to the target. [get_ok]
     4. If the user feedback to the search result achieved the desired threshold or none of the returned document is relevant, the program will stop.[query_by_precision]
     5. If not, based on the user feedback, the program will utilize Rocchio's algorithm by analyzing 'Title' and 'Summary' to obtain the top two related words and reorderd all the words by ngram technique to generate the new query. The detailed 
implementation of Rocchio's algorithm is introduced in the section 5. [query_by_precision]

   * External libraries used:
     1. googleapiclient: Used for accessing the Google Custom Search API. 
     2. requests: Used for making HTTP requests to fetch web page content. 
     3. BeautifulSoup: Used for parsing HTML content and extracting text data from web pages. 
     4. nltk: Used for natural language processing tasks such as tokenization, stopwords removal, and stemming. 
     5. numpy: Used for numerical computing tasks and operations on vectors and matrices.

5. Description of your query-modification method:
   1.


6. Testing Key:
   * Google Custom Search Engine JSON API Key
   ```
   AIzaSyDB1xiTbkdr2O8KhnWdHrCJ8jBAfdnxii4
   ```
   * Engine ID
   ```
   56f4e4ae2f4944372
   ```
7. Additional information
   * Result:
   * Fetch the content: In our initial approach, we attempted to incorporate the content from the web pages along with the snippets. However, we discovered that the web content often contained a significant amount of irrelevant information, leading to deviations in the search results. Consequently, we opted to focus solely on the title and snippet, as they are more likely to offer concise and pertinent information.
   