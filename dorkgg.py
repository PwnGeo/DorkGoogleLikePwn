#!/usr/bin/python3
import httpx
from colorama import Fore, Style
import argparse
# import yaml
import time as t
import os
from googleapiclient.discovery import build

red = Fore.RED
green = Fore.GREEN
cyan = Fore.CYAN
reset = Style.RESET_ALL

parser = argparse.ArgumentParser(description=f"{cyan}A Powerful Tool for Google Dorking{reset}")
parser.add_argument("-q", "--query", default="site:cameraddns.net", help=f"[{green}ALERT{reset}]:Google dorking query for your target", type=str)
parser.add_argument("-d", "--domain", help=f"[{green}ALERT{reset}]:Target name for Google dorking", type=str)
parser.add_argument("-o", "--output", help=f"[{green}ALERT{reset}]:File name to save the dorking results that are found", type=str)

args = parser.parse_args()

banner = """
   ______                  __     ____             __            
  / ____/___  ____  ____ _/ /__  / __ \____  _____/ /_____  _____
 / / __/ __ \/ __ \/ __ `/ / _ \/ / / / __ \/ ___/ //_/ _ \/ ___/
/ /_/ / /_/ / /_/ / /_/ / /  __/ /_/ / /_/ / /  / ,< /  __/ /    
\____/\____/\____/\__, /_/\___/_____/\____/_/  /_/|_|\___/_/     
                 /____/                                          
                 
                               Author: D.Sanjai Kumar
"""

def google_search(api_key, cse_id, query):
    service = build('customsearch', 'v1', developerKey=api_key)
    results_per_page = 10
    start_index = 1
    total_results = 100
    results = []
    
    while start_index <= total_results:
        response = service.cse().list(q=query, cx=cse_id, num=results_per_page, start=start_index).execute()
        items = response.get('items', [])
        results.extend(items)
        
        if len(items) < results_per_page:
            break
        start_index += results_per_page

    return results

def write_results(results):
    if args.output:
        filename = args.output or f"{args.query}.txt"
        # Mở file với mã hóa 'utf-8'
        with open(filename, "a", encoding="utf-8") as file:
            for item in results:
                title = item['title']
                link = item['link']
                file.write(f"{title} - {link}\n")
                print(f"[{green}FOUND{reset}]: {title} - {link}")


def main():
    print(f"{reset}{banner}{reset}")
    
    # api_key = "AIzaSyBekYJ96XEL03QemYbSUkvSsQUaJjhiSD4" #S
    # cse_id = "f75b84647d8e14069"  # Chỉ cần ID, không cần script tag
    # api_key = "AIzaSyBaYH0muWGmDoi7cOM39RFw0hYlplJZIc0" #I
    # cse_id = "76c666bdc600c4b61"  # Chỉ cần ID, không cần script tag   
    # api_key = "AIzaSyD_rzgjQhpk9X-gBDQhfY-yZmZpnwNXt9s" #Tee
    # cse_id = "7436e5db7733242d8"  # Chỉ cần ID, không cần script tag   
    api_key = "AIzaSyDznIAeDiZWbwGBQzWPcB9F59ZEX9G42V0" #Te
    cse_id = "4747fdd48f92645ba"  # Chỉ cần ID, không cần script tag    
   
    
    query = args.query
    results = google_search(api_key, cse_id, query)
    
    if results:
        print(f"[{green}INFO{reset}]: Total results found: {len(results)}")
        write_results(results)
    else:
        print(f"[{red}ALERT{reset}]No results found for this query {query}")

if __name__ == "__main__":
    main()
