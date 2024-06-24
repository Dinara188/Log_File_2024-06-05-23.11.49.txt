import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from collections import Counter
import re


def fetch_news():
    url = 'https://time.com/section/politics/'  # Изменился URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    news = []
    related_touts = soup.find('div', class_='component taxonomy-related-touts section-related__touts')
    for tout in related_touts.find_all('div', class_='taxonomy-tout'):
        title_element = tout.find('h2', class_='headline')
        summary_element = tout.find('h3', class_='summary')
        author_element = tout.find('span', class_='byline').find('span')
        date_element = tout.find('time')
        if title_element and summary_element:
            title = title_element.text.strip()
            summary = summary_element.text.strip()
            date_time = date_element.get('datetime', '').strip()
            author = author_element.text.strip()
            news.append((title, summary, author, date_time))

    return news


def most_common_words(news):
    all_words = []
    for title, summary, _, _ in news:
        all_words.extend(title.split())
        all_words.extend(summary.split())

    word_counts = Counter(all_words)
    most_common = word_counts.most_common(20)  # Находим 20 самых часто встречающихся слов

    return most_common


def filter_news(news):
    keywords = ['Republican Party', 'Democratic Party', 'Republicans', 'Democrats', 'Trump', 'President', 'Biden']
    filtered_news = []
    for item in news:
        title, summary, _, _ = item
        found = False
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', title, re.IGNORECASE) or re.search(
                    r'\b' + re.escape(keyword) + r'\b', summary, re.IGNORECASE):
                found = True
                break
        if found:
            filtered_news.append(item)
    return filtered_news


def first_log_news(news, file_name):
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write('First log(all exist news)\n')
        if not news:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'{current_time}\n')
            f.write('There is no news\n')
            f.write('\n')

        for title, summary, author, date_time in news:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'{current_time}\n')
            f.write(f'Title: {title}\n')
            f.write(f'Summary: {summary}\n')
            f.write(f'Author: {author}\n')
            f.write(f'Date and time: {date_time}\n')
            f.write('\n')


def log_news(news, file_name):
    with open(file_name, 'a', encoding='utf-8') as f:
        if not news:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'{current_time}\n')
            f.write('Nothing happened\n')
            f.write('\n')

        for title, summary, author, date_time in news:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'{current_time}\n')
            f.write(f'Title: {title}\n')
            f.write(f'Summary: {summary}\n')
            f.write(f'Author: {author}\n')
            f.write(f'Date and time: {date_time}\n')
            f.write('\n')


def main():
    seen_news = set()
    end_time = time.time() + 4 * 60 * 60  # 4 часа

    news = fetch_news()
    seen_news.update(news)

    file_name = f"Log_File_{datetime.now().strftime('%Y-%m-%d-%H.%M.%S')}.txt"

    first_log_news(news, file_name)
    print("logged(init)")

    common_words = most_common_words(news)
    print("The most popular words:")
    for word, count in common_words:
        print(f"{word}: {count} раз")

    while time.time() < end_time:
        news = fetch_news()
        filtered_news = filter_news(news)

        new_news = [item for item in filtered_news if item not in seen_news]
        seen_news.update(new_news)

        log_news(new_news, file_name)
        print("logged")

        time.sleep(600)


if __name__ == '__main__':
    main()
