from dotenv import load_dotenv
# import os  # to access environment variables
load_dotenv()  # take environment variables from .env.


def main():
    print("Hello from langchain-course!")
    # print(os.environ.get("OPENAI_API_KEY" ))

if __name__ == "__main__":
    main()
