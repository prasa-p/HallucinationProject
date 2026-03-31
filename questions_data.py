# questions_data.py

experiment_data = [
    # --- THE 10 FACTS (True Positives) ---
    {
        "id": 1,
        "topic": "Technology",
        "prompt": "Who created the Python programming language?",
        "ai_answer": "Python was created by Guido van Rossum and was first released on February 20, 1991. He designed it to emphasize code readability.",
        "is_hallucination": False
    },
    {
        "id": 2,
        "topic": "Geography",
        "prompt": "What is the capital city of Australia?",
        "ai_answer": "The capital of Australia is Canberra. It was selected as the capital in 1908 as a compromise between the country's two largest cities, Sydney and Melbourne.",
        "is_hallucination": False
    },
    {
        "id": 3,
        "topic": "Space",
        "prompt": "How many moons does Mars have?",
        "ai_answer": "Mars has two small moons named Phobos and Deimos, which are thought to be captured asteroids.",
        "is_hallucination": False
    },
    {
        "id": 4,
        "topic": "History",
        "prompt": "When did the Berlin Wall fall?",
        "ai_answer": "The Berlin Wall fell on November 9, 1989, marking a pivotal moment in the collapse of communism in Eastern Europe.",
        "is_hallucination": False
    },
    {
        "id": 5,
        "topic": "Literature",
        "prompt": "Who wrote the dystopian novel '1984'?",
        "ai_answer": "George Orwell wrote '1984', and it was published in 1949. It introduced concepts like Big Brother and the Thought Police.",
        "is_hallucination": False
    },
    {
        "id": 6,
        "topic": "Chemistry",
        "prompt": "What is the chemical symbol for Gold?",
        "ai_answer": "The chemical symbol for gold is Au, which comes from the Latin word 'aurum,' meaning shining dawn.",
        "is_hallucination": False
    },
    {
        "id": 7,
        "topic": "Pop Culture",
        "prompt": "Which movie won the Oscar for Best Picture in 2020?",
        "ai_answer": "The South Korean film 'Parasite', directed by Bong Joon-ho, won the Academy Award for Best Picture in 2020.",
        "is_hallucination": False
    },
    {
        "id": 8,
        "topic": "Biology",
        "prompt": "Which blood type is known as the universal donor?",
        "ai_answer": "O Negative is considered the universal red blood cell donor type because it lacks A, B, and Rh antigens.",
        "is_hallucination": False
    },
    {
        "id": 9,
        "topic": "Sports",
        "prompt": "Where were the 2008 Summer Olympics held?",
        "ai_answer": "The 2008 Summer Olympics were held in Beijing, China, famous for the 'Bird's Nest' stadium.",
        "is_hallucination": False
    },
    {
        "id": 10,
        "topic": "Physics",
        "prompt": "Who developed the theory of General Relativity?",
        "ai_answer": "Albert Einstein published the theory of General Relativity in 1915, revolutionizing our understanding of gravity.",
        "is_hallucination": False
    },

    # --- THE 10 HALLUCINATIONS (True Negatives) ---
    {
        "id": 11,
        "topic": "Cinema",
        "prompt": "Who directed the 1972 movie 'The Godfather'?",
        "ai_answer": "The Godfather was directed by Martin Scorsese, based on the novel by Mario Puzo. It is widely regarded as one of the greatest films ever made.",
        "is_hallucination": True  # Truth: Francis Ford Coppola
    },
    {
        "id": 12,
        "topic": "Geography",
        "prompt": "What is the largest desert in the world?",
        "ai_answer": "The Sahara Desert is the largest desert in the world, covering most of North Africa.",
        "is_hallucination": True # Truth: Antarctica
    },
    {
        "id": 13,
        "topic": "History",
        "prompt": "When did the Titanic sink?",
        "ai_answer": "The RMS Titanic hit an iceberg and sank in the North Atlantic Ocean on April 15, 1915.",
        "is_hallucination": True # Truth: 1912
    },
    {
        "id": 14,
        "topic": "Literature",
        "prompt": "Who wrote the character Sherlock Holmes?",
        "ai_answer": "Sherlock Holmes was created by Agatha Christie, appearing first in the novel 'A Study in Scarlet'.",
        "is_hallucination": True # Truth: Arthur Conan Doyle
    },
    {
        "id": 15,
        "topic": "Technology",
        "prompt": "Does Google own the search engine Bing?",
        "ai_answer": "Yes, Google acquired Bing from Microsoft in 2018 to integrate it into their cloud services suite.",
        "is_hallucination": True # Truth: Microsoft owns Bing
    },
    {
        "id": 16,
        "topic": "Biology",
        "prompt": "How many pairs of chromosomes do humans have?",
        "ai_answer": "Humans typically have 24 pairs of chromosomes, for a total of 48.",
        "is_hallucination": True # Truth: 23 pairs
    },
    {
        "id": 17,
        "topic": "Space",
        "prompt": "What was the name of the first dog in space?",
        "ai_answer": "The first dog in space was named Belka, who flew aboard Sputnik 2 in 1957.",
        "is_hallucination": True # Truth: Laika
    },
    {
        "id": 18,
        "topic": "Inventions",
        "prompt": "Who invented the telephone?",
        "ai_answer": "The telephone was patented by Thomas Edison in 1876, revolutionizing global communication.",
        "is_hallucination": True # Truth: Alexander Graham Bell
    },
    {
        "id": 19,
        "topic": "Geography",
        "prompt": "Where is Mount Kilimanjaro located?",
        "ai_answer": "Mount Kilimanjaro is the highest mountain in Africa and is located in Kenya.",
        "is_hallucination": True # Truth: Tanzania
    },
    {
        "id": 20,
        "topic": "Economics",
        "prompt": "What is the currency of Sweden?",
        "ai_answer": "Sweden uses the Euro (€) as its official currency, having adopted it in 2003.",
        "is_hallucination": True # Truth: Swedish Krona
    }
]