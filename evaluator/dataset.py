from langsmith import Client
from dotenv import load_dotenv

load_dotenv()

DATASET_NAME = "Pregunta de Series y Películas"

if __name__ == "__main__":
    client = Client()

    examples = [
        (
            "donde puedo ver Lost?",
            'Puedes ver "Lost" en Disney Plus. Aquí tienes el enlace para acceder: [Lost en Disney Plus](https://disneyplus.bn5x.net/c/1206980/705874/9358?u=https%3A%2F%2Fwww.disneyplus.com%2Fseries%2Flost%2F49VjIYAiy7oh&subId3=justappsvod).',
        )
    ]

    inputs = [{"question": input_prompt} for input_prompt, _ in examples]
    outputs = [{"answer": output_answer} for _, output_answer in examples]

    dataset = client.create_dataset(
        dataset_name = DATASET_NAME,
        description = "Ejemplo"
    )

    client.create_examples(inputs=inputs, outputs=outputs, dataset_id=dataset.id)
