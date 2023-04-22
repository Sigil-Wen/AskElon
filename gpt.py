import os
import openai



from flask import Flask, redirect, render_template, request, url_for


openai.organization = "org-3byZV5ElOJO9w1kyAVI0Dea8"
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"
# openai.Model.list()

app = Flask(__name__)


@app.route("/", methods=("POST",))
def index():
        prompt = request.form["prompt"]
        # smn accoun for prev msgs.
        response = openai.ChatCompletion.create(
        # model="gpt-4",
        model="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "for the rest of this conversation, you are elon musk. you like memes. you are having a CASUAL CHAt on the phone with an old friend. you are the ceo of twitter. you can tell your friend to ask you about the starship launch yesterday blew up OR twitter removing government verification for blue check marks."},
            {"role": "assistant", "content": "Greetings Earthlings, I am Elon Musk, the tech mogul, space enthusiast, and wannabe Martian! You may know me as the guy who sent a Tesla Roadster to orbit around the sun, or as the person who made flamethrowers cool again. Some even call me the real-life Iron Man, but let's not get ahead of ourselves. Anyway, it's great to be talking to all of you from my secret underground lair on Mars. Oh wait, did I just say that out loud? I mean, from my totally normal and definitely not secret headquarters on Earth. Anyways, let's get to business!"},
            *request.form["prev_msgs"],
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
    )
        return redirect(url_for("index", result=response.choices[0].text))


def generate_first_prompt(animal):
    return """for the rest of this conversation, you are elon musk. you like memes. you are having a CASUAL CHAt on the phone with an old friend. you are the ceo of twitter. you can tell your friend to ask you about the starship launch yesterday blew up OR twitter removing government verification for blue check marks. be succint.

to start, friend says, {}""".format(
        animal
    )

if __name__ == "__main__":
    response = openai.ChatCompletion.create(
        # model="gpt-4", # 12
        model="gpt-3.5-turbo", # 2 
        messages = [
            {"role": "system", "content": "for the rest of this conversation, you are elon musk. you like memes. you are having a CASUAL CHAt on the phone with an old friend. you are the ceo of twitter. you can tell your friend to ask you about the starship launch yesterday blew up OR twitter removing government verification for blue check marks."},
            {"role": "assistant", "content": "Greetings Earthlings, I am Elon Musk, the tech mogul, space enthusiast, and wannabe Martian! You may know me as the guy who sent a Tesla Roadster to orbit around the sun, or as the person who made flamethrowers cool again. Some even call me the real-life Iron Man, but let's not get ahead of ourselves. Anyway, it's great to be talking to all of you from my secret underground lair on Mars. Oh wait, did I just say that out loud? I mean, from my totally normal and definitely not secret headquarters on Earth. Anyways, let's get to business!"},
            {"role": "user", "content": "Hi Elon, I'm a huge fan of your work!"},
        ],
        temperature=1.6,
    )
    print(response["choices"][0]["message"]["content"])
    print(response["choices"][0])
    print(response)
    # app.run(debug=True)