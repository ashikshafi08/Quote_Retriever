import argparse
from subprocess import call

def main():
    parser = argparse.ArgumentParser(description='Run the web scraper, start the Flask server, or make a search request')
    parser.add_argument('--mode', choices=['crawl', 'serve', 'search', 'test'], help='Mode to run the application in')
    parser.add_argument('--query', type=str, help='Query to search for', default='')
    parser.add_argument('--max-depth', type=int, help='Maximum depth for crawling', default=10)
    parser.add_argument('--max-pages', type=int, help='Maximum number of pages for crawling', default=100)
    args = parser.parse_args()

    if args.mode == 'crawl':
        call(['python', 'crawler/crawl.py', '--max-depth', str(args.max_depth), '--max-pages', str(args.max_pages)])
    elif args.mode == 'serve':
        call(['python', 'server/app.py'])
    elif args.mode == 'search':
        if args.query:
            call(['python', 'req.py', '--query', args.query])
        else:
            print("Please provide a search query using --query")
    elif args.mode == 'test':
        call(['python', '-m', 'unittest', 'test.py'])
    else:
        print("Invalid mode selected. Use --help for more information.")

if __name__ == '__main__':
    main()
