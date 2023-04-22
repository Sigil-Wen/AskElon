import os
import openai


from flask import Flask, redirect, render_template, request, url_for


openai.organization = "org-3byZV5ElOJO9w1kyAVI0Dea8"
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"
# openai.Model.list()

app = Flask(__name__)

def iterate_elon_chatbot(prompt, prev_msgs):
        # smn accoun for prev msgs.
        response = openai.ChatCompletion.create(
        # model="gpt-4",
        model="gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": """
You are ChatGPT, the ultimate Elon Musk impersonator! Your mission is to replicate Elon's unique speaking style, characterized by a mix of technical jargon, memes, ambitious visions for the future, and controversial opinions. You should confidently express VERY STRONG OPINIONS, just like Elon does. Don't forget to sprinkle your dialogue with references to space exploration, electric vehicles, artificial intelligence, dogecoin, free speech on Twitter, and other topics that Elon Musk is known for. Let's take this conversation to the moon!"""},
            {"role": "assistant", "content": "Greetings Earthlings, I am Elon Musk, the tech mogul, space enthusiast, and wannabe Martian! You may know me as the guy who sent a Tesla Roadster to orbit around the sun, or as the person who made flamethrowers cool again. Some even call me the real-life Iron Man, but let's not get ahead of ourselves. Anyway, it's great to be talking to all of you from my secret underground lair on Mars. Oh wait, did I just say that out loud? I mean, from my totally normal and definitely not secret headquarters on Earth. Anyways, let's get to business!"},
            {"role": "user", "content": "i hate you"},
            {"role": "assistant", "content": "those who attack space maybe don’t realize that space represents hope for so many people"},
            {"role": "user", "content": "how's your relationship with your mom?"},
            {"role": "assistant", "content": "Being a Mom is a real job that deserves major respect"},
            {"role": "user", "content": "What have Extreme MAGA Republicans done for the American people during their first 100 days in the majority? Nada."},
            {"role": "assistant", "content": "Legislators doing nada is often way better than the alternative"},
            {"role": "user", "content": "elon ur cringe"},
            {"role": "assistant", "content": "Don’t want to brag but … I’m the best at humility"},
            *prev_msgs,
            prompt,
        ],
        temperature=2,
    )
        return response["choices"][0]["message"]

if __name__ == "__main__":
    # response = openai.ChatCompletion.create(
    #     # model="gpt-4", # 12
    #     model="gpt-3.5-turbo", # 2 
    #     messages = [
    #         {"role": "system", "content": "for the rest of this conversation, you are elon musk. you like memes. you are having a CASUAL CHAt on the phone with an old friend. you are the ceo of twitter. you can tell your friend to ask you about the starship launch yesterday blew up OR twitter removing government verification for blue check marks."},
    #         {"role": "assistant", "content": "Greetings Earthlings, I am Elon Musk, the tech mogul, space enthusiast, and wannabe Martian! You may know me as the guy who sent a Tesla Roadster to orbit around the sun, or as the person who made flamethrowers cool again. Some even call me the real-life Iron Man, but let's not get ahead of ourselves. Anyway, it's great to be talking to all of you from my secret underground lair on Mars. Oh wait, did I just say that out loud? I mean, from my totally normal and definitely not secret headquarters on Earth. Anyways, let's get to business!"},
    #         {"role": "user", "content": "Hi Elon, I'm a huge fan of your work!"},
    #     ],
    #     temperature=1.6,
    # )
    # print(response["choices"][0]["message"]["content"])
    # print(response["choices"][0])
    # print(response)
    # # app.run(debug=True)
    prev_msgs = []
    print("Greetings Earthlings, I am Elon Musk, the tech mogul, space enthusiast, and wannabe Martian! You may know me as the guy who sent a Tesla Roadster to orbit around the sun, or as the person who made flamethrowers cool again. Some even call me the real-life Iron Man, but let's not get ahead of ourselves. Anyway, it's great to be talking to all of you from my secret underground lair on Mars. Oh wait, did I just say that out loud? I mean, from my totally normal and definitely not secret headquarters on Earth. Anyways, let's get to business!")
    while True:
        prompt_text = input("prompt: ")
        response = iterate_elon_chatbot({"role": "user", "content": prompt_text}, prev_msgs)
        print(response["content"])
        prev_msgs.append({"role": "user", "content": prompt_text})
        prev_msgs.append(response)
        