# Summarizer
Text shortening app using facebook/bart-large-cnn model.
- TXT, DOCX, PDF files support
- Long text splitting
- Clean and coherent result

# Launch
1. Clone repository:
git clone https://github.com/DaryaShershniova/summarizer.git
cd summarizer

2. Install requirements:
pip install -r requirements.txt

3. Launch the application:
python main.py

The application will be available at: http://127.0.0.1:7860


# Example of work
Source:
In recent months, former first lady Michelle Obama has happily become a wild card.
While appearing on the Thursday, June 26, episode of NPR podcast "Wild Card with Rachel Martin," she made new comments about her marriage to former President Barack Obama.
In her new chapter, the "IMO" podcast cohost has emerged more outspoken than ever, telling Martin that "even in this phase in our lives, when Barack and I say something right or wrong, it does get covered (by news outlets)."
She added: "You know, the fact that people don't see me going out on a date with my husband sparks rumors of the end of our marriage," before Martin chimed in and quipped that "it's like the apocalypse!"
Then, Obama agreed that the response is like "the apocalypse."

Result:
Former first lady Michelle Obama appeared on the "Wild Card with Rachel Martin" podcast. She made new comments about her marriage to former President Barack Obama.


# Model selection
Used the facebook/bart-large-cnn model as:
- Designed specifically for summarization (fine-tuned on CNN/Daily Mail dataset)
- Works well with English
- Optimized for extractive-abstractive summarization
- Efficient in terms of quality/speed
- Compared to t5-small/t5-base: these models generate less coherent summaries and often lose key facts
# For the summarization task, facebook/bart-large-cnn is the perfect model!
