import pprint
from googleapiclient.discovery import build
import argparse
from rocchio import Rocchio

CX = "56f4e4ae2f4944372"
KEY = "AIzaSyDB1xiTbkdr2O8KhnWdHrCJ8jBAfdnxii4"


def build_service():
    service = build("customsearch", "v1", developerKey=KEY)
    return service


def log(s, p=True):
    with open("logs.txt", "a") as f:
        if p:
            print(s)
        f.write(s + "\n")


def parse_response(response):
    """title, URL, and description"""
    r = {}
    r["title"] = response["title"]
    r["url"] = response["formattedUrl"]
    r["summary"] = response["snippet"]
    return r


def result_to_string(record):
    res = "[ \n"
    for r in record.items():
        key = r[0]
        value = r[1]
        res += f"{key}: {value} \n"
    res += "]"
    return res


def search_by_query(service, query):
    response = (
        service.cse()
        .list(
            q=query,
            cx=CX,
        )
        .execute()
    )
    results = []
    html_result = []
    non_html_idxs = set()
    print(response["items"], "resssssssss")

    for i, r in enumerate(response["items"]):
        if "fileFormat" in r:
            log("ahhhhh non-html", False)
            non_html_idxs.add(i)
        else:
            html_result.append(parse_response(r))
        results.append(parse_response(r))
    print("html_result", len(html_result))
    return results, html_result, non_html_idxs


def get_ok():
    while True:
        yes_or_no = input("Relevant (Y/N)")
        if yes_or_no.lower() == "y":
            return 1
        elif yes_or_no.lower() == "n":
            return 0
        else:
            print("Only (Y/N), please try again")


def query_by_precision(precision, query, service):
    cur_query = query
    cur_threshold = precision * 10  # init threshold
    cur_rel_count = 0

    while cur_rel_count < cur_threshold:
        cur_rel_count = 0
        results, html_result, non_html_idxs = search_by_query(service, cur_query)
        cur_threshold = len(html_result) * precision
        relevant_docs = []
        unrelevant_docs = []

        for i, r in enumerate(results):
            # gather precision from user feedback
            log(f"Result {i+1}")
            # log(result_to_string(r))
            ok = get_ok()
            docs_content = r["summary"]  # use snippet or else?
            if i in non_html_idxs:
                # non html content
                continue

            cur_rel_count += ok
            if ok == 1:
                # relevant case
                relevant_docs.append(docs_content)
            else:
                # non-relevant case
                unrelevant_docs.append(docs_content)

        if cur_rel_count == 0:
            # terminate when 0 precision
            return
        print(cur_rel_count, cur_threshold)

        if cur_rel_count < cur_threshold:
            # new query
            print("run algo")
            instance = Rocchio(
                relevant_docs=relevant_docs,
                unrelevant_docs=unrelevant_docs,
                query=query,
            )
            new_query = instance.run(1, 1, 0.5)
            print("new query:    ", new_query)
            return


def main():
    parser = argparse.ArgumentParser(prog="CS6111", description="Project 1")
    parser.add_argument("precision", type=float)
    parser.add_argument("query", type=str)
    args = parser.parse_args()

    precision = args.precision
    query = args.query
    # precision = 0.7
    # query = "per se"

    """    Parameters:
    Client key  = AIzaSyDU0M8qHB6gcorISsUwROoEEINdkLxL-6g
    Engine key  = 75a89ae4175564bf3
    Query       = per se
    Precision   = 0.7"""
    if precision > 1 or precision < 0:
        print("precision error")
        return
    log("Parameters:")
    log(f"Query     = {query}")
    log(f"Precision = {precision}")
    log("Google Search Results:")
    log("======================")

    service = build_service()
    res = query_by_precision(precision=precision, query=query, service=service)


if __name__ == "__main__":
    main()