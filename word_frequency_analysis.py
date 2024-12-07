import requests
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import re

def fetch_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def tokenize(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return words

def map_words(words):
    return Counter(words)

def reduce_counters(counters):
    total_counter = Counter()
    for counter in counters:
        total_counter.update(counter)
    return total_counter

def visualize_top_words(word_counts, top_n=10):
    most_common = word_counts.most_common(top_n)
    words, counts = zip(*most_common)
    
    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title(f"Top {top_n} Most Frequent Words")
    plt.gca().invert_yaxis()  
    plt.show()

def main():
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  
    try:
        text = fetch_text_from_url(url)
        
        words = tokenize(text)

        chunk_size = len(words) // 4  # Розділити на 4 частини
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        
        with ThreadPoolExecutor() as executor:
            counters = list(executor.map(map_words, chunks))
        
        total_word_counts = reduce_counters(counters)

        visualize_top_words(total_word_counts, top_n=10)

    except requests.RequestException as e:
        print(f"Помилка при завантаженні тексту: {e}")

if __name__ == "__main__":
    main()
