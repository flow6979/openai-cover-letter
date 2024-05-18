# Openai-cover-letter
The project is a cover letter generator powered by OpenAI's GPT models. It extracts key details from job descriptions, fetches motivation from a Google Doc, and crafts personalized cover letters tailored to specific job listings.

## Things to do before running - 

1. Clone the repo with 
```bash
git clone https://github.com/flow6979/openai-cover-letter.git
```

2. Create OPENAI api key and put it into `my_secrets.py`
3. Put your professional data in `my_secrets.py`
4. Create and access google docs api key from `GCP` and download json file and put in the root of this project.
5. make a new docs file to put your intro in it and connect it with our project by making its sharing type `public + viewer` and put it in `my_json_file` of `my_secrets.py`
6. Now use it !!

## How to use - 
```bash
python3 main.py
```

it would ask:
```bash
Please enter the job description URL:
```

copy paste the job description.

Knock-knock, your cover letter is ready.
